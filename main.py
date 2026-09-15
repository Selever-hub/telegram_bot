import os
import time
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

TOKEN = os.environ["BOT_TOKEN"]

GROUP_ID = "-1002354604250"
THREAD_ID = 411435

MOSCOW = ZoneInfo("Europe/Moscow")
NOVOSIBIRSK = ZoneInfo("Asia/Novosibirsk")

SCHEDULE = {
    "Артем": {
        0: [("10:00", "12:00"), ("18:30", "20:00")],
        1: [("10:00", "11:00"), ("19:00", "20:00")],
        2: [("10:00", "12:00"), ("18:30", "20:00")],
        3: [("10:00", "12:00"), ("18:20", "20:00")],
        4: [("10:00", "11:00")],
    },

    "Арсений": {
        4: [("18:00", "20:00")],
        5: [("11:00", "12:00"), ("18:00", "20:00")],
        6: [("10:00", "12:00")],
    },

    "Ярослав": {
        2: [("15:30", "17:20")],
        3: [("15:30", "17:20")],
        4: [("15:30", "17:20")],
        5: [("10:00", "20:00")],
        6: [("10:00", "20:00")],
    },

    "Кирилл": {
        0: [("15:00", "18:00")],
        4: [("15:00", "18:00")],
    },
}

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": GROUP_ID,
        "message_thread_id": THREAD_ID,
        "text": text
    }

    requests.post(url, data=data)

sent_start = set()
sent_end = set()

while True:

    for name, days in SCHEDULE.items():

        if name == "Артем":
            now = datetime.now(NOVOSIBIRSK)
        else:
            now = datetime.now(MOSCOW)

        day = now.weekday()
        current_time = now.strftime("%H:%M")
        date = now.strftime("%Y-%m-%d")

        if day not in days:
            continue

        for start, end in days[day]:

            start_key = f"{date}_{name}_{start}"
            end_key = f"{date}_{name}_{end}"

            if current_time == start and start_key not in sent_start:

                send_message(
                    f"🚇 Смена началась!\n\n"
                    f"👤 Сотрудник: {name}\n"
                    f"🕐 Время: {start} — {end}"
                )

                sent_start.add(start_key)

            if current_time == end and end_key not in sent_end:

                send_message(
                    f"🔴 Смена закрыта!\n\n"
                    f"👤 Сотрудник: {name}\n"
                    f"🕐 Время смены: {start} — {end}"
                )

                sent_end.add(end_key)

    if len(sent_start) > 1000:
        sent_start.clear()
        sent_end.clear()

    time.sleep(20)

