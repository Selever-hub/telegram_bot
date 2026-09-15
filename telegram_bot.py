import urllib.request
import urllib.parse
import time
from datetime import datetime

TOKEN = "8993713089:AAEpvvyBzOS9r-xe8c5m2MRgwIyqw5priEs"
CHAT_ID = "-1002354604250"

schedule = {
    "Понедельник": [
        ("Артем", "10:00", "12:00"),
        ("Артем", "18:30", "20:00"),
        ("Кирилл", "15:00", "18:00")
    ],
    "Вторник": [
        ("Артем", "10:00", "11:00"),
        ("Артем", "19:00", "20:00")
    ],
    "Среда": [
        ("Артем", "10:00", "12:00"),
        ("Артем", "18:30", "20:00"),
        ("Ярослав", "15:30", "17:20")
    ],
    "Четверг": [
        ("Артем", "10:00", "12:00"),
        ("Артем", "18:20", "20:00"),
        ("Ярослав", "15:30", "17:20")
    ],
    "Пятница": [
        ("Артем", "10:00", "11:00"),
        ("Арсений", "18:00", "20:00"),
        ("Ярослав", "15:30", "17:20"),
        ("Кирилл", "15:00", "18:00")
    ],
    "Суббота": [
        ("Арсений", "11:00", "12:00"),
        ("Арсений", "18:00", "20:00"),
        ("Ярослав", "10:00", "20:00")
    ],
    "Воскресенье": [
        ("Арсений", "10:00", "12:00"),
        ("Ярослав", "10:00", "20:00")
    ]
}

days = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
]

sent_shifts = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text
    }).encode()

    try:
        urllib.request.urlopen(url, data)
        print("Сообщение отправлено!")
    except Exception as e:
        print("Ошибка:", e)

while True:
    now = datetime.now()
    day = days[now.weekday()]
    current_time = now.strftime("%H:%M")

    if day in schedule:
        for name, start, end in schedule[day]:

            shift_id = f"{day}_{name}_{start}_{end}_{now.date()}"

            if current_time == start and shift_id not in sent_shifts:
                start_time = datetime.strptime(start, "%H:%M")
                end_time = datetime.strptime(end, "%H:%M")

                duration = end_time - start_time
                minutes = int(duration.total_seconds() // 60)

                hours = minutes // 60
                mins = minutes % 60

                if mins == 0:
                    duration_text = f"{hours} ч."
                else:
                    duration_text = f"{hours} ч. {mins} мин."

                text = (
                    "🟢 Смена открыта!\n\n"
                    f"👤 Модератор: {name}\n"
                    f"⏱ Продолжительность: {duration_text}\n"
                    f"🕐 Время: {start}–{end}"
                )

                send_message(text)
                sent_shifts.add(shift_id)

    time.sleep(20)
