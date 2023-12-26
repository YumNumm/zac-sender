#!/usr/bin/env python3
import time
import json
import requests
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from enum import Enum
import argparse


class YumekinSendType(Enum):
    BEGIN = "開始"
    LUNCH = "休憩"
    RESUME = "再開"
    FINISH = "終了"
    BREAK = "中断"
    REPORT = "報告"


class YumekinSender:
    __url__ = "https://yumekin.corp.yumemi.jp/"

    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument(
            # Change this path to your own one
            "--user-data-dir=/Users/r_onoue/dev/github.com/YumNumm/zac-sender/server/src/server/chrome_profile"
        )
        options.add_argument("--profile-directory=Profile")
        self.driver = webdriver.Chrome(options=options)

    def send(self, type: YumekinSendType) -> None:
        self.__show_top_page__()
        self.__wait_for_load__()
        self.__select_status__(type)
        self.__post_status__()

    def __show_top_page__(self) -> None:
        self.driver.get(self.__url__)

    def __wait_for_load__(self) -> None:
        # Yumekin Icon
        xPath = "/html/body/div[1]/div/div/div[1]/div[1]/a/img"
        # Wait until the element is loaded for 10 seconds
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, xPath))
        )

    def __select_status__(self, type: YumekinSendType) -> None:
        xpath = f"//span[contains(.,'{type.value}')]"

        print(xpath)
        # Wait until the element is loaded for 4 seconds
        WebDriverWait(self.driver, 4).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        )
        time.sleep(1)
        # Click
        self.driver.find_element(By.XPATH, xpath).click()

    def __post_status__(self) -> None:
        xpath = "/html/body/div[1]/div/div/div[3]/form/div[6]/button"
        self.driver.find_element(By.XPATH, xpath).click()
        # wait 1 sec
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Yumekin Sender")

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=[e.name for e in YumekinSendType],
        required=True,
        help="type of yumekin",
    )

    args = parser.parse_args()
    type = YumekinSendType[args.type]

    sender = YumekinSender()
    sender.send(type)
