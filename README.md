# Название проекта: 
## Video Hosting SkillFactory
<br>

### swagger: http://hostname/swagger/
<br>

# Требования к проекту: 
- поиск и просмотр загруженных пользователями видеороликов;
- регистрация и авторизация пользователей;
- добавление и управление видеороликами - зарегистрированными пользователями;
- связи пользователей друг с другом через чаты (ЛС и групповые);
- рассылка уведомлений по разным каналам связи.
<br>
<br>

## Основные поля сущностей в базе данных: 

### Видеоролик:
```
channel - канал к которому относится видео
title - название видео
video_file - ссылка на файл
description - описание
upload_date - дата загрузки
```

### Пользователь:
```
sub - идентификатор из Auth0
phone - номер телефона
email - email
is_banned - бан пользователя
```

### Канал:
```
user - пользователь которому принадлежит канал 
title - название канала
description - описание канала
subscribers - подписчика канала
```
### Комментарий:
```
text - текст 
user - пользователь которому принадлежит комментарий
video - видео к которому относится комментарий
create - дата публикации
```
### Подписка:
```
user - пользователь, который подписан на канал
channel - канал к которому относиться подписка
```

### Лайк:
```
user - пользователь, который оставил лайк
video - видео к которому относиться лайк
```
<br>
<br>

# Разработка схемы REST API: 
## Необходимые методы API 
### swagger: http://hostname/swagger/

<br>

### Пользователи:
- логин для Auth0
- логаут для Auth0
- получить csrf
- проверка активной сессии
- user info
- также подключить djoser, если необходимо jwt авторизация
<br>

### Видео:
- поиск видео
- список всех видео (пагинация, свежие в начале) 
- получить видео по id 
- загрузить видео
- 
- список видео из подписок (пагинация)
- удалить видео (владелец)
- редактирование мета данных видео (владелец)
- оценить видео (лайк)
- список всех комментариев на видео (свежие в начале)


### Другие:
- создать комментарии
- подписаться на канал

### Чат:
- создание комнаты между пользователями
- список постов из истории для чата по id