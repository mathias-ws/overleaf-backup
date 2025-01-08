import logging
import sys
from pathlib import Path

from overleaf_backup import config
from overleaf_backup.backup import backup, fetch
from overleaf_backup.overleaf import read_project_list, save_project_list
from overleaf_backup.utils.args import Modes, parse_args
from overleaf_backup.utils.config import Configuration


def full_mode(config: Configuration) -> None:
    """
    Runs the program in full mode. It fetches the project list from Overleaf
    and takes backups of these.

    :param config: The program configuration file.
    """
    logging.info("Running in full mode: This will perform a complete backup and fetch.")

    projects = fetch(config)

    if not projects:
        logging.critical("No projects found, unable to take backups")
        sys.exit(1)

    backup(config, projects)


def backup_mode(path: str, config: Configuration) -> None:
    """
    Runs the program in backup mode. It uses a prefetched project list and takes backup of it.

    :param path: A file path for where to save the project list.
    :param config: The program configuration file.
    """
    if not Path(path).exists():
        logging.critical(
            "Running in backup mode: No file specified, unable to take backup."
        )
        sys.exit(1)

    logging.info(f"Running in backup mode: Using file '{path}' for the backup.")

    projects = read_project_list(path)

    if not projects:
        logging.critical("Unable to find any projects, cannot take backup.")
        sys.exit(1)

    backup(config, projects)


def fetch_mode(path: str, config: Configuration) -> None:
    """
    Runs the program in the fetch mode. It fetches the project list from
    Overleaf and saves it to a specified file.

    :param path: A file path for where to save the project list.
    :param config: The program configuration file.
    """
    logging.info(f"Running in fetch mode: Saving projects to '{path}'.")

    projects = fetch(config)

    save_project_list(projects, path)


def main() -> None:
    """
    The main function that runs the program in the correct mode.
    """
    try:
        args = parse_args()

        match args.mode:
            case Modes.FULL:
                full_mode(config)
            case Modes.BACKUP:
                backup_mode(args.file, config)
            case Modes.FETCH:
                fetch_mode(args.file, config)
            case _:
                logging.critical(
                    f"Invalid mode. Valid options: {[m.value for m in Modes]}."
                )
                sys.exit(1)
    except Exception as e:
        logging.debug(f"Unknown error caught from main: {e}")
        logging.critical("Unknown critical error occured.")
        sys.exit(1)


if __name__ == "__main__":
    main()
