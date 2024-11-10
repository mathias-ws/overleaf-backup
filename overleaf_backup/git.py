import logging

import gitlab
from gitlab.exceptions import GitlabCreateError

from overleaf_backup.utils.config import GitLabSettings


class GitLab:
    def __init__(self, config: GitLabSettings):
        """
        Initializes the GitLab object and authenticates with the GitLab API.

        :raises gitlab.GitlabAuthenticationError: If unable to authenticate with GitLab.
        """
        self.__config = config
        self.__gl = gitlab.Gitlab(
            url=config.url,
            private_token=self.__config.access_token.get_secret_value(),
        )
        self.__gl.auth()

        if self.__gl.user is not None:
            logging.info(f"Successfully authenticated as {self.__gl.user.username}")
        else:
            logging.error("Unable to authenticate with GitLab")
            raise gitlab.GitlabAuthenticationError("unable to authenticate with GitLab")

        if self.__config.group:
            self.__group_id = self.group_exists(self.__config.group)
        else:
            self.__group_id = None

    def group_exists(self, group_name: str) -> int:
        """
        Checks if the specified group exists in GitLab.

        :param group_name: The name of the group.
        :raises ValueError: When unable to find specified GitLab group.
        :return: The group id.
        """
        groups_found = self.__gl.groups.list(search=group_name)

        if len(groups_found) > 0:
            logging.info(
                f"Found GitLab group {group_name} with id: {groups_found[0].id}."
            )
            return int(groups_found[0].id)
        else:
            logging.error(
                f"Unable to find GitLab group {group_name} when searching for groups"
            )
            raise ValueError(f"GitLab group {group_name} does not exist in GitLab")

    def create_project(self, project_name: str) -> str:
        """
        Creates a project in GitLab.

        :param project_name: The name of the project.
        :return: Url to GitLab repo.
        """
        if self.__group_id:
            return self.__create_project_in_group(str(self.__group_id), project_name)
        else:
            return self.__create_project(project_name)

    def __create_project(self, project_name: str):
        try:
            project = self.__gl.projects.create({"name": str(project_name)})
            logging.info(
                f"Successfully created project {project_name} with id {project.id}."
            )
            return project.http_url_to_repo
        except GitlabCreateError as e:
            if e.error_message["project_namespace.name"] == ["has already been taken"]:
                logging.debug(f"Project {project_name} already exists.")

                project = self.__get_project(project_name)
                if project:
                    return project.http_url_to_repo

            logging.error(f"Unable to create project {project_name}, with error: {e}")
        except gitlab.GitlabAuthenticationError as e:
            logging.error(
                f"Authentication error when creating project {project_name}, with error: {e}"
            )
        except Exception as e:
            logging.error(
                f"Unknown error when creating project {project_name}, with error: {e}"
            )

    def __create_project_in_group(self, group_id: str, project_name: str):
        try:
            logging.debug(f"Name of project to be created {project_name}")
            project = self.__gl.projects.create(
                {"name": project_name, "namespace_id": group_id}
            )

            logging.info(
                f"Successfully created project {project_name} in namespace {group_id}."
            )
            return project.http_url_to_repo
        except gitlab.GitlabListError as e:
            logging.error(
                f"Unable to find group {group_id} when creating project {project_name}, with error: {e}"
            )
        except GitlabCreateError as e:
            if e.error_message["project_namespace.name"] == ["has already been taken"]:
                logging.debug(
                    f"Project {project_name} in namespace {group_id} already exists."
                )

                project = self.__get_project(project_name)
                if project:
                    logging.debug(
                        f"Found {project_name} in namespace {group_id}, it already existed"
                    )
                    return project.http_url_to_repo

            logging.error(
                f"Unable to create project {project_name} in namespace {group_id}, with error: {e}"
            )
        except gitlab.GitlabAuthenticationError as e:
            logging.error(
                f"Authentication error when creating project {project_name} in namespace {group_id}, with error: {e}"
            )
        except Exception as e:
            logging.error(
                f"Unknown error when creating project {project_name} in namespace {group_id}, with error: {e}"
            )

    def __get_project(self, project_name: str):
        try:
            if self.__group_id:
                project = self.__gl.projects.get(
                    f"{self.__config.group}/{project_name}"
                )
            else:
                default_namespace = self.__gl.user.username
                project = self.__gl.projects.get(f"{default_namespace}/{project_name}")
            return project
        except gitlab.GitlabGetError as e:
            logging.error(f"Unable to get project {project_name}, with error: {e}")
        except gitlab.GitlabAuthenticationError as e:
            logging.error(
                f"Authentication error when getting project {project_name}, with error: {e}"
            )
        except Exception as e:
            logging.error(
                f"Unknown error when getting project {project_name}, with error: {e}"
            )
