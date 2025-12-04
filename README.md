Используемые технологии:
Python 3.13
FastAPI – для создания REST API
SQLModel – ORM для работы с PostgreSQL
PostgreSQL – СУБД
DBeaver – для создания таблиц и проверки данных
Psycopg2 – драйвер для подключения Python к PostgreSQL

Настройка и запуск
Установить Python и необходимые библиотеки:

pip install fastapi sqlmodel psycopg2 uvicorn

Наполнить базу минимальными данными:

python seed.py

Запустить FastAPI приложение:

uvicorn main:app --reload

Открыть документацию API:

http://127.0.0.1:8000/docs

Основные маршруты API:

/guests – получить всех гостей
/rooms/free – получить свободные номера
/booking/create – создать бронирование
/checkin – регистрация заезда
/checkout – регистрация выезда
/service/add – добавить услугу к счету
/staff – список сотрудников
/schedule/add – добавить смену сотруднику