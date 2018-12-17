import json
from pprint import pprint
from decouple import config

import requests
from flask import Flask, request

from . import utils

app = Flask(__name__)

BOT_TOKEN = config('BOT_TOKEN')
SERVER_URL = f'{config("NGROK_URL")}/{BOT_TOKEN}'


def _get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(BOT_TOKEN, method)


def _process_message(update):
    data = {}
    data["chat_id"] = update["message"]["from"]["id"]

    if update["message"]["text"].lower().find('nadaprafazer') == 1:
        command = update["message"]["text"].split()
        if len(command) >= 2:
            threads = json.dumps(utils.get_reddits(command[1], 5000), indent=2)
            data["text"] = threads
        else:
            data["text"] = "Exemplo: /NadaPraFazer cats;dogs"
    else:
        data["text"] = "Help: /NadaPraFazer [+ Lista de subrredits]"

    requests.post(_get_url("sendMessage"), data=data)


@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
def _process_update():
    if request.method == "POST":
        update = request.get_json()
        if "message" in update:
            _process_message(update)
        return "ok!", 200


def _configure():
    requests.get(_get_url("setWebhook"), data={"url": SERVER_URL})
    response = requests.get(_get_url("getWebhookInfo"))
    pprint(response.status_code)
    pprint(response.json())


_configure()
