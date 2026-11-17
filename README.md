# Notes API

Учебное HTTP-приложение для практической работы № 5. Хранит заметки в JSON-файле именованного Docker-тома.

## Запуск

```bash
cp env.example .env
docker compose up -d --build
docker compose ps
```

Проверка:

```bash
curl http://localhost:8201/health
curl -X POST http://localhost:8201/notes -H "Content-Type: application/json" -d '{"text":"Первая запись"}'
curl http://localhost:8201/notes
```

Остановка: `docker compose down`. Для сохранности данных не добавляйте флаг `-v`.

## Тесты

```bash
python -m unittest discover -v
```

Конфигурация задаётся через переменные `PORT` и `DATA_FILE`. Секреты приложению не требуются.
