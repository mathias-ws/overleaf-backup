from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class OverleafSettings(BaseSettings):
    url: str = Field("https://www.overleaf.com")
    git_url: str = Field("https://git@git.overleaf.com")
    git_token: SecretStr
    username: str
    password: SecretStr

    model_config = SettingsConfigDict(frozen=True, strict=True, env_prefix="OVERLEAF_")


class GitLabSettings(BaseSettings):
    url: str = Field("https://gitlab.com")
    username: str
    access_token: SecretStr
    group: str = Field("")

    model_config = SettingsConfigDict(frozen=True, strict=True, env_prefix="GITLAB_")


class LoggingSettings(BaseSettings):
    level: str = "info"

    model_config = SettingsConfigDict(frozen=True, strict=True, env_prefix="LOGGING_")


class Configuration(BaseSettings):
    overleaf: OverleafSettings = OverleafSettings()
    gitlab: GitLabSettings = GitLabSettings()
    logging: LoggingSettings = LoggingSettings()

    model_config = SettingsConfigDict(frozen=True, strict=True)
