import dotenv
import logging

def load_dotenv():
    logging.info("Loading .env file.")
    if dotenv.load_dotenv():
        logging.info("Loaded .env succesfully")
    else:
        logging.warning("No .env file found.")