# Daily Horoscopes Bot 

ТЗ: Необходимо создать telegram-бота, чтобы была возможность получить актуальный гороскоп по каждому из знаков зодиака на сегодня.

**Остобенности**
- Приложение в Docker-контейнере
- Использование aiogram  

## Архитектура

## Реализация

Команды для дебага: 

```bash
docker logs astro_bot
docker ps -a | grep bot
docker rm -f astro_bot
```

```bash
docker images | grep bot
docker rmi astrolog_bot
```

```bash
docker build -t astrolog_bot .
docker run --name astro_bot -d astrolog_bot
```

Пересобрать образ и запустить контейнер: 
```bash
docker rm -f astro_bot
docker rmi astrolog_bot
docker build -t astrolog_bot .
docker run --name astro_bot -d astrolog_bot
docker logs -f astro_bot
```