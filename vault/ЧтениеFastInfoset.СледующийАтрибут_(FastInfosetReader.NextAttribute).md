# ЧтениеFastInfoset.СледующийАтрибут

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [XML](XML-2.md) › [ЧтениеFastInfoset](ЧтениеFastInfoset_(FastInfosetReader).md) › [Методы](ЧтениеFastInfoset__Методы.md)

ЧтениеFastInfoset (FastInfosetReader)

СледующийАтрибут (NextAttribute)

Доступен, начиная с версии 8.1.

Синтаксис:

СледующийАтрибут()

Возвращаемое значение:

Тип: [Булево](lang__Булево_(Boolean).md).   
[Истина](lang__def_BooleanTrue.md) - атрибут прочитан, [Ложь](lang__def_BooleanFalse.md) - атрибутов больше нет.

Описание:

Позиционирует текущее состояние объекта на следующий атрибут текущего элемента. Если вызов осуществляется при текущем узле [НачалоЭлемента](ТипУзлаXML.НачалоЭлемента_(XMLNodeType.StartElement).md), то вызов аналогичен методу [ЧтениеFastInfoset.ПервыйАтрибут](ЧтениеFastInfoset.ПервыйАтрибут_(FastInfosetReader.FirstAttribute).md).  
При этом свойствам [ЧтениеFastInfoset.ТипУзла](ЧтениеFastInfoset.ТипУзла_(FastInfosetReader.NodeType).md), [ЧтениеFastInfoset.Имя](ЧтениеFastInfoset.Имя_(FastInfosetReader.Name).md), [ЧтениеFastInfoset.ЛокальноеИмя](ЧтениеFastInfoset.ЛокальноеИмя_(FastInfosetReader.LocalName).md), [ЧтениеFastInfoset.Префикс](ЧтениеFastInfoset.Префикс_(FastInfosetReader.Prefix).md), [ЧтениеFastInfoset.URIПространстваИмен](ЧтениеFastInfoset.URIПространстваИмен_(FastInfosetReader.NamespaceURI).md), [ЧтениеFastInfoset.Значение](ЧтениеFastInfoset.Значение_(FastInfosetReader.Value).md) и т.д. присваиваются значения, соответствующие прочитанным данным атрибута.  
Вызов метода [ЧтениеFastInfoset.Прочитать](ЧтениеFastInfoset.Прочитать_(FastInfosetReader.Read).md) прерывает процесс чтения атрибутов элемента и позиционирует текущий узел на следующий атрибут после [НачалоЭлемента](ТипУзлаXML.НачалоЭлемента_(XMLNodeType.StartElement).md).

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.1.

---
