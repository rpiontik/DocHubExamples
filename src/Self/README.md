# Минимальный базовый пример описания самого репозитория примеров

**Цель примера:** Показать минимально работающую структуру описания архитектуры

# Суть примера

* Необходимо показать архитектуру самого репозитория примеров, при попмощи архитектуры как код

## Логическое описание реализации и файловая структура примера

Содержит только 2 файла

* [root.yaml](root.yaml) - главный файл описывающий пользователя репозитория примеров, один компонент, один аспект и одну технологию и один документ
* [WELCOME.md](WELCOME.md) - главная страница (index.html) архитектуры - содержит пример ссылки на общее описание

## Использование

* вариант 1: запустить визуализацию с помощью плагинов IDEA или VSCode/VSCodium
* вариант 2: запустите сервис через команду Docker `docker run --rm -p 48080:8080 -v ./src/Self:/usr/share/nginx/html/documentation ghcr.io/rabotaru/dochub:v2.6.2` - откройте адрес http://localhost:48080 для ознакомления

## Задания для практики

* запустите команду в Linux `docker run --rm -p 48080:8080 -v ./dochub.yaml:/usr/share/nginx/html/documentation/root.yaml -v ./:/usr/share/nginx/html/documentation ghcr.io/rabotaru/dochub:v2.6.2` 
* расскоментируйте ВСЕ примеры в файле [главного импорта в корне репозитория (dochub.yaml)](../../dochub.yaml)