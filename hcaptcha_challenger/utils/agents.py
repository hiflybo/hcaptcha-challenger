# -*- coding: utf-8 -*-
# Time       : 2023/8/15 20:41
# Author     : QIN2DIM
# GitHub     : https://github.com/QIN2DIM
# Description:
import logging
import os
import sys
import typing
import warnings

from loguru import logger
from undetected_chromedriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_challenge_ctx(
    silence: typing.Optional[bool] = None, lang: typing.Optional[str] = None, **kwargs
):
    """
    Challenger drive for handling human-machine challenges.

    :param silence: Control headless browser
    :param lang: Restrict the language of hCAPTCHA label.
      See https://github.com/QIN2DIM/hcaptcha-challenger/issues/13
    :rtype: undetected_chromedriver.Chrome
    """
    # Control headless browser
    # If on Linux, and no X server is available (`DISPLAY` not set), assume
    # headless operation
    silence = (
        True
        if silence is None or ("linux" in sys.platform and "DISPLAY" not in os.environ)
        else silence
    )

    # - Use chromedriver cache to improve application startup speed
    # - Requirement: undetected-chromedriver >= 3.1.5.post2
    logging.getLogger("WDM").setLevel(logging.NOTSET)
    driver_executable_path = ChromeDriverManager().install()

    logger.debug("🎮 Activate challenger context")
    return Chrome(
        options=create_chrome_options(silence, lang),
        headless=silence,
        driver_executable_path=driver_executable_path,
        **kwargs,
    )


def create_chrome_options(
    silence: typing.Optional[bool] = None, lang: typing.Optional[str] = None
) -> ChromeOptions:
    """
    Create ChromeOptions for undetected_chromedriver.Chrome

    :param silence: Control headless browser
    :param lang: Restrict the language of hCAPTCHA label.

    :rtype: undetected_chromedriver.ChromeOptions
    """

    # - Restrict browser startup parameters
    options = ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--disable-dev-shm-usage")

    # - Restrict the language of hCaptcha label
    # - Environment variables are valid only in the current process
    # and do not affect other processes in the operating system
    os.environ["LANGUAGE"] = "en_US" if lang is None else lang
    options.add_argument(f"--lang={os.getenv('LANGUAGE')}")

    if silence is True:
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")

    return options
