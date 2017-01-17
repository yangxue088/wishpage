# -*- coding: utf-8 -*-

import requests


def send_mail_message(sender, receipt, subject, content):
    return requests.post(
        "https://api.mailgun.net/v3/tjchtech.com/messages",
        auth=("api", "key-b6139f5afd5b82a73a810724b263b380"),
        data={"from": sender,
              "to": receipt,
              "subject": subject,
              "text": content}, timeout=10)
