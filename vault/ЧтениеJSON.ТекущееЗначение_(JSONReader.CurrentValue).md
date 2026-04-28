# ЧтениеJSON.ТекущееЗначение

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [JSON](JSON-2.md) › [ЧтениеJSON](ЧтениеJSON_(JSONReader).md) › [Свойства](ЧтениеJSON__Свойства.md)

ЧтениеJSON (JSONReader)

ТекущееЗначение (CurrentValue)

Доступен, начиная с версии 8.3.6.

Использование:

Только чтение.

Описание:

Тип: [Число](lang__def_Number.md), [Строка](lang__def_String.md), [Булево](lang__Булево_(Boolean).md), [Неопределено](lang__def_Undefined.md).   
Содержит текущее значение:

- [Число](lang__def_Number.md) - если [ТипТекущегоЗначения](ЧтениеJSON.ТипТекущегоЗначения_(JSONReader.CurrentValueType).md) имеет значение [Число](ТипЗначенияJSON.Число_(JSONValueType.Number).md);
- [Строка](lang__def_String.md) - если [ТипТекущегоЗначения](ЧтениеJSON.ТипТекущегоЗначения_(JSONReader.CurrentValueType).md) имеет значение:
  - [Комментарий](ТипЗначенияJSON.Комментарий_(JSONValueType.Comment).md),
  - [ИмяСвойства](ТипЗначенияJSON.ИмяСвойства_(JSONValueType.PropertyName).md),
  - [Строка](ТипЗначенияJSON.Строка_(JSONValueType.String).md);
- [Булево](lang__Булево_(Boolean).md) - если [ТипТекущегоЗначения](ЧтениеJSON.ТипТекущегоЗначения_(JSONReader.CurrentValueType).md) имеет значение [Булево](ТипЗначенияJSON.Булево_(JSONValueType.Boolean).md),
- [Неопределено](lang__def_Undefined.md) - если [ТипТекущегоЗначения](ЧтениеJSON.ТипТекущегоЗначения_(JSONReader.CurrentValueType).md) имеет значение [Null](ТипЗначенияJSON.Null_(JSONValueType.Null).md).

Исключение генерируется в случае, если [ТипТекущегоЗначения](ЧтениеJSON.ТипТекущегоЗначения_(JSONReader.CurrentValueType).md) имеет одно из следующих значений:

- [НачалоМассива](ТипЗначенияJSON.НачалоМассива_(JSONValueType.ArrayStart).md),
- [КонецМассива](ТипЗначенияJSON.КонецМассива_(JSONValueType.ArrayEnd).md),
- [НачалоОбъекта](ТипЗначенияJSON.НачалоОбъекта_(JSONValueType.ObjectStart).md),
- [КонецОбъекта](ТипЗначенияJSON.КонецОбъекта_(JSONValueType.ObjectEnd).md),
- [Ничего](ТипЗначенияJSON.Ничего_(JSONValueType.None).md).

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.3.6.

---
