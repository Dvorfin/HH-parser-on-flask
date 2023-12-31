# HH-parser-on-flask

Зачастую монитория head hunter можно столкнуться с проблемой выдачи одних и тех же вакансий, помимо этого при долгом поиске мешают излишняя информация в вакансиях. Данный проект создан для упрощения поиска новых публикаций вакансий под заданный запрос с выделением только необходимой информации, таких как требования и обязанности, с сохранением полученных результатов в базу данных.

Приложение отправляет запрос через api head hunter'a с заданным запросом, сохраняет данные в БД и выводит их в веб-интерфейсе.


Проект использует следующие компоненты:
+ Flask
+ SQLAlchemy
+ requests
+ docker


Установить докер:
```sh
sudo apt install docker
```

Скопировать репозиторий:
```sh
git clone https://github.com/Dvorfin/HH-parser-on-flask
```

Создать образ:
```sh
docker build . -t <image_name>
```

Создать образ:
```sh
docker build . -t <image_name>
```

Запустить контейнер:
```sh
docker run -p 5000:5000 -v <абсолютный путь к БД parser_database.db на хосте)>:home/user/HH-pareser-on-flask/instance <image_name>
```

**Для проверки работы приложения - перейти по 127.0.0.1:5000 в браузере.**



Изображения приложения:

![image](https://github.com/Dvorfin/HH-parser-on-flask/assets/70969469/7f5e08f7-7d14-4a76-a352-18d580e6989b)


![image](https://github.com/Dvorfin/HH-parser-on-flask/assets/70969469/3770b650-d076-4a3f-8d89-07fb71e1d672)
