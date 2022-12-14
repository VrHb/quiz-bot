# Бот для проведения викторины

Бот проводит фикторину по загруженным вопросам и ответам.

## Как установить

Доступны два модуля реализации бота:

- Для VK
- Для telegram

### Настройка переменных окружения:

- Для хранения переменных окружения создаем файл .env:

```
touch .env
```

1. Токен telegram бота, получаем после регистрации [бота](https://habr.com/ru/post/262247/)

```
echo "TG_BOT_TOKEN='<токен tg бота>'" >> .env
```

2. Ключ доступа к API VK, как получить читаем [тут](https://cloud.google.com/docs/authentication/client-libraries)

```
echo "VK_BOT_TOKEN='<токен vk бота>'" >> .env
```

3. Параметры для подключения к вашей db redis, смотрим [доку](https://redis.com/redis-enterprise-cloud/overview/) 

```
echo "REDIS_DB='<адрес db>'\nREDIS_PORT='<порт db>'\nREDIS_PASSWORD='<пароль для подключения>'" >> .env
```

### Установка:

- Необходимо установить интерпретатор python версии 3.8
- Cкопировать содержимое проекта к себе в рабочую директорию
- Активировать внутри рабочей директории виртуальное окружение:

```
python -m venv [название окружения]
```

- Установить зависимости(необходимые библиотеки):

```
pip install -r requirements.txt
```

### Как пользоваться:

Скачать архив с квизами [тут](https://dvmn.org/media/modules_dist/quiz-questions.zip) или поискать с подобной стркуктурой.

- Запускаем vk бота:

```
python vk_bot.py --help
```
Бот стартует по команде <Старт>

- Запускаем telegram бота:

```
python tg_bot.py --help
```
