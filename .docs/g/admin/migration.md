## Создать новую миграцию

Перейдите в директорию `server` и создайте новую миграцию, вместо `MESSAGE` укажите собственный комментарий:

```
notilog % cd server 
server % alembic revision --autogenerate -m "MESSAGE"
```

## Применение миграции

Эта команда применит все непроизведенные миграции и создаст таблицы:

```
server % alembic upgrade head
```

После успешного выполнения миграции таблица `event` будет создана в базе данных. Вы можете это проверить через SQL клиент или инструменты работы с базой данных