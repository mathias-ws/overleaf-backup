import json
import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from overleaf_backup.utils.config import OverleafSettings


class Overleaf:
    def __init__(self, config: OverleafSettings):
        self.__driver = self.__create_web_driver()
        self.__config = config

    def __create_web_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        return webdriver.Chrome(options=options)

    def overleaf_sign_in(self):
        logging.info("Attempting to log into overleaf")

        self.__driver.get(f"{self.__config.url}/login")

        time.sleep(1)

        username_field = self.__driver.find_element(By.XPATH, '//*[@id="email"]')
        password_field = self.__driver.find_element(By.XPATH, '//*[@id="password"]')

        username_field.send_keys(self.__config.username)

        # Must be done to not log the password
        org_log_level = logging.getLogger().getEffectiveLevel()
        if org_log_level == logging.DEBUG:
            logging.debug(
                "Setting log level to INFO, to prevent password from being logged."
            )
            logging.getLogger().setLevel(logging.INFO)

        password_field.send_keys(self.__config.password.get_secret_value())

        # Must be done to not log the password
        if org_log_level == logging.DEBUG:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug("Resetting log level back to DEBUG.")

        self.__driver.find_element(
            By.XPATH, '//*[@id="main-content"]/div[1]/form/div[5]/button'
        ).click()

        time.sleep(2)

    def overleaf_fetch_project_list(self):
        if self.__driver.current_url != "https://www.overleaf.com/project":
            self.__driver.get("https://www.overleaf.com/project")

        time.sleep(2)

        return self.__driver.page_source

    def parse_project_list(self, html_project_list: str) -> list[dict[str, str]]:
        soup = BeautifulSoup(html_project_list, "lxml")

        try:
            data = soup.find("meta", dict(name="ol-prefetchedProjectsBlob")).get(
                "content"
            )
            data = json.loads(str(data))
        except Exception as e:
            logging.error("Unable to parse project list from Overleaf.")
            logging.debug(
                f"Unable to parse projects with error {e}. HTML contents: {html_project_list}"
            )

            return []

        projects = []

        for project_data in data["projects"]:
            projects.append(
                {
                    "name": str(project_data["name"]),
                    "id": project_data["id"],
                }
            )

        return projects

    def close_driver(self) -> None:
        self.__driver.close()
        self.__driver.quit()
