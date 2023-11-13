# Тестовое задание Elefanto


## Запуск



```bash
docker-compose up --build
```
или
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
проект запустится на localhost:8000

## Документация и админ-панель
###
Вход в админ-панель: http://localhost:8000/api/admin
логин: admin
пароль: admin
Документация: http://localhost:8000/api/swagger
###
БД вместе с тестовыми данными также лежат в репозитории.
Также необходимо добавить почту-отправитель в settings.py
###
EMAIL_HOST, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_HOST_PASSWORD