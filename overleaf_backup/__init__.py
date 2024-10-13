from overleaf_backup.utils.config import Configuration
from overleaf_backup.utils.logging import setup_logging

config = Configuration()
setup_logging(config.logging)
