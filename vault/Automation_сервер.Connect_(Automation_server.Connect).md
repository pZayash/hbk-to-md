# Automation сервер.Connect

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Средства интеграции и администрирования](Средства_интеграции_и_администрирования.md) › [Automation сервер](Automation_сервер_(Automation_server).md) › [Методы](Automation_сервер__Методы.md)

Automation сервер (Automation server)

Connect (Connect)

Доступен, начиная с версии 8.1.

Синтаксис:

Connect(<СтрокаСоединения>)

Параметры:

<СтрокаСоединения> (обязательный)

Тип: [Строка](lang__def_String.md).   
Строка параметров ([Строка соединения](lang__Строка_соединения.md)), используемая 1С:Предприятием для соединения с информационной базой.

Возвращаемое значение:

Тип: [Булево](lang__Булево_(Boolean).md).   
[Истина](lang__def_BooleanTrue.md) - инициализация прошла удачно, [Ложь](lang__def_BooleanFalse.md) - в противном случае.

Описание:

Выполняет соединение системы 1С:Предприятие с информационной базой.

Доступность:

Интеграция.

Пример:

|  |
| --- |
| // Пример приводится на языке MS Visual Basic:  Dim connector As Object Set connector=CreateObject("V83.Application") result=connector.Connect("File=c:\InfoBases\Trade;Usr=Director;") |

Использование в версии:

Доступен, начиная с версии 8.1.

---
