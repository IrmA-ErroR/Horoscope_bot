# Daily Horoscopes Bot 

ТЗ: Необходимо создать telegram-бота, чтобы была возможность получить актуальный гороскоп по каждому из знаков зодиака на сегодня.

**Остобенности**
- Приложение в Docker-контейнере
- Использование aiogram  

## Архитектура

## Реализация

#### Команды для дебага: 
Собрать образ из текущей директории, собрать и запустить контейнер
```bash
docker build -t astrolog_bot .
docker run --name astro_bot -d astrolog_bot
```
<br><br>Если что-то не так:

1. Проверить запущен ли контейнер, посмотреть логи
```bash
docker ps | grep astro_bot
docker logs astro_bot
```

2. Проверить наличие образа:
```bash
docker images | grep astrolog_bot
```

3. Пересобрать образ и запустить контейнер: 

*(сразу смотреть логи)*
```bash
docker rm -f astro_bot
docker rmi astrolog_bot
docker build -t astrolog_bot .
docker run --name astro_bot -d astrolog_bot
docker logs -f astro_bot
```