"""Генерация синтетических данных для проекта"""
import csv
import math
import random
from datetime import datetime, timedelta

random.seed(42)


def write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"{path}: {len(rows)} строк")


#Доля мобильного и десктопного трафика
def traffic():
    rows = []
    day = datetime(2026, 1, 1)
    for i in range(250):
        d = day + timedelta(days=i)
        weekend = d.weekday() >= 5
        total = int(random.gauss(5200 if not weekend else 4300, 300))
        mobile_share = random.gauss(0.52 if not weekend else 0.60, 0.02)
        tablet_share = random.gauss(0.015, 0.004)
        mobile = round(total * mobile_share)
        tablet = max(0, round(total * tablet_share))
        desktop = total - mobile - tablet
        rows.append([
            d.strftime("%Y-%m-%d"), d.strftime("%a"), total, mobile, desktop, tablet,
            round(mobile / total * 100, 2), round(desktop / total * 100, 2), round(tablet / total * 100, 2),
        ])
    write("data/traffic_mobile_desktop.csv",
          ["date", "weekday", "total_sessions", "mobile_sessions", "desktop_sessions",
           "tablet_sessions", "mobile_pct", "desktop_pct", "tablet_pct"], rows)


#Спам и хам: 300 сообщений, около 15 % спама
HAM = [
    "Привет, ты сегодня будешь на паре?", "Скинь, пожалуйста, конспект по ООП",
    "Во сколько встречаемся?", "Я уже вышел, буду через 10 минут",
    "Спасибо, всё получилось!", "Как прошла лабораторная?",
    "Завтра сдаём проект, ты готов?", "Давай созвонимся вечером",
    "Купи хлеба по дороге, пожалуйста", "Ок, договорились",
    "Посмотри, я закинул файл в общий чат", "Сегодня отменили вторую пару",
    "Не могу найти ошибку в коде, поможешь?", "С днём рождения! Всего самого лучшего",
    "Я опоздаю, начинайте без меня", "Когда дедлайн по практике?",
    "Отправил отчёт на почту", "Увидимся на выходных?",
    "Кто идёт на обед?", "Сервер упал, перезапусти, пожалуйста",
    "Напомни, в какой аудитории лекция", "Хорошо, завтра обсудим",
    "Я залил изменения на гитхаб", "Спокойной ночи", "Принёс ноутбук, жду у входа",
]
SPAM_START = ["СРОЧНО!", "ВЫ ВЫИГРАЛИ!", "Акция только сегодня!", "Поздравляем!", "Внимание!", "Только для вас!"]
SPAM_BODY = [
    "Получите приз 50000 рублей, перейдите по ссылке", "Займ без отказа за 5 минут на карту",
    "Заработок на дому от 3000 рублей в день", "Скидка 90% на всё, успейте купить",
    "Ваша карта заблокирована, подтвердите данные по ссылке", "Бесплатный iPhone каждому, регистрируйтесь",
    "Криптовалюта удвоит ваш капитал за неделю", "Подпишись на канал и получи бонус 1000 рублей",
    "Вы выбраны для участия в розыгрыше автомобиля", "Кредит под 0% без справок и поручителей",
]
LINKS = ["http://bit.ly/x{}".format, "https://prize-{}.top".format, "http://get-money{}.ru".format]


def spam_text():
    t = f"{random.choice(SPAM_START)} {random.choice(SPAM_BODY)}"
    if random.random() < 0.85:
        t += " " + random.choice(LINKS)(random.randint(10, 99))
    if random.random() < 0.5:
        t += "!!"
    return t


def ham_text():
    t = random.choice(HAM)
    if random.random() < 0.15:
        t += " " + random.choice([")", "))", "!", "..."])
    return t


def spam_ham():
    rows = []
    start = datetime(2026, 9, 1, 8, 0)
    for i in range(1, 301):
        is_spam = random.random() < 0.15
        text = spam_text() if is_spam else ham_text()
        ts = start + timedelta(minutes=random.randint(0, 60 * 24 * 30))
        letters = [c for c in text if c.isalpha()]
        upper = sum(c.isupper() for c in letters) / len(letters)
        rows.append([
            i, random.randint(1, 120), random.choice(["private", "group"]),
            ts.strftime("%Y-%m-%d %H:%M"), text, "spam" if is_spam else "ham",
            len(text), len(text.split()), text.count("http"),
            sum(c.isdigit() for c in text), text.count("!"), round(upper, 3),
        ])
    rows.sort(key=lambda r: r[3])
    for n, r in enumerate(rows, 1):
        r[0] = n
    write("data/spam_ham_messages.csv",
          ["id", "sender_id", "chat_type", "timestamp", "text", "label", "text_length",
           "word_count", "links_count", "digits_count", "exclamation_count", "uppercase_ratio"], rows)


#Отключение уведомлений в группах
def muting():
    rows = []
    for uid in range(1, 251):
        age = random.choices(["16-20", "21-25", "26-35", "36-50", "51+"], [20, 35, 25, 15, 5])[0]
        platform = random.choices(["mobile", "desktop", "both"], [60, 15, 25])[0]
        groups = max(1, int(random.lognormvariate(1.9, 0.6)))
        msgs = max(1, int(random.lognormvariate(3.5, 0.8)))   # сообщений в группах в день
        # чем больше групп и сообщений, тем выше вероятность отключить уведомления
        p = min(0.95, 0.06 + 0.02 * groups + 0.0015 * msgs)
        muted = sum(random.random() < p for _ in range(groups))
        rows.append([
            uid, age, platform, random.randint(5, 900), groups, msgs, muted,
            round(muted / groups * 100, 1), str(muted > 0).lower(), str(muted == groups).lower(),
        ])
    write("data/group_notifications_muting.csv",
          ["user_id", "age_group", "platform", "registered_days", "groups_count",
           "group_msgs_per_day", "muted_groups", "muted_share_pct", "muted_any", "muted_all"], rows)


#Нагрузка на сервер
HOURLY = [0.08, 0.05, 0.04, 0.03, 0.03, 0.05, 0.12, 0.25, 0.40, 0.55, 0.65, 0.72,
          0.62, 0.66, 0.74, 0.70, 0.72, 0.85, 1.00, 0.97, 0.95, 0.85, 0.55, 0.28]


def server_load():
    rows = []
    start = datetime(2026, 11, 4, 0, 0) 
    for i in range(288):
        t = start + timedelta(minutes=5 * i)
        h = t.hour + t.minute / 60
        a, b = int(h) % 24, (int(h) + 1) % 24
        base = HOURLY[a] + (HOURLY[b] - HOURLY[a]) * (h - int(h))
        k = base * random.uniform(0.94, 1.06)
        if random.random() < 0.02:     
            k *= random.uniform(1.2, 1.5)
        users = max(1, round(300 * k))
        rpm = round(users * 6 * random.uniform(0.9, 1.1))
        cpu = round(min(98, 4 + 0.03 * rpm + random.uniform(-2, 2)), 1)
        ram = round(min(95, 35 + 0.08 * users + random.uniform(-1.5, 1.5)), 1)
        resp = round(40 + 0.05 * rpm + (rpm / 1800) ** 4 * 120 + random.uniform(-5, 5))
        errors = max(0, round((cpu - 55) * 0.4 + random.uniform(-1, 1))) if cpu > 55 else 0
        rows.append([t.strftime("%Y-%m-%d %H:%M"), users, rpm, cpu, ram, resp, errors])
    write("data/server_load.csv",
          ["timestamp", "online_users", "requests_per_min", "cpu_pct", "ram_pct",
           "response_ms", "errors_5xx"], rows)


if __name__ == "__main__":
    traffic()
    spam_ham()
    muting()
    server_load()
