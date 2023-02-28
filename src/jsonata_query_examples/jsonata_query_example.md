# Примеры запросов JSONata

Описание языка JSONata можно найти на [официальном сайте](https://docs.jsonata.org/overview). Также на этом сайте вы можете попробовать [сделать свои запросы](https://try.jsonata.org/).

## Как отфильтровать данные в запросе

### Как отфильтровать данные по ключу

Задача:
Требуется получить все системы одного бизнес-юнита "crocodile", т.е. задача сводится к тому, что нужно получить все системы у которых ключ массива содержит значение "swamp.crocodile".

Пример данных:
```yaml
components:
  swamp.crocodile.sid:
    title: S.ID    # Название компоненты
    entity: system   # Сущность компонента из PlantUML (https://plantuml.com/ru/deployment-diagram)    
    system_status: production
    short_description: Общекорпоративный сервис SSO (Single Sign-On)
    description: Сервис SSO (Single Sign-On). Реализована возможность авторизации через OAuth 2 и OpenID Connect.
    business_owners:
      - Крокодил Гена
      - Шапокляк
    application_owner: Чебурашка
    budget_holder: Малыш
    architect: Карлсон
    critical_level: business_critical #administrative/business_operational/business_critical/mission_critical
    system_category: business_app #channel_app/business_app/ext_business_app/it_app/ext_it_app    
    technologies:  # Используемые технологии
      - Django
      - Python
      - Faust
      - PostgreSQL
      - Redis
      - Kafka
      - Nginx

```

Варианты решения:

#### Вариант 1

Для того чтобы отфильтровать данные по ключу можно использовать функцию $sift(). Данная функция позволяет по дефолту фильтровать данные по ключу. Описание функции можно найти [здесь](https://docs.jsonata.org/higher-order-functions#sift).

При этом в работе функции есть нюансы:
1. Если у вас статический параметр фильтрации, то вы можете в функцию просто передать параметр жестко указав его в функции или через переменную.

```
(
    $matcher := /swamp\.crocodile\..*/; /*Задаем параметр фильтрации запроса*/
	components.$sift(function($v, $k) {$k ~> $matcher}).$spread().
        {"id": $keys()[0],"component": $.*}
)
```
2. Если у вас динамический параметр фильтрации, то предыдущий вариант работать не будет и нужно преобразовать параметр через функцию $eval().

```
(
	$bu_id := $params.id; /*Так должно быть в оригинале*/
	$bu_id := "crocodile"; /*Для теста перебиваем значение*/
	$pattern := $eval("/swamp\\." & $bu_id & "\\..*/");
	components.$sift(function($v, $k) {$k ~> $pattern}).$spread().
        {"id": $keys()[0],"component": $.*}
)
```

#### Вариант 2

Можно использовать второй вариант, который более универсальный. Он позволяет фильтроваться по любому полю и если мы хотим фильтроваться по ключу, то для этого нам нужно ключ добавить внутрь массива, а затем уже фильтроваться по этому полю. 

```
(
    /*Формируем строку поиска через регулярное выражение*/
	$matcher := /swamp\.crocodile\..*/;
    /*Выбираем все системы*/
	components.$spread(). /*$spread() используется в том случае, если мы хотим получть ключ через функцию $keys()[0]. Если не ходим, то $spread() можно не использовать*/
        {"id": $keys()[0], /*Помещаем ключ внутрь запроса*/
        "component": $.*
        }[$matcher(id)] /*Фильтруемся по ключу*/
)
```

#### Отличия первого и второго вариантов

Если у вас есть массив данных, который просто нужно отфильтровать, то проще всего использовать вариант 2. Если же у вас многослойная последовательная выборка, то вариант 2 вам может не подойти и тогда используйте вариант 1.


### Как отфильтровать данные по значению внутри массива

Иногда требуется отфильтровать данные по значению какого либо поля внутри массива. Например, в нашем примере мы ходим выбрать все критичные для бизнеса системы. В нашем случае мы хотим выбрать все системы где:
`critical_level: business_critical`.

В данном случае тоже существует два способа:

#### Вариант 1

Для того чтобы отфильтровать данные по значению можно использовать функцию $filter(). Данная функция позволяет  фильтровать данные по значению любого поля в массиве. Описание функции можно найти [здесь](https://docs.jsonata.org/higher-order-functions#filter).

```
(
	$level := "business_critical";
	components.$filter($.*, function($v, $i, $a) {$contains($v."critical_level", $level)}).(
	$
	);
)
```

#### Вариант 2

Это способ мы описали выше ["Как отфильтровать данные по ключу - Вариант 2"](#вариант-2).

```
(
    /*Формируем строку поиска через регулярное выражение*/
	$matcher := /business_critical/;
    /*Выбираем все системы*/
	components.(	
        	$.*
        )[$matcher(critical_level)] /*Фильтруемся по полю critical_level*/
)
```
#### Отличия первого и второго вариантов

Если у вас есть массив данных, который просто нужно отфильтровать, то проще всего использовать вариант 2. Если же у вас многослойная последовательная выборка, то вариант 2 вам может не подойти и тогда используйте вариант 1.


## Как получить список систем/сервисов с кастомным списком полей

Задача:
Требуется получить все системы/сервисы уровня ПА-L1. Конечный массив данных, должен соответствовать выводимой таблице. В списке должна быть ссылка на карточку системы. Также конечный список данных хотим отсортировать по идентификатору системы.
```
(
	$level := "business_critical";
	components.$filter($.*, function($v, $i, $a) {$contains($v."critical_level", $level)}).(
	$
	);
)
```

Контекст:
Уровень ПА-L1 (общая прикладная архитектура) описывается системами/сервисами с entity="system", поэтому в качестве условия выборки должно быть данное условие.

Варианты решения:

```
(
	$distinct([components.$spread().(
	$COMPONENT_ID := $keys()[0];
	$systems := $.*.{
        "id": $COMPONENT_ID,
        "link_to_system": "/architect/components/" & $COMPONENT_ID,
        "title": title,
        "entity": entity,
        "description": description,
        "owner": owner
         };
	$systems[entity="system"]; /*Устанавливаем фильтр*/
      )])^(id) /*Сортируем по полю id*/
)
```

## Как выбрать технологии использующиеся в системах

Задача:
Требуется получить список технологий использующихся в системах. Технологии не должны дублироваться.

Контекст:
Пример интересен тем, что внутри запроса показана проверки данных и подмены их дефолтными значениями. Также есть хитрый способ исключения дублирования данных.

Варианты решения:

```
(
    $MANIFEST := $;
    $distinct($distinct(components.*.technologies).(
        $TECHKEY := $;
        $TECHNOLOGY := $lookup($MANIFEST.technologies.items, $type($)="string" ? $ : undefined);
        $TECHNOLOGY := $TECHNOLOGY ? $merge([$TECHNOLOGY, {"id": $TECHKEY}]) : $single(
            $spread(
                $sift($MANIFEST.technologies.items, function($v, $k) {
                    [$TECHKEY in $v.aliases]}
                )
            ), function($v, $k){ $k=0 }).$merge([$.*, {"id": $keys($)}]);
        $TECHNOLOGY := $TECHNOLOGY ? $TECHNOLOGY : {
            "id": $TECHKEY,
            "section": "UNKNOWN",
            "title": "Не определено"
        };
        $SECTION := $lookup($MANIFEST.technologies.sections, $TECHNOLOGY.section);
        {
            "label": $TECHNOLOGY.id,
            "key": $TECHNOLOGY.id,
            "hint": $TECHNOLOGY.title,
            "link": $TECHNOLOGY.link,
            "status": $TECHNOLOGY.status,
            "section" : {
                "key": $TECHNOLOGY.section,
                "title": $SECTION.title ? $SECTION.title : "Не определено"
            }
        }
    ))
)
```
## Как получить уникальные логины всех сотрудников

Задача:
Был написан REST API, который выдает всю информацию по учетным записям пользователей в формате yaml. Так как учетных записей более 6000 тысяч, а реально в DocHub мы используем менее 30, то встала задача выбрать все используемые учетные записи. Так как в самих полях сейчас бардак - кто-то указывает логины, а кто-то просто ФИО, поэтому нужно выбрать только логины и убрать все лишнее.

Контекст:
Пример системы:
```yaml
components:
  swamp.crocodile.spact:
    title: S.Pact    # Название компонента
    entity: system   # Сущность компонента из PlantUML (https://plantuml.com/ru/deployment-diagram)    
    short_description: Сервис для создания и подписания договоров
    description: Сервис для создания и подписания договоров
    business_owners:
      - vupsen
      - Пупсень
    application_owner: k.korneech  
    budget_holder: valentin  
    critical_level: business_critical #administrative/business_operational/business_critical/mission_critical
    system_category: business_app #channel_app/business_app/ext_business_app/it_app/ext_it_app          
    links:
      # Интеграции между системами одного БЮ
      - id: swamp.frog.1cbit_finance
        direction: <--      

```
Выбирать будем business_owners, application_owner и budget_holder.

Варианты решения:

**Вариант 1**
```
(
    $_manifest := $;
    /* Делаем регулярку на выбор только латинских букв */
    $matcher := /^[a-z]/;
    /* Создаем массив со списком имен полей из которых будем выбирать логины */
    $scan_fields := ["budget_holder", "application_owner", "business_owners"];
    /* Выбираем системы */
    $system_accounts := $distinct($_manifest.components.*.(
        $component := $; /* Получаем конкретную систему*/        
        $scan_fields.(
            $lookup($component, $); /* Внутри конкретной системы берем значение конкретного реквизиты для каждого поля указанного в $scan_fields*/
        )[$matcher($)]; /*Каждое полученное значение свяряем с регуляркой и лишнее игнорируем*/
    ))[$];/*В предыдущей выборке будут nill-ы, для того чтобы избавиться от них делаем фильтр*/

    /* Повторяем предыдущий алгоритм для версий архитектуры */
    $arch_versions_accounts := $distinct($_manifest.arch_versions.*.сhanged_data.*.(
        $component := $;
        $scan_fields.(
            $lookup($component, $);
        )[$matcher($)];
    ))[$];

    /*Соединяем два полученных выше массива*/
    $all_accounts := $distinct($append($system_accounts, $arch_versions_accounts )); 
)
```
**Вариант 2**
Ниже описан более простой вариант реализации задачи. С одной стороны вариант более понятный и линейный, с другой менее масштабируемый, но полезно ознакомиться с разными подходами получения одного и того же результата.
```
(
    $_manifest := $;
    $arch_version := $_manifest.arch_versions; 
    $components := $_manifest.components; 

    $pattern := $eval("/^[a-z]/");
    $sys_accounts := $distinct($components.*.(
        $account := $append($account, budget_holder);
        $account := $append($account, application_owner);
        $account := $append($account, $.business_owners);
    ));

    $arch_versions_accounts := $distinct($arch_version.*.сhanged_data.*.(
        budget_holder;
    ));
    $all_accounts := $append($sys_accounts, $sys_accounts); 

    $accounts := $distinct($all_accounts.(
        $contains($, $pattern) = true
        ?  $append($account, $); 
    ));
)
```
## Как переиспользовать код

В классическом понимании, функции в JSONata работают только внутри одного алгоритма, т.е. если вам нужно внутри одного алгоритма переиспользовать какой-то кусок кода, то вы можете выделить его в функцию. При этом нет такого понятия как объявить глобальную функцию и использовать её везде где нам нужно. Детально об использовании функций можно почитать в документации по JSONata в разделе ["Функциональное программирование"](http://docs.jsonata.org/programming).

Что же делать если нам нужно переиспользовать один кусок кода для разных алгоритмов?
Есть альтернативное решение - это объявить переиспользуемый кусок кода и импортировать его в общее хранилище данных DocHub. После этого вы сможете выполнять описанный кусок вашего кода через специальную функцию $eval(), при этом функция $eval(expr [, context]) в качестве второго параметра может принимать контекст, что по факту можно использовать как параметры функции.

Так как  не специалист в JSONata, то моё объяснение может кому-то показаться колхозным, поэтому если у вас есть более правильное объяснение, то делайте MR.

Давайте рассмотрим пример:
1. Создадим yaml файл где у нас будут храниться куски кода, которые мы хотим переиспользовать в разных алгоритмах. Например, у нас этот файл хранится по следующему пути: `./functions.yaml`
2. Объявим и опишем код
```yaml
functions:
  get_resources: >
    (
      $context := $.context;
      $mult := $.mult;
      $output_type := $.output_type;
      $output_type = "short"
      ? "RAM: " & $context.ram * $mult & "Gb" & "\n"            
        & "CPU: " & $context.cpu * $mult & "Core" & "\n"        
        & ($context.storage_size > 0
        ? "Storage: " & $context.storage_size * $mult & "Gb")
      : "RAM: " & $context.ram * $mult & "Gb" & "\n"
        & "CPU type: " & $context.cpu_type & "\n"
        & "CPU: " & $context.cpu * $mult & "Core" & "\n"
        & ($context.storage_size > 0 
          ? "Storage type: " & $context.storage_type & "\n"
          & "Storage: " & $context.storage_size * $mult & "Gb" : "")
    )
```
3. Вызовем кусок нашего кода с разными параметрами в редакторе JSONata
```yaml
(
    $functions := functions;
    $eval($functions.get_resources,{"context": {"ram": 2, "cpu": 8, "storage_size": 5}, "mult": 4, "output_type": "short"});
    $eval($functions.get_resources,{"context": {"ram": 2, "cpu_type": "standart", "cpu": 8, "storage_type": "standart", "storage_size": 5}, "mult": 1, "output_type": "full"});
)
  ```
Также нужно учитывать, что блок кода описанный выше работает только с переданным контекстом и если вам нужно будет получить что-то типа `$.components`, то это нужно делать при помощи переданных параметров `$components := $.components`.