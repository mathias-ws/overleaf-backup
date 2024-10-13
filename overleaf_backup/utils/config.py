from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class OverleafSettings(BaseSettings):
    overleaf_url: str = Field("https://www.overleaf.com")
    overleaf_git_url: str = Field("https://git@git.overleaf.com")
    overleaf_git_token: SecretStr
    overleaf_username: str
    overleaf_password: SecretStr

    model_config = SettingsConfigDict(frozen=True, strict=True)


class GitLabSettings(BaseSettings):
    gitlab_url: str = Field("https://gitlab.com")
    gitlab_username: str
    gitlab_access_token: SecretStr
    gitlab_group: str = Field("")

    model_config = SettingsConfigDict(frozen=True, strict=True)


class LoggingSettings(BaseSettings):
    level: str = "info"

    model_config = SettingsConfigDict(frozen=True, strict=True)


class Configuration(BaseSettings):
    overleaf: OverleafSettings = OverleafSettings()
    gitlab: GitLabSettings = GitLabSettings()
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(frozen=True, strict=True)
