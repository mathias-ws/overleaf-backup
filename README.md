# overleaf-backup

[![release](https://gitlab.com/mathias_ws/overleaf-backup/-/badges/release.svg?order_by=release_at)](https://gitlab.com/mathias_ws/overleaf-backup/-/releases)
[![pipeline](https://gitlab.com/mathias_ws/overleaf-backup/-/badges/main/pipeline.svg)](https://gitlab.com/mathias_ws/overleaf-backup/-/pipelines)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://gitlab.com/mathias_ws/overleaf-backup/-/blob/main/LICENSE)
[![docker](https://img.shields.io/docker/pulls/mathiasws/overleaf-backup)](https://hub.docker.com/r/mathiasws/overleaf-backup)
[![docker](https://img.shields.io/docker/image-size/mathiasws/overleaf-backup)](https://hub.docker.com/r/mathiasws/overleaf-backup)

**This repository resides in [GitLab](https://gitlab.com/mathias_ws/overleaf-backup), but is mirrored to [GitHub](https://github.com/mathias-ws/overleaf-backup).**
All issues and Merge Requests should be created in GitLab.

This script aims to clone and sync all Overleaf projects connected to your account and sync them to GitLab.
The script works by using Selenium to log in to Overleaf and fetch the list of projects. The list of
projects is then parsed to get the ids and the name of the projects. Using git, the projects
are downloaded to a local directory. If a GitLab repository does not exist for the project,
one is automatically created. The GitLab repo is then added as a remote and then a push is done to this remote.
This creates a backup of all Overleaf projects to GitLab.

Because of compatibility issues with some of the packages used, only Python versions <3.12 is required.

## Known issues

- Sometimes captcha is required to log in to Overleaf. (This does not seem to be an issue from the NTNU network)
  - This might be solved by [this merge request](https://gitlab.com/mathias_ws/overleaf-backup/-/merge_requests/10).
- Some shared projects require some manual interaction before it can be cloned.

## Installation

### Docker

A Docker container is provided that runs the script. The imaged can be fetched from [Docker hub](https://hub.docker.com/repository/docker/mathiasws/overleaf-backup).
The image is called `mathiasws/overleaf-backup`.

### Local

To run the script locally, some more steps are required.

1. **Clone the repository:**

`git clone https://gitlab.com/mathias_ws/overleaf-backup.git`

2. **Install the required packages:**

For the script to work, google chrome and the chromedriver needs to be installed.
Additionally, the required python packages must be installed. It is recommended to use a virtual environment.

```bash
pip install venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Set the required environment variables**

4. **Run the script:**

`python -m overleaf_backup`

## Configuration

All configurations for this script is done through environment variables.

| Variable            | Description                                                                       | Required | Default                      |
| ------------------- | --------------------------------------------------------------------------------- | -------- | ---------------------------- |
| OVERLEAF_URL        | Url to Overleaf instance.                                                         | No       | https://www.overleaf.com     |
| OVERLEAF_GIT_URL    | Git url to Overleaf instance.                                                     | No       | https://git@git.overleaf.com |
| OVERLEAF_USERNAME   | Overleaf username.                                                                | Yes      | NA                           |
| OVERLEAF_PASSWORD   | Overleaf password.                                                                | Yes      | NA                           |
| OVERLEAF_GIT_TOKEN  | Git token provided by Overleaf.                                                   | Yes      |                              |
| GITLAB_URL          | Url to GitLab instance.                                                           | No       | https://gitlab.com           |
| GITLAB_USERNAME     | GitLab username.                                                                  | Yes      | NA                           |
| GITLAB_ACCESS_TOKEN | Access token to GitLab, must have `api` rights.                                   | Yes      | NA                           |
| GITLAB_GROUP        | Name of GitLab group to use, if not set the default namespace (username) is used. | No       | NA                           |
| LOGGING_LEVEL       | The logging level.                                                                | No       | info                         |

## Contribution

This repository resides in [GitLab](https://gitlab.com/mathias_ws/overleaf-backup), but is mirrored to [GitHub](https://github.com/mathias-ws/overleaf-backup).
All issues and Merge Requests should be created in GitLab.

All contributions and issues are welcome.
When implementing features and creating Merge Requests, please ensure that
your commits follows the [commit message format](https://semantic-release.gitbook.io/semantic-release#commit-message-format)
required by [semantic-release](https://semantic-release.gitbook.io/semantic-release/).
This will ensure that the version and changelog is automatically updated.
