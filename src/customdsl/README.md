# Пример кастомного DSL

## Цель примера:
Представить пример кастомного DSL для отображения контекстных диаграмм.
Пользовательский DSL должен имплементировать следующий интерфейс:

### Отображение региона
```
!unquoted procedure $Region($alias, $label, $type)
... здесь PlantUML код имплементации ...
!endprocedure
```

### Отображение заголовка
```
!unquoted procedure $Header($Title="Header", !endprocedure
... здесь PlantUML код имплементации ...
!endprocedure
```

### Начало отображения элемента
```
!unquoted procedure $Entity($entity, $ACName, $id, $ACType)
... здесь PlantUML код имплементации ...
!endprocedure
```

### Конец отображения элемента
```
!unquoted procedure $EntityEnd($entity)
... здесь PlantUML код имплементации ...
!endprocedure
```
### Отображения аспекта элемента
```
!unquoted procedure $EntityAspect($entity, $prop)
... здесь PlantUML код имплементации ...
!endprocedure
```

### Отображение расширения элемента
```
!unquoted procedure $EntityExpand($entity, $ID)
... здесь PlantUML код имплементации ...
!endprocedure
```

## Для включения пользовательского DSL в контексте, необходимо задекларировать шаблон в контексте
```
uml:  
    $dsl: dsl.puml
```
