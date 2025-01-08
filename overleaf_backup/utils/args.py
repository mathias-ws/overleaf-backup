import argparse
from enum import Enum


class Modes(Enum):
    """
    The available modes the program can be run in.
    """

    FULL = "full"
    BACKUP = "backup"
    FETCH = "fetch"

    def __str__(self):
        return self.value


def parse_args() -> argparse.Namespace:
    """
    Sets up the command line arguments of the program. It defines arguments for
    specifying the file to save to and which mode the script should run in.

    :return: The program arguments.
    """
    parser = argparse.ArgumentParser(
        prog="overleaf-backup",
        description="A program for taking backups of Overleaf projects.",
    )

    parser.add_argument(
        "mode",
        type=Modes,
        choices=Modes,
        help="Mode to run the program in. Full fetches project list from Overleaf and takes the backup. Backup uses the exported project file from the 'fetch' mode to only take the backup. Fetch downloads the a list of all projects from Overleaf and saves them to a file.",
        default=Modes.FULL,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="The file to use for backup or fetch modes. Default: 'projects.json'.",
        default="projects.json",
    )

    return parser.parse_args()
