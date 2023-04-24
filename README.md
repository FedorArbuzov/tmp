# LMS PLATONICS


## Как использовать

Чтобы использовать выполните:

```
git clone ...
cd <название вашего проекта>
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Теперь чтобы дебажить в vs code создайте файл launch.json и туда запишите

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "python": "${workspaceFolder}/env/bin/python",
            "args": [
                "runserver"
            ],
            "django": true,
            "justMyCode": true
        },
    ]
}
```


## Настройка приложения на сервере

1. Заходим по ssh на свою виртуалку по логину и паролю
2. Делаем ssh ключ чтобы делать git pull без логина и пароля
    1. В терминале запускаем `ssh-keygen`
    2. Прожимаем везде enter (без пароля и тд)
    3. делаем `cat /root/.ssh/id_rsa.pub` и то что выпало вставляем у себя в гитхабе в разделе с ключами https://github.com/settings/keys
3. Делаем `git clone` по ssh

4. Запуск django бекенда ИСПОЛЬЗОВАТЬ ТОЛЬКО НА ДЕВНОМ КОНТУРЕ ДЛЯ ДЕМО

    1. Идем в папку проекта и выполняем, сайт должен открыться
        ```
            python3 -m venv env
            source env/bin/activate
            pip install -r requirements.txt
            python manage.py runserver 0.0.0.0:8080
        ```

    2. Создаем systemd команду
        1. `cd /etc/systemd/system/`
        2. `nano server.service`
        3. Полулжить туда надо что-то вроде этого
        ```
        [Unit]
        Description=My test service
        After=multi-user.target

        [Service]
        Type=simple
        Restart=always
        ExecStart=/root/template-django/env/bin/python /root/template-django/manage.py runserver 0.0.0.0:8080

        [Install]
        WantedBy=multi-user.target
        ```
        3. `systemctl daemon-reload`
        4. `systemctl start server.service`

## Настройка s3

Вот шаги по установке Minio на Ubuntu:

1. Сначала обновите списки пакетов:

      `sudo apt update`
   

2. Скачайте бинарный файл Minio с помощью команды wget:

      `wget https://dl.min.io/server/minio/release/linux-amd64/minio`
   

3. Сделайте загруженный бинарный файл исполняемым:

      `chmod +x minio`
   

4. Переместите бинарный файл в директорию /usr/local/bin:

      `sudo mv minio /usr/local/bin/`
   

5. Создайте нового системного пользователя для запуска Minio:

      `sudo useradd -s /sbin/nologin -r minio-user`
   

6. Создайте новую директорию для данных Minio:

      `sudo mkdir /var/lib/minio`
   

7. Установите владельца директории данных на minio-user:

      `sudo chown -R minio-user:minio-user /var/lib/minio`
   

8. Создайте новый systemd-файл сервиса для Minio:

      `sudo nano /etc/systemd/system/minio.service`
   

9. Вставьте следующее содержимое в файл:

   ``` 
   Unit
   Description=MinIO
   Documentation=https://docs.min.io
   Wants=network-online.target
   After=network-online.target
   AssertFileIsExecutable=/usr/local/bin/minio

   Service
   WorkingDirectory=/var/lib/minio
   User=minio-user
   Group=minio-user
   ProtectHome=on
   ProtectSystem=full
   PrivateDevices=yes
   PrivateTmp=yes
   NoNewPrivileges=yes
   ExecStart=/usr/local/bin/minio server --address :9000 /var/lib/minio
   Restart=on-failure
   RestartSec=5

   Install
   WantedBy=multi-user.target
   ```
   

10. Сохраните и закройте файл, нажав Ctrl+X, затем Y, затем Enter.

11. Перезагрузите демона systemd:

      `sudo systemctl daemon-reload`
   

12. Включите и запустите сервис Minio:

      `sudo systemctl enable --now minio`
   

13. Откройте веб-интерфейс Minio в вашем веб-браузере, перейдя по адресу `http://SERVERIP:9000`, заменив SERVERIP на IP-адрес вашего сервера.

Вот и все! Теперь у вас установлен Minio на вашем сервере Ubuntu.`

## Настройка postgres

### Установка

Пошаговое руководство по установке PostgreSQL на Ubuntu:

1. Откройте терминальное окно на вашей машине Ubuntu.

2. Обновите список пакетов, выполнив следующую команду:

      `sudo apt-get update`
   

3. Установите PostgreSQL, выполнив следующую команду:

      `sudo apt-get install postgresql postgresql-contrib`
   

4. После завершения установки PostgreSQL должен запуститься автоматически. Вы можете проверить его статус, выполнив следующую команду:

      `systemctl status postgresql`
   

   Если PostgreSQL не запущен, вы можете запустить его, выполнив следующую команду:

      `sudo systemctl start postgresql`
   

5. PostgreSQL теперь должен быть установлен и работать на вашей машине Ubuntu. Чтобы получить доступ к интерфейсу командной строки PostgreSQL, выполните следующую команду:

      `sudo -u postgres psql`
   

   Это пустит в систему PostgreSQL под пользователем postgres.

6. Теперь вы можете создать нового пользователя и базу данных, выполнив следующие команды:
   
   ``` 
   CREATE USER myuser WITH PASSWORD 'mypassword';
   CREATE DATABASE mydatabase;
   GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
   ```

   Замените myuser и mypassword на желаемое имя пользователя и пароль, а mydatabase на желаемое имя базы данных.

Готово! Теперь у вас должен быть установлен и работающий PostgreSQL на вашей машине Ubuntu, и вы можете начать использовать его для создания своих приложений.

### Открыть на внешний контур

Чтобы запустить PostgreSQL на 0.0.0.0 и порту 5432, вам нужно изменить файлы postgresql.conf и pghba.conf. Вот шаги, которые нужно выполнить:

1. Откройте файл postgresql.conf в текстовом редакторе. Файл обычно находится в директории /etc/postgresql/<version>/main/. Замените <version> на номер версии PostgreSQL, установленной на вашей системе.

   
   sudo nano /etc/postgresql/<version>/main/postgresql.conf
   

2. Найдите строку, которая начинается с listen_addresses, и раскомментируйте ее, удалив символ # в начале строки. Затем измените значение на '', чтобы разрешить подключения с любого IP-адреса.

   
   listen_addresses = ''
   

3. Сохраните изменения и закройте файл.

4. Откройте файл pghba.conf в текстовом редакторе. Файл обычно находится в той же директории, что и файл postgresql.conf.

   
   sudo nano /etc/postgresql/<version>/main/pghba.conf
   

5. Найдите строку, которая контролирует доступ для пользователя postgres, которая должна выглядеть так:

   
   host    all             postgres        127.0.0.1/32            md5
   

6. Добавьте новую строку под ней, чтобы разрешить доступ для всех IP-адресов. Строка должна выглядеть так:

   
   host    all             postgres        0.0.0.0/0               md5
   

7. Сохраните изменения и закройте файл.

8. Перезапустите службу PostgreSQL, чтобы изменения вступили в силу.

   
   sudo systemctl restart postgresql
   

Теперь PostgreSQL должен слушать все сетевые интерфейсы, включая 0.0.0.0, и порт 5432. Вы можете проверить подключение, подключившись к базе данных с помощью клиента PostgreSQL с другой машины в сети.

