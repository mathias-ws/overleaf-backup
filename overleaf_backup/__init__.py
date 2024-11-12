from overleaf_backup.utils.dotenv import load_dotenv
from overleaf_backup.utils.logging import setup_logging, set_log_level

setup_logging()
load_dotenv()

from overleaf_backup.utils.config import Configuration

config = Configuration()
set_log_level(config.logging.level)
