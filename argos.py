import logging
import requests
import pickle
import telegram
from targets import targets
from secrets import TOKEN, CHAT_IDS
from asyncio import run
from datetime import datetime
from bs4 import BeautifulSoup

BOT = telegram.Bot(TOKEN)
WORKDIR = "/data/"

logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
    filename=WORKDIR + "argos.log"
)

async def main():

    for target in targets:
        if target["method"] == "GET":
            r = requests.get(target["url"], headers=target["headers"])
        elif target["method"] == "POST":
            r = requests.post(target["url"], json=target["data"], headers=target["headers"])
        else:
            raise ValueError(f"Unknown method: {target['method']}")

        if not r.status_code == 200:
            raise ConnectionError(f"Got a non-OK status code: {r.status_code}")

        content = BeautifulSoup(r.content, "html.parser")

        if target["html-tag"]:
            result = [item.text for item in content.find_all(target["html-tag"])]
        elif target["html-class"]:
            result = [item.text for item in content.find_all(target["html-class"])]
        elif target["html-id"]:
            result = [item.text for item in content.find_all(target["html-id"])]
        else:
            result = [item.text for item in content.find_all()]

        # If the file does not exist yet, we're not going to bother
        # creating it because that will happen anyways
        prev_result = ""
        try:
            with open(WORKDIR + target["id"], 'rb') as rd:
                prev_result = pickle.load(rd)
        except:
            pass
            
        if prev_result != result:
            # Save the new result
            with open(WORKDIR + target["id"], 'wb') as wr:
                pickle.dump(result, wr)
                
            # Save the result with a timestamp as a snapshot
            with open(WORKDIR + target["id"] + datetime.now().strftime("-%Y%m%d-%H%M"), 'wb') as wr:
                pickle.dump(result, wr)
            
            for chat_id in CHAT_IDS:
                await BOT.send_message(text=f"Something changed on {target['id']}: {target['url']}", chat_id=chat_id)


if __name__ == '__main__':
    run(main())
