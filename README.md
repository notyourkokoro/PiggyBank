# Немного о проекте
Это веб-приложения, которое позволяет создавать копилки, редактировать их, добавлять пользователей по их username, помогать копить остальным и просить помощи, чтобы помогли накопить Вам. Всё работает очень просто. Создаете копилку, копите или простите помочь, добавляя пользователя Не понравилось? Удалите копилку. Позвал кто-то, кто Вам не знаком или не хотите помогать копить? Покиньте копилку. Надоело вообще всё? Удалите учетную запись. Кстати, есть возможность добавить себе аватарку =)

# Старт работы
## Создание миграции
python manage.py makemigrations

## Проведение миграции для работы БД
python manage.py migrate

## Создание суперпользователя
python manage.py createsuperuser

## Создание дампа даты
python -Xutf8 manage.py dumpdata приложение.название модель -o имя файла.json
(Ctrl + Alt + L - для удобного отображения json-файлов)

## Загрузка дампа
python manage.py loaddata путь до файла json

## Запуск всех тестов
python manage.py test .