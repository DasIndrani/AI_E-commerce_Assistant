import os
import logging
from datetime import datetime

logging_str = "[%(asctime)s: %(levelname)s: %(lineno)s: %(module)s: %(message)s]"
log_file_name = f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.log"

log_dir = "logs"
os.makedirs(log_dir,exist_ok=True)
log_file_path = os.path.join(log_dir,log_file_name)

logging.basicConfig(filename=log_file_path, format=logging_str, level=logging.INFO)
