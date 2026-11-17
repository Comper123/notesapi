# Runbook развёртывания и отката

## Предусловия

Docker и Compose v2 установлены; порт 8201 свободен; в каталоге есть `.env`, созданный из `env.example`.

## Развёртывание

```bash
git status
python -m unittest discover -v
docker compose config
docker compose build
docker compose up -d
docker compose ps
curl -f http://localhost:8201/health
docker stats --no-stream
```

Контрольная точка: контейнер `healthy`, `/health` возвращает 200. При ошибке остановить процедуру и изучить `docker compose logs --tail=100`.

## Резервная копия и восстановление

```bash
mkdir -p backup
docker run --rm -v notes-api-data:/data -v "$PWD/backup:/backup" alpine tar czf /backup/notes-data.tgz -C /data .
mkdir -p backup/restore-check
tar xzf backup/notes-data.tgz -C backup/restore-check
```

## Откат

```bash
docker compose down
git checkout v0.9.0
docker compose up -d --build
curl -f http://localhost:8201/health
curl -f http://localhost:8201/notes
```

Именованный том не удаляется, поэтому данные сохраняются. Не использовать `docker compose down -v`.

## Безопасное моделирование отказа

```bash
docker compose exec -T notes-api kill -9 1
sleep 7
docker compose ps
curl -f http://localhost:8201/health
curl -f http://localhost:8201/notes
```

Аварийное завершение главного процесса проверяет политику перезапуска. Явная команда `docker stop` не подходит: Docker считает её намеренной остановкой администратора.
