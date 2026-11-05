# Простейший мессенджер на Flask

Простейший веб-мессенджер на Flask: пользователи, чаты, личные и групповые сообщения.

> Университетский проект по Python (ООП). Тема: «Разработка простейшего мессенджера на Flask».

## Данные

Для проекта подготовлено пять наборов данных. Четыре собраны из открытых источников, один сгенерирован скриптом. Все файлы лежат в `data/`.

| Файл | Тип | Строк | Содержание |
|---|---|---|---|
| `traffic_mobile_desktop.csv` | собранные | 7 | доля мобильного и десктопного трафика |
| `sms_spam_ham_summary.csv` | собранные | 3 | спам и хам: итоговые доли |
| `sms_spam_ham_sources.csv` | собранные | 5 | спам и хам: корпуса, из которых собран датасет |
| `group_notifications_muting.csv` | собранные | 15 | пользователи, отключающие уведомления в группах |
| `server_load_hourly.csv` | сгенерированные | 168 | нагрузка на сервер по часам за неделю |

### Мобильный и десктопный трафик

Файл `traffic_mobile_desktop.csv`. Колонки: `period`, `region`, `mobile_pct`, `desktop_pct`, `tablet_pct`, `console_pct`, `source`.

| Период | Регион | Mobile, % | Desktop, % | Tablet, % | Console, % |
|---|---|---|---|---|---|
| 2026-04 | World | 52.80 | 45.61 | 1.59 | — |
| 2026-06 | World | 51.45 | 47.15 | 1.36 | 0.03 |
| 2026-08 | World | 49.34 | 49.09 | 1.54 | 0.03 |
| 2026-09 | North America | 50.49 | 49.51 | — | — |
| 2026-01 | USA | 43.00 | 57.00 | — | — |
| 2026-01 | China | 33.21 | 66.79 | — | — |
| 2026-01 | Sudan | 72.05 | 27.95 | — | — |

Это доля трафика всего веба, а не только мессенджеров. Для North America источник сравнивает только mobile и desktop.

### Спам и хам

Файлы `sms_spam_ham_summary.csv` и `sms_spam_ham_sources.csv`. Датасет SMS Spam Collection: 5 574 англоязычных SMS, размеченных как `ham` (нормальное сообщение) или `spam`.

| Класс | Сообщений | Доля, % |
|---|---|---|
| ham | 4 827 | 86.60 |
| spam | 747 | 13.40 |
| Всего | 5 574 | 100 |

| Источник | Класс | Сообщений |
|---|---|---|
| Grumbletext Forum | spam | 425 |
| SMS Spam Corpus v0.1 Big | spam | 322 |
| NUS SMS Corpus | ham | 3 375 |
| Caroline Tag PhD thesis | ham | 450 |
| SMS Spam Corpus v0.1 Big | ham | 1 002 |

Доли посчитаны как сумма по корпусам из описания датасета. Файл с текстами сообщений скачивается по ссылке из раздела «Источники» и кладётся в `data/`.

### Отключение уведомлений в группах

Файл `group_notifications_muting.csv`. Колонки: `country`, `year`, `sample`, `metric`, `value_pct`, `source`.

| Страна | Показатель | Значение, % |
|---|---|---|
| USA | участвовали хотя бы в одном групповом чате | 99.5 |
| USA | заглушали надоедливый групповой чат | 75 |
| USA | перегружены групповыми чатами | 66 |
| USA | раздражаются, но не меняют настройки | 34 |
| USA | отключают уведомления группы сразу после добавления (1 из 6) | 16.7 |
| USA | отключают уведомления группы позже (1 из 4) | 25 |
| Ireland | состоят хотя бы в одном групповом чате | 96 |
| Ireland | заглушили хотя бы одну группу | 79 |
| Ireland | заглушили семейную группу | 38 |
| Ireland | заглушили группу друзей | 38 |
| Ireland | заглушили рабочую группу | 24 |
| Ireland | заглушили спортивную группу | 16 |
| не указана (2018) | хотели бы выйти из группы, но используют mute | 40 |
| не указана (2018) | состоят хотя бы в одной группе | 93 |
| USA/UK (2023) | перегружены сообщениями и уведомлениями | 40 |

Это данные разных опросов с разной методикой и выборкой. Для Ireland проценты по типам групп считаются среди тех, кто состоит в группах.

### Нагрузка на сервер по времени суток

Файл `server_load_hourly.csv`. Колонки: `day`, `hour`, `online_users`, `requests_per_min`, `cpu_pct`, `response_ms`.

Данные синтетические: публичных почасовых измерений нагрузки мессенджеров найти не удалось, поэтому значения сгенерированы скриптом `generate_server_load.py`. Форма суточной кривой откалибрована по открытым источникам: вечерний пик Messenger около 18:00 (Nielsen) и рабочие пики около 11:00 и 14:00 с провалом на обеде (Slack Engineering).

Параметры модели: 1 000 зарегистрированных пользователей, до 300 одновременно онлайн, 6 запросов в минуту на активного пользователя, выходные на 8 % ниже, случайный шум, `seed=42`.

| Час | Онлайн, чел. (будни, без шума) |
|---|---|
| 03:00 | 9 |
| 08:00 | 120 |
| 12:00 | 186 |
| 18:00 | 300 |
| 23:00 | 84 |

### Запуск генерации

```
python generate_server_load.py   # создаёт data/server_load_hourly.csv
```

## Структура репозитория

```
.
├── data/
│   ├── traffic_mobile_desktop.csv
│   ├── sms_spam_ham_summary.csv
│   ├── sms_spam_ham_sources.csv
│   ├── group_notifications_muting.csv
│   └── server_load_hourly.csv
├── generate_server_load.py     # генерация нагрузки на сервер
└── README.md
```

## Источники

Мобильный и десктопный трафик:
- [StatCounter: Website vs Traffic Market Share](https://gs.statcounter.com/platform-market-share/website-traffic/worldwide)
- [StatCounter: Web Market Share](https://gs.statcounter.com/platform-market-share/web/worldwide)
- [StatCounter: Mobile vs Desktop, North America](https://gs.statcounter.com/platform-market-share/mobile-vs-desktop/north-america)
- [SQ Magazine: Web Design Statistics 2026](https://sqmagazine.co.uk/web-design-statistics.md)
- [Digital Silk: Mobile vs Desktop Traffic Share 2026](https://www.digitalsilk.com/?p=6030)

Спам и хам:
- [UCI: SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)
- [Hugging Face: sms_spam](https://huggingface.co/datasets/sms_spam/blob/main/README.md)
- [UFSCar: состав корпуса](https://lasid.dcomp.ufscar.br/sms-spam-collection/)
- Almeida T.A., Gómez Hidalgo J.M., Yamakami A. Contributions to the Study of SMS Spam Filtering: New Collection and Results. ACM DocEng, 2011.

Уведомления в группах:
- [Secure Data Recovery: Group Messaging Feels Like a Part Time Job](https://www.securedatarecovery.com/blog/group-messaging-feels-like-job)
- [Pure Telecom: Connected Lives](https://irishtechnews.ie/pure-telecom-survey-reveals-38-percent-of-adults/)
- [Brit + Co: опрос Viber](https://www.brit.co/muting-the-group-text)
- [The Star: WhatsApp etiquette](https://www.the-star.co.ke/news/2018-10-20-whatsapp-etiquettethe-dos-and-donts-of-messaging/)
- [The Conversation: Overwhelmed by group chat messages](https://phys.org/news/2023-11-overwhelmed-group-chat-messages-youre.html)

Калибровка модели нагрузки:
- [MarketingCharts: Nielsen, пиковые часы приложений](https://www.marketingcharts.com/digital-65149)
- [Slack Engineering: Real Time Messaging](https://slack.engineering/real-time-messaging)
