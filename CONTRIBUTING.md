# Разработка сервиса

## Рабочее окружение
Для начала разработки необходимо настроить рабочее окружение. Нам понадобятся следующие системные зависимости:
- [python](https://www.python.org/downloads/) версии >= 3.9.9

### Установить poetry
В проекте используется poetry версии 1.7.0

```env
# Адрес сервиса
SERVICE_HOST=localhost #хост основного сервиса
SERVICE_PORT=24718 #порт основного сервиса

# Переменные базы данных
DB_USER=shedko # пользователь базы данных
DB_PASS=postgres # пароль базы данных
DB_NAME=effective_warehouse # имя базы данных
DB_HOST=localhost # сервис (контейнер) базы данных
DB_PORT=5432 # порт для подключения базы данных
```

Настройка окружения:
1. Настроить репозиторий
    ```shell script
    git clone https://github.com/ShedkoV/effectivemobile.git
    cd effectivemobile
    ```
2. Установить зависимости. Зависимости установятся в виртуальное окружение.
    ```shell script
    poetry install -E lint -E tests

## Описание переменных окружения, используемых в приложении

3. ### Определение переменных окружения

Создаем файл с переменными окружения по [образцу](.envexample)
```shell
touch .env
```
```shell
cat << EOF > .env
SERVICE_HOST=localhost
SERVICE_PORT=8000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=effective_warehouse
DB_USER=shedko
DB_PASS=postgres
EOF
```
```
export PYTHONPATH="$PWD/src"
```

## Локальный запуск сервиса
```sh
cd src
alembic upgrade head
```

Из корневой директории запустить скрипт:
```shell script
chmod a+x ./*.sh
./start.sh
```

Запуск линтера:
```shell script
flake8 --config=setup.cfg src
```

Запуск mypy
```shell script
mypy --config-file setup.cfg
```

Развернуть сервис:
```powershell
docker compose -f src/tools/docker-compose.yaml up -d
```


