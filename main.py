import signal
import json
from datetime import datetime

import requests
from pyrogram import Client
import time
from config import *


def _timeout_handler(signum, frame):
    raise Exception('timeout!')


def ignore_exception(func):
    def new_func(*args, **kwargs):
        global number_of_exception
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(30)
        try:
            result = func(*args, **kwargs)
            number_of_exception = 0
            signal.alarm(0)
            return result
        except Exception as ex:
            number_of_exception += 1
            print(number_of_exception)
            if number_of_exception > 10:
                print("Hi")
                client.send_message(chat_id=SUPPORTER, text="سگ بازاربین درست کار نمی کند :(")
            print('IGNORED:', ex)
        signal.alarm(0)
        return

    new_func.__name__ = func.__name__
    return new_func


@ignore_exception
def send_message():
    chat_id = CHANNEL_SEE
    print("__________________________________________\n*************************************")
    global number_of_delay, before
    history = client.get_history(chat_id, limit=1)
    now_time = history[0].date
    show_now_time = datetime.fromtimestamp(now_time)
    # print(show_now_time)
    if "خطا" in history[0].text:
        client.send_message(chat_id=SUPPORTER, text="بازاربین قطع داده :(")
    if now_time == before:
        print(''.join((str(number_of_delay), ' : ', "not change in channel")))
        number_of_delay += 1
    else:
        print("new post send to channel")
        number_of_delay = 0

    if number_of_delay > 20:
        client.send_message(chat_id=SUPPORTER, text="بازاربین قطع شده است :(")

    before = now_time



def run():
    print('running...')
    print('use ctrl+C to stop')
    try:
        delay = 60
        while True:
            if not DEBUG_ON:
                time.sleep(delay - int(time.time()) % delay)
            start_time = time.time()
            send_message()
            running_time = time.time() - start_time
            print('running_time:', round(running_time, 2), 'S')
    except KeyboardInterrupt:
        print('Stopped by KeyboardInterrupt')


def _init_session(self) -> requests.Session:
    headers = self._get_headers()
    session = requests.session()
    session.headers.update(headers)
    return session


before = datetime.now()
number_of_delay = 0
number_of_exception = 0
client = Client(session_name)
client.start()

if __name__ == '__main__':
    run()
