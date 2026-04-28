# ЧтениеFastInfoset.ПервыйАтрибут

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [XML](XML-2.md) › [ЧтениеFastInfoset](ЧтениеFastInfoset_(FastInfosetReader).md) › [Методы](ЧтениеFastInfoset__Методы.md)

ЧтениеFastInfoset (FastInfosetReader)

ПервыйАтрибут (FirstAttribute)

Доступен, начиная с версии 8.1.

Синтаксис:

ПервыйАтрибут()

Возвращаемое значение:

Тип: [Булево](lang__Булево_(Boolean).md).   
[Истина](lang__def_BooleanTrue.md) - атрибут прочитан, [Ложь](lang__def_BooleanFalse.md) - в противном случае.

Описание:

Позиционирует текущее состояние объекта на первый атрибут текущего элемента.   
При этом свойствам [ЧтениеFastInfoset.ТипУзла](ЧтениеFastInfoset.ТипУзла_(FastInfosetReader.NodeType).md), [ЧтениеFastInfoset.Имя](ЧтениеFastInfoset.Имя_(FastInfosetReader.Name).md), [ЧтениеFastInfoset.ЛокальноеИмя](ЧтениеFastInfoset.ЛокальноеИмя_(FastInfosetReader.LocalName).md), [ЧтениеFastInfoset.Префикс](ЧтениеFastInfoset.Префикс_(FastInfosetReader.Prefix).md), [ЧтениеFastInfoset.URIПространстваИмен](ЧтениеFastInfoset.URIПространстваИмен_(FastInfosetReader.NamespaceURI).md), [ЧтениеFastInfoset.Значение](ЧтениеFastInfoset.Значение_(FastInfosetReader.Value).md) и т.д. присваиваются значения, соответствующие прочитанным данным атрибута.

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Примечание:

Имеет смысл, если текущим узлом является [НачалоЭлемента](ТипУзлаXML.НачалоЭлемента_(XMLNodeType.StartElement).md) или [Атрибут](ТипУзлаXML.Атрибут_(XMLNodeType.Attribute).md).

Использование в версии:

Доступен, начиная с версии 8.1.

---
