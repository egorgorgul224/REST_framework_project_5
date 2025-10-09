# Проект 5 "Трекер привычек"

---

## Оглавление

<a id="content"></a>

1. [Описание](#description)
2. [Установка и настройка проекта](#instruction)
3. [Структура проекта](#structure)
4. [Приложения](#apps)
   - [Приложение Habits](#habits_app)
     - [Модели](#habits_models) 
     - [Контроллеры и ссылки](#habits_controllers)
     - [Вспомогательные функции](#habits_services)
     - [Сериализация](#habits_serialize)
     - [Задачи](#habits_tasks)
     - [Пагинаторы](#habits_paginators)
     - [Валидаторы](#habits_validators)
     - [Кастомные команды](#habits_commands)
   - [Приложение Users](#users_app)
     - [Модели](#users_models) 
     - [Контроллеры и ссылки](#users_controllers)
     - [Сериализация](#users_serialize)
     - [Классы разрешений](#users_permissions)
     - [Кастомные команды](#users_commands)
5. [Тестирование](#tests)
6. [Запуск и тестирование проекта, документация](#launch)
7. [Запуск и тестирование с помощью Docker Compose](#docker)
8. [Запуск и тестирование с помощью Yandex Cloud](#ya_cloud)
9. [Лицензия](#license)

---

## Описание<a id="description"></a>

В проекте реализована бэкенд-часть SPA веб-приложения трекер привычек.

---

## Установка и настройка проекта<a id="instruction"></a>

1. Клонируйте репозиторий:

```
git clone https://github.com/username/project-x.git
```

2. Перейдите в директорию проекта:

```
cd ваш_проект
```

3. Установите зависимости проекта:

```
poetry install
```

4. Зайдите в файл .env.example и следуйте инструкциям из него.

---

## Структура проекта<a id="structure"></a>

```
.
├── config
│     ├── asgi.py, settings.py, urls.py, wsgi.py необходимые модули для работы приложения
├── habits - приложение на django
│ ├── migrations - папка с миграциями
│ ├── admin.py, apps.py, models.py, paginators.py, serializers.py, tests.py, urls.py, validators.py, views.py,
 tasks.py, services.py - модули для работы приложения
├── static - папка со стилями и фото
│ ├── css
│     ├── bootstrap.min.css
│ ├── images
│ ├── js
│     ├── bootstrap.bundle.min.js
├── users - приложение на django
│ ├── management
│     ├── commands - папка с командами
│         ├── createadmin - команда для создания суперпользователя(админа)
│ ├── migrations - папка с миграциями
│ ├── templates - папка с шаблонами страниц
│ ├── admin.py, apps.py, models.py, oermissions.py, serializers.py, services.py, tests.py, urls.py, views.py - модули
для работы приложения
├── .env.example - env экземпляр для доступа к закрытым данным
├── .flake8
├── .gitignore
├── manage.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

---

## Приложения<a id="apps"></a>

В проекте реализовано 2 приложения:
1. **habits**: приложение для ведения привычек.
2. **users**: приложения для создания/редактирования/просмотра и удаления пользователя.

---

## Приложение Habits <a id="habits_app"></a>

Приложение **habits** создано для создания/редактирования/удаления и ведения привычек.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="habits_models"></a>

В приложении созданы следующие модели:
- Habit - приложение с привычками. Содержит поля place, time, action, is_nice_habit, related_habit, periodicity,
reward, execute_time, is_published, owner, day_counter.

### Контроллеры и ссылки<a id="habits_controllers"></a>

1. Контроллеры модели **Habit**.
   - Контроллер HabitCreateAPIView для создания привычки.
   - Контроллер HabitListAPIView для вывода списка своих привычек.
   - Контроллер HabitPublishedListAPIView для вывода списка опубликованных в общий доступ привычек.
   - Контроллер HabitRetrieveAPIView для вывода информации о привычке.
   - Контроллер HabitUpdateAPIView для обновления информации о привычке.
   - Контроллер HabitDestroyAPIView для удаления привычки.

```
Ссылка для контроллера HabitListAPIView: адрес/habits/
Ссылка для контроллера HabitPublishedListAPIView: адрес/published/habits/
Ссылка для контроллера HabitCreateAPIView: адрес/habit/create/
Ссылка для контроллера HabitRetrieveAPIView: адрес/habit/id_урока/detail/
Ссылка для контроллера HabitDestroyAPIView: адрес/habit/id_урока/delete/
Ссылка для контроллера HabitUpdateAPIView: адрес/habit/id_урока/update/
```

### Вспомогательные функции Services<a id="habits_services"></a>

В приложении реализованы следующие вспомогательные функции:
1. **send_telegram_message** - функция отправки сообщения о выполнении привычки в чат телеграм.

### Сериализация<a id="habits_serialize"></a>

Реализованы следующие сериализации:
1. **HabitSerializer** - сериализация модели Habit. Предоставлен доступ ко всем полям, кроме owner.
2. **HabitInfoSerializer** - сериализация модели Habit. Предоставлен доступ к полям place, time, action, periodicity,
reward, execute_time. Используется в контроллере для отображения привычек в общем доступе.

### Задачи<a id="habits_tasks"></a>

В приложении реализованы следующие задачи:
1. **send_habit_message_to_telegram** - задача для получения привычек по времени и отправки оповещений по привычкам в
телеграм. Задача вызывается каждый час и оправляет привычки в период этого часа(например задача запускается в 11:00,
привычки от 11:00 до 11:59).

! Для задачи **send_habit_message_to_telegram** в настройках установлено срабатывание каждую 1 минуты для проверки
работы задачи. По логике задача вызывается 1 раз каждый час.

### Пагинаторы<a id="habits_paginators"></a>

Реализована следующие пагинаторы:
1. **HabitListPaginator** - пагинатор для вывода списка привычек. Выводит 5 элементов на страницу.

### Валидаторы<a id="habits_validators"></a>

Реализованы следующие валидаторы:
1. **NiceHabitValidator** - класс-валидатор для определения, что привычка является приятной. У такой привычки не может
быть указана связанная привычка и/или вознаграждение.
2. **RelatedHabitOrRewardValidator** - класс-валидатор для определения, что для полезной привычки можно указать
связанную приятную привычку или вознаграждение.
3. **IsNiceRelatedHabitValidator** - класс-валидатор для определения, что связанная привычка является приятной.
Запрещено для полезной привычки выбирать полезную привычку.

### Кастомные команды<a id="habits_commands"></a>

В приложении реализованы следующие команды:

---

## Приложение User <a id="users_app"></a>

Приложение **user** создано для регистрации/авторизации/редактирования/просмотра и удаления пользователя.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="users_models"></a>

В приложении созданы следующие модели:
- User - модель пользователь. Содержит поля email, city, phone, tg_chat_id..

### Контроллеры и ссылки<a id="users_controllers"></a>

1. Контроллеры модели **User**.
   - Контроллер UserCreateAPIView для регистрации/создания пользователя.
   - Контроллер UserListAPIView для вывода списка пользователей.
   - Контроллер UserRetrieveAPIView для вывода информации о пользователе.
   - Контроллер UserUpdateAPIView для обновления информации о пользователе.
   - Контроллер UserDestroyAPIView для удаления пользователя.

```
Ссылка для контроллера UserCreateAPIView: адрес/register/
Ссылка для контроллера авторизации и получения токена TokenObtainPairView: адрес/login/
Ссылка для контроллера обновления токена TokenRefreshView: адрес/token/refresh/
Ссылка для контроллера UserListAPIView: адрес/users/
Ссылка для контроллера UserRetrieveAPIView: адрес/user/id_пользователя/detail/
Ссылка для контроллера UserUpdateAPIView: адрес/user/id_пользователя/update/
Ссылка для контроллера UserDestroyAPIView: адрес/user/id_пользователя/delete/
```

### Сериализация<a id="users_serialize"></a>

Реализованы следующие сериализации:
1. **UserSerializer** - сериализатор для модели User. В Meta класс предоставлен доступ к полям: first_name, last_name,
city, phone, tg_chat_id.
2. **UserMinInfoSerializer** - сериализатор для просмотра минимальной информации о пользователе, если пользователь не
является админом. Предоставлен доступ к полям: email, first_name, city, date_joined.
3. **RegisterUserSerializer** - сериализатор для контроллера UserCreateAPIView. Используется для регистрации/создания
пользователя. Предоставлен доступ к полям: email.

### Классы разрешений<a id="users_permissions"></a>

Реализованы следующие разрешения:
1. **IsHabitOwner** - проверяет, что пользователь является создателем привычки. Если владелец - возвращает True, иначе
False.
2. **IsAccountOwner** - проверяет, что пользователь является владельцем аккаунта. Если владелец - возвращает True,
иначе False.

### Кастомные команды<a id="users_commands"></a>

В приложении реализованы следующие команды:
1. **add_payments** - команда для добавления платежей в базу данных. При вызове команды происходит удаление текущих
платежей и загрузка платежей из файла payments_fixture.json.

Команда в консоль: 
```
python manage.py add_payments
```

---

## Тестирование<a id="tests"></a>

В приложении протестировано:
1. HabitTestCase - тесты модели Habit. Тесты и описание:
   - **test_habit_create** - проверяет работу контроллера HabitCreateAPIView создания привычки. Проверяется корректный
возврат статуса 201 и количество привычек в тестовой базе данных(2).
   - **test_habit_create_with_nice_habit_error** - проверяет работу контроллера HabitCreateAPIView создания привычки с
некорректным вводом(признак приятной привычки с указанием связанной привычки и вознаграждения). Проверяется корректный
возврат статуса 400 и сообщение ошибки.
   - **test_habit_create_with_is_nice_related_habit_error** - проверяет работу контроллера HabitCreateAPIView создания
привычки с некорректным вводом(для полезной привычки можно выбрать только приятную привычку в поле related_habit).
Проверяется корректный возврат статуса 400 и сообщение ошибки.
   - **test_habit_create_with_related_reward_error** - проверяет работу контроллера HabitCreateAPIView создания
привычки с некорректным вводом(для полезной привычки можно указать только связанную привычку или вознаграждение).
Проверяется корректный возврат статуса 400 и сообщение ошибки.
   - **test_habit_retrieve** - проверяет работу контроллера HabitRetrieveAPIView получения данных о привычке.
Проверяется корректный возврат статуса 200 и места привычки.
   - **test_habit_update** - проверяет работу контроллера HabitUpdateAPIView обновления данных о привычке. Проверяется
корректный возврат статуса 200 и обновленное названия привычки..
   - **test_habit_delete** - проверяет работу контроллера HabitDestroyAPIView удаления привычки. Проверяется корректный
возврат статуса 204 и количество привычек в базе данных(0).
   - **test_habit_list** - проверяет работу контроллера HabitListAPIView вывода списка привычек. Проверяется корректный
возврат статуса 200 и список привычек с пагинацией.
   - **test_habit_published_list** - проверяет работу контроллера HabitPublishedListAPIView вывода списка
опубликованных привычек. Проверяется корректный возврат статуса 200 и список привычек с пагинацией.

2. UserTestCase - тесты для модели User. Тесты и описание:
    - **test_user_create** - проверяет работу контроллера UserCreateAPIView регистрации пользователя. Проверяется
корректный возврат статуса 201 и количество пользователей в тестовой базе данных(2).
    - **test_user_retrieve** - проверяет работу контроллера UserRetrieveAPIView получения данных о пользователе.
Проверяется корректный возврат статуса 200 и почту пользователя.
    - **test_user_update** - проверяет работу контроллера UserUpdateAPIView обновления данных о пользователе.
Проверяется корректный возврат статуса 200 и обновленное имя пользователя.
    - **test_user_delete** - проверяет работу контроллера UserDestroyAPIView удаления пользователя. Проверяется
корректный возврат статуса 204 и количество ползователей в базе данных(0).

---

## Запуск и тестирование проекта, документация<a id="launch"></a>

1. После установки и настройки проекта в консоль введите python/python3 manage.py runserver для запуска сервера.
2. Создание/редактирование/просмотр/удаление моделей проводится в Postman.
3. Для просмотра документации введите в адресной строке:
```
http://127.0.0.1:8000/swagger/ - документация в swagger
http://127.0.0.1:8000/redoc/ - документация в redoc
```
4. Для проверки работоспособности задач введите в консоли(запуск Celery Worker) вместе с запуском сервера:
```
celery -A config worker -l INFO
celery -A config worker -l INFO -P eventlet - для Windows
```
5. Для проверки работоспособности отложенных задач введите в консоли(Celery Beat) команды вместе с командой из
4 пункта и запуском сервера:
```
celery -A config beat -l INFO -S django
```

---

## Запуск и тестирование с помощью Docker Compose<a id="docker"></a>

С помощью Docker Compose можно запустить все необходимые для проекта сервисы в одной оболочке(веб-приложение, базу
данных(PostgreSQL), Redis, Celery и Celery Beat).

Запуск:
1. Установите Docker.
2. Введите команду для создания и запуска Docker Compose в фоновом режиме.
```
docker-compose up -d --build
```
3. Проверить работоспособность Docker Compose можно:
- проверить сервер по адресу:
```
http://localhost:8000/
или
http://127.0.0.1:8000/
```
- для добавления админа и входа в базу данных используйте команды:
```
создание админа:
docker-compose run web python manage.py createadmin

входа в базу данных:
docker exec -it django_rest_homework-db-1  psql -U postgres materials

проверка всех таблиц в базе данных:
\dt

пример для проверки пользователей:
SELECT * FROM users_user;
```
- ввести в терминал команду, запущенные команды будут иметь status "Up":
```
docker-compose ps
```
- ввести в терминал команду для просмотра логов по каждому сервису:
```
docker-compose logs
```
4. Для остановки и/или удаления используйте команду:
```
docker-compose stop

или с удалением контейнера:
docker-compose down
```

---

## Запуск и тестирование с помощью Yandex Cloud<a id="ya_cloud"></a>

С помощью Yandex Cloud можно запустить проект на удаленном сервере.

Для успешного развертывания на сервере необходимо:
   - Удаленный сервер с установленным Docker
   - Учетная запись Docker Hub
   - Доступ к репозиторию на GitHub

Настройка удаленного сервера:
1. Обновление системы:
```
sudo apt update
sudo apt upgrade
```

2. Установка docker и docker-compose:
```
sudo apt-get install ca-certificates curl

sudo install -m 0755 -d /etc/apt/keyrings

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

3. Активация файрвола:
```
# проверка статуса файрвола
sudo ufw status

# сли файрвол отключен, активируйте его
sudo ufw enable
```

4. Открытие необходимых портов:
```
# http port:
sudo ufw allow 80/tcp
	
# https port:
sudo ufw allow 443/tcp
	
# ssh port:
sudo ufw allow 22/tcp
```

Клонирование проекта на сервер и запуск:
1. Зайти на удаленный сервер:
```
ssh SSH_USER@$SERVER_IP
```

2. Клонируйте репозиторий:

```
git clone https://github.com/username/project-x.git
```

3. Заполнить файл env своими данными:
```
sudo nano .env
```
4. Запустить контейнер на сервере:
```
sudo docker compose -f docker-compose.prod.yml up -d --build --remove-orphans
```

Проверить работоспособность:
1.
```
http://158.160.1.109/
http://158.160.1.109/swagger/
```

---

## Лицензия<a id="license"></a>

Этот проект лицензирован по [лицензии MIT](LICENSE).

##### [Оглавление](#content)