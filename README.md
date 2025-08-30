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
7. [Лицензия](#license)

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
reward, execute_time, is_published, owner.

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

### Сериализация<a id="habits_serialize"></a>

Реализованы следующие сериализации:
1. **HabitSerializer** - сериализация модели Habit. Предоставлен доступ ко всем полям, кроме owner.
2. **HabitInfoSerializer** - сериализация модели Habit. Предоставлен доступ к полям place, time, action, periodicity,
reward, execute_time. Используется в контроллере для отображения привычек в общем доступе.

### Задачи<a id="habits_tasks"></a>

В приложении реализованы следующие задачи:
1. **** - задача для .

! Для задачи **** в настройках установлено срабатывание каждые 2 минуты для проверки работы задачи.

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
city, phone .
2. **UserMinInfoSerializer** - сериализатор для просмотра минимальной информации о пользователе, если пользователь не
является админом. Предоставлен доступ к полям: email, first_name, city, date_joined.
3. **RegisterUserSerializer** - сериализатор для контроллера UserCreateAPIView. Используется для регистрации/создания
пользователя. Предоставлен доступ к полям: email, password.

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
1. TestCase - тесты модели . Тесты и описание:
   - *** - проверяет работу контроллера .

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

## Лицензия<a id="license"></a>

Этот проект лицензирован по [лицензии MIT](LICENSE).

##### [Оглавление](#content)