# Пример кастомного DSL

**Цель примера:** Представить пример кастомного DSL для отображения контекстных диаграмм

Пользовательский DSL должен имплементировать следующий интерфейс

**отображение региона**
!unquoted procedure $Region($alias, $label, $type)
!endprocedure

**отображение заголовка**
!unquoted procedure $Header($Title="Header", !endprocedure
!endprocedure

**начало отображения элемента**
```
!unquoted procedure $Entity($entity, $ACName, $id, $ACType)
!endprocedure
```

**конец отображения элемента**
```
!unquoted procedure $EntityEnd($entity)
!endprocedure
```
**отображения аспекта элемента**
```
!unquoted procedure $EntityAspect($entity, $prop)
!endprocedure
```
**отображение расширения элемента**
```
!unquoted procedure $EntityExpand($entity, $ID)
!endprocedure
```
**для включения пользовательского DSL в контексте, необходимо задекларировать шаблон в контексте**
```
uml:  
    $dsl: dsl.puml
```