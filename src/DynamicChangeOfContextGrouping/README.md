## Пример изменения группировки компонент в представлении контекста

### Цели примера
- Расширение возможности стандартного представления контекстов, которое формируется по умолчанию на основании ID компонента в формате DDD, за счет группировки по произвольным атрибутам описания компонента, например, по статусу жизненного цикла или уровню критичности приложения/сервиса, БЕЗ необходимости вручную вносить изменения в структуру описания компонентов. В целом, идея приблизиться к возможностям отчетов внутри 1С приложений, предоставляющих возможность «на лету» менять группировки отчетов.
- Использование конструкции `... ~> | ... | ... | (Transform)` (http://docs.jsonata.org/other-operators) для демонстрации преобразования данных проекта
 
### Чего нет в примере
- [Валидации](https://dochub.info/docs/dochub.rules) корректности и полноты заполнения озера данных проекта (архитектуры);

### Файловая структура примера

```
|- Datalake                                   - Озеро данных проекта (архитектуры)
|  |- Applications                            - Озеро данных "Архитектуры приложений/сервисов"
|  |  |- systems.yaml                         - Описание приложений/сервисов
|  |  |- components.yaml                      - Определение структуры Организации, Приложений/Сервисов, Функциональных контуров
|  |- Templates                               - Шаблоны контекстов
|  |  |- DefaultView.md                       - Стандартное представление контекста
|  |  |- GroupingByStatus.md                  - Группировка приложений/сервисов по статусу
|  |  |- GroupingByStatusCriticalLevel.md     - Группировка приложений/сервисов по уроню критичности
|  |- contexts.yaml                           - Контексты
|  |- docs.yaml                               - Документы
|- Imgs                                       - Изображения для README.md
|- Metamodel                                  - Метамодель проекта (архитектуры), определяющая объекты, их наполнение и зависимости
|  |- Applications                            - Метамодель "Архитектуры приложений/сервисов"
|  |- Dictionaries                            - Справочники, используемые как при описании атрибутов приложений/сервисов, так и атрибутов для группировки
|  |  |- applications_status.yaml             - Справочник статусов 
|  |  |- critical_level.yaml                  - Справочник уровней критичности
|  |- Dochub                                  
|  |  |- plantuml.yaml                        - Код движка Dochub для формирования представлений. Изменения промаркировны /* +++ДОБАВЛЕНИЕ+++ */ /* ---ДОБАВЛЕНИЕ--- */
|  |- functions.yaml                          - Функция трансформации данных $  
|- README.md                                  - Описание репозитория
```
### Примеры

#### Список систем и сервисов
![ListOfInformationSystems.png](Imgs%2FListOfInformationSystems.png)

#### Стандартное представление
![Default.svg](Imgs%2FDefault.svg)

#### Группировка по статусу приложения
![GroupingByStatus.svg](Imgs%2FGroupingByStatus.svg)

#### Группировка по уровню критичности
![GroupingByStatusCriticalLevel.svg](Imgs%2FGroupingByStatusCriticalLevel.svg)

#### Отображение списка выбор и цветовая подсветка в стандартной карточке компонента
![ChoosingAaOptionInContext.png](Imgs%2FChoosingAaOptionInContext.png)

# Пример добавления новой группировки

- Добавить новую сущность вида "dictionaries", например, создав новый файл `\Metamodel\Dictionaries\development_model.yaml`:
```
dictionaries:

  DevelopmentModel:
    title: Модель разработки
    description: Модель разработки определяет каким образом система создается/развивается - собственными силами либо силами подрядчика во внутреннем контуре разработки Компании, либо за пределами контура
    parameters:
      - name: inhouse                  # Ключ, указываемый при описании приложения/сервиса + используется при формировании ID приложения при группировке
        title: Внутренняя разработка   # Отображение в отчетах, в группировках контекста
      - name: external                 # Ключ, указываемый при описании приложения/сервиса + используется при формировании ID приложения при группировке
        title: Внешняя разработка      # Отображение в отчетах, в группировках контекста
      - name: none                     # Ключ, указываемый при описании приложения/сервиса + используется при формировании ID приложения при группировке
        title: Разработка не ведется   # Отображение в отчетах, в группировках контекста   
```
- Если изменение выполнено через отдельный файл `development_model.yaml`, то необходимо добавить в файл `\Metamodel\Dictionaries\root.yaml` ссылку на добавленный файл, должно получится следующим образом:
```
imports:
  ...
  - development_model.yaml
  ...
```
- Для каждого приложения/сервиса, указанного в файле `\Datalake\Applications\systems.yaml`, добавить новое поле `development_model`, значения поля необходимо заполнять значениями ранее добавленного справочника `DevelopmentModel` из свойсва `name`:
```
  Romashka.Systems.FinancialManagement.CPM:
    title: 1С:Управление холдингом 8
    ...
    extension:
      ...
      development_model: none
      ...

  Romashka.Systems.FinancialManagement.ERP:
    title: 1С:ERP Управление предприятием
    ...
    extension:
      ...
      development_model: inhouse
      ...
```
- Добавить новый контекст, описывающий правила группировки приложений/систем, в файле `\Datalake\contexts.yaml`
```
  GroupingByDevelopmentModel:
    title: Группировка по модели разработки
    extra-links: true
    components:
      - Romashka.Systems.*.*     # Для отображения в списке выбора контекста в карточке компонента
      - Romashka.Systems.*.*.*   # СДля отображения в списке выбора контекста в карточке компонента
    source: >
      (

          $Grouping := {
            "GroupingName": "DevelopmentModel",                         /* Имя группировки, добавляемое в описание идентификатора компонента DDD */
            "GroupingTitle": "Модель разработки",                       /* Представление группировки, отображаемое пользователями на схеме контекста */
            "FieldPath": "*.extension.development_model",               /* Путь к значениям для  расчета группировок */
            "Dictionary": $.dictionaries.DevelopmentModel.parameters};  /* Описание вариантов значений и представлений группируемого атрибута */

          $Components := $eval($.functions.get_transformed_components_description, {"Grouping": $Grouping, "Datalake": $});

          $ ~> | $ | { "components": $Components } | 

      )
```
В целом, на этом этапе достаточно добавить свойство контекста `location`, чтобы контекст отобразился в интерфейсе и был доступен в карточке компонента. Следующие пункты необходимы для реализации единого интерфейсного подхода текущего примера.
- Скорректировать файл `\Datalake\docs.yaml`, добавив строки:
```
...
  Romashka.doc.GroupingByDevelopmentModel:
    type: markdown
    source: templates/GroupingByDevelopmentModel.md
...
```
- Добавить **новый** файл `\Datalake\Templates\GroupingByDevelopmentModel.md` следующего содержания (отдельное представление для отображения группировки по модели разработки):
```
   **Перейти** | [Группировка по-умолчанию](/docs/Romashka.doc.DefaultView)
   | [Группировка по статусу](/docs/Romashka.doc.GroupingByStatus)
   | [Группировка по уровню критичности](/docs/Romashka.doc.GroupingByStatusCriticalLevel) |

![Архитектура](@context/GroupingByDevelopmentModel)
```
- Скорректировать в файл `\Datalake\Templates\DefaultView.md`, добавив "ссылку" на созданный ранее документ (`/docs/Romashka.doc.GroupingByDevelopmentModel`):
```   
**Перейти** | [Группировка по статусу](/docs/Romashka.doc.GroupingByStatus)
   | [Группировка по уровню критичности](/docs/Romashka.doc.GroupingByStatusCriticalLevel)
   | [Группировка по модели разработки](/docs/Romashka.doc.GroupingByDevelopmentModel) |

![Архитектура](@context/DefaultView)
```
- Скорректировать в файл `\Datalake\Templates\GroupingByStatus.md`, добавив "ссылку" на созданный ранее документ (`/docs/Romashka.doc.GroupingByDevelopmentModel`):
```   
**Перейти** | [Группировка по-умолчанию](/docs/Romashka.doc.DefaultView) 
| [Группировка по уровню критичности](/docs/Romashka.doc.GroupingByStatusCriticalLevel) 
| [Группировка по модели разработки](/docs/Romashka.doc.GroupingByDevelopmentModel) |

![Архитектура](@context/GroupingByStatus)
```
- Скорректировать в файл `\Datalake\Templates\GroupingByStatusCriticalLevel.md`, добавив "ссылку" на созданный ранее документ (`/docs/Romashka.doc.GroupingByDevelopmentModel`):
```   
**Перейти** | [Группировка по-умолчанию](/docs/Romashka.doc.DefaultView)
| [Группировка по статусу](/docs/Romashka.doc.GroupingByStatus)
| [Группировка по модели разработки](/docs/Romashka.doc.GroupingByDevelopmentModel) |

![Архитектура](@context/GroupingByStatusCriticalLevel)
```

## Авторские права
- Автор примера: https://t.me/SultanovStanislav
