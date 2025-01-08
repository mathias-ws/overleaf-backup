import logging
import os
import subprocess
from pathlib import Path

import regex

from overleaf_backup.git import GitLab
from overleaf_backup.overleaf import Overleaf
from overleaf_backup.utils.config import Configuration


class OverleafRepo:
    """
    Class that represents a Overleaf project repository.
    It has the ability to clone the repository, add a remote and push to the backup remote.
    """

    def __init__(
        self,
        config: Configuration,
        overleaf_project_id: str,
        backup_url: str,
        clone_path: Path,
    ):
        """
        Initialize the OverleafRepo object.

        :param overleaf_url: The url to the Overleaf project.
        :param backup_url: The url to the backup repository.
        :param clone_path: The path where the repository will be cloned.
        """
        self.__overleaf_url = f"{config.overleaf.git_url}/{overleaf_project_id}"
        self.__overleaf_project_id = overleaf_project_id
        self.__backup_url = backup_url
        logging.debug(
            f"Clone path entered to OverleafRepo is {clone_path.absolute()} for project {overleaf_project_id}."
        )
        self.__clone_path = clone_path.absolute()
        self.__config = config

    def clone_repo(self):
        """
        Clone the Overleaf repository into the clone path.
        """
        if Path(f"{self.__clone_path}/{self.__overleaf_project_id}").exists():
            if self.__run_git_command(
                [
                    "git",
                    "-C",
                    f"{self.__clone_path}/{self.__overleaf_project_id}",
                    "pull",
                ]
            ):
                logging.info(f"{self.__overleaf_project_id} was successfully pulled.")
            else:
                logging.error(f"Unable to pull {self.__overleaf_project_id}.")

            return

        # Cloning the repo if it is not already cloned
        if self.__run_git_command(
            ["git", "-C", self.__clone_path, "clone", self.__overleaf_url]
        ):
            logging.info(
                f"Was able to clone {self.__overleaf_url} into {self.__clone_path}"
            )
        else:
            logging.error(
                f"Unable to clone {self.__overleaf_url} into {self.__clone_path}"
            )

    def add_remote(self, remote_name: str = "backup"):
        """
        Adds the backup remote to the cloned Overleaf project.

        :param remote_name: The name of the remote.
        """
        if self.__run_git_command(
            [
                "git",
                "-C",
                f"{self.__clone_path}/{self.__overleaf_project_id}",
                "remote",
                "add",
                remote_name,
                self.__backup_url,
            ],
        ):
            logging.info(
                f"Successfully added remote {remote_name} to {self.__overleaf_project_id}."
            )
        else:
            logging.error(
                f"Unable to add remote {remote_name} to {self.__overleaf_project_id}. This might be because the remote already exists."
            )

    def push(self, remote_name: str = "backup"):
        """
        Pushes the Overleaf project to the backup remote.

        :param remote_name: The name of the remote
        """
        if self.__run_git_command(
            [
                "git",
                "-C",
                f"{self.__clone_path}/{self.__overleaf_project_id}",
                "push",
                remote_name,
            ],
        ):
            logging.info(
                f"Successfully pushed {self.__overleaf_project_id} to {remote_name}."
            )
        else:
            logging.error(
                f"Unable to push {self.__overleaf_project_id} to {remote_name}."
            )

    def __run_git_command(self, command: list) -> bool:
        """
        Runs arbritarty git commands and returns True if the command was successful.

        :param command: A list of commands to run.
        :return: If the command was successful.
        """
        if "clone" in command or "pull" in command:
            os.environ["GIT_USERNAME"] = self.__config.overleaf.username
            os.environ["GIT_PASSWORD"] = (
                self.__config.overleaf.git_token.get_secret_value()
            )
        else:
            os.environ["GIT_USERNAME"] = self.__config.gitlab.username
            os.environ["GIT_PASSWORD"] = (
                self.__config.gitlab.access_token.get_secret_value()
            )

        os.environ["GIT_ASKPASS"] = "../../assets/git_creds.sh"

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode == 0:
            logging.debug(
                f"Command '{command}' was successful with output: {result.stdout}."
            )
        else:
            logging.debug(
                f"Command '{command}' was unsuccessful, with output: {result.stderr}."
            )

        return result.returncode == 0


def transform_string_unicode(s):
    # Replace all characters not in the allowed set with '-'
    allowed_chars_pattern = r"[^\p{Letter}\p{Number}_\.\+\-]"
    s = regex.sub(allowed_chars_pattern, "-", s)

    # Ensure the first character is a letter, digit, or underscore '_'
    if not regex.match(r"^[\p{Letter}\p{Number}_]", s):
        if s:
            s = "_" + s[1:]
        else:
            s = "_"

    # Collapse multiple '-' or '_' into a single '-'
    s = regex.sub(r"[-_]+", "-", s)

    return s


def fetch(config: Configuration) -> list:
    """
    Fetches project list from Overleaf.

    :param config: The program configuration.
    :return: A list of all Overleaf projects found.
    """
    overleaf = Overleaf(config.overleaf)
    overleaf.overleaf_sign_in()
    project_list = overleaf.overleaf_fetch_project_list()
    overleaf.close_driver()

    overleaf_projects = overleaf.parse_project_list(project_list)

    logging.info(f"Found {len(overleaf_projects)} projects in Overleaf")

    return overleaf_projects


def backup(config: Configuration, overleaf_projects: list) -> None:
    """
    Signs in to GitLab, downloads git projects from Overleaf and pushes them to GitLab.

    :param config: The program configuration.
    :param overleaf_projects: A list of all projects to take backups of.
    """
    gitlab_obj = GitLab(config.gitlab)

    Path("clone_folder").mkdir(exist_ok=True)

    for project in overleaf_projects:
        logging.info(f"Backing up project {project['name']} with id {project['id']}.")
        try:
            repo_name = transform_string_unicode(f"{project['id']}-{project['name']}")
            gitlab_url = gitlab_obj.create_project(repo_name)
            if not gitlab_url:
                logging.debug(
                    f"Unable to find backup url for project {repo_name} for Overleaf project {project['name']} with id {project['id']}."
                )
                raise ValueError("Unable to get the backup url for the project.")

            logging.debug(f"Backup url: {gitlab_url}")

            overleaf_repo = OverleafRepo(
                config, project["id"], gitlab_url, Path("clone_folder")
            )
            overleaf_repo.clone_repo()
            overleaf_repo.add_remote()
            overleaf_repo.push()

            logging.info(
                f"Successfully backed up {project['name']} with id {project['id']} to {gitlab_url}."
            )
        except Exception as e:
            logging.error(
                f"Unable to backup project {project['name']} with id {project['id']}. Unknown error: {e}"
            )
