# ЧтениеFastInfoset.Прочитать

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [XML](XML-2.md) › [ЧтениеFastInfoset](ЧтениеFastInfoset_(FastInfosetReader).md) › [Методы](ЧтениеFastInfoset__Методы.md)

ЧтениеFastInfoset (FastInfosetReader)

Прочитать (Read)

Доступен, начиная с версии 8.1.

Синтаксис:

Прочитать()

Возвращаемое значение:

Тип: [Булево](lang__Булево_(Boolean).md).   
[Истина](lang__def_BooleanTrue.md) - очередной узел прочитан; [Ложь](lang__def_BooleanFalse.md) - текст XML завершился.

Описание:

Считывает очередной узел XML. При этом свойствам [ЧтениеFastInfoset.ТипУзла](ЧтениеFastInfoset.ТипУзла_(FastInfosetReader.NodeType).md), [ЧтениеFastInfoset.Имя](ЧтениеFastInfoset.Имя_(FastInfosetReader.Name).md), [ЧтениеFastInfoset.ЛокальноеИмя](ЧтениеFastInfoset.ЛокальноеИмя_(FastInfosetReader.LocalName).md), [ЧтениеFastInfoset.Префикс](ЧтениеFastInfoset.Префикс_(FastInfosetReader.Prefix).md), [ЧтениеFastInfoset.URIПространстваИмен](ЧтениеFastInfoset.URIПространстваИмен_(FastInfosetReader.NamespaceURI).md) и [ЧтениеFastInfoset.Значение](ЧтениеFastInfoset.Значение_(FastInfosetReader.Value).md) присваиваются значения, соответствующие прочитанным данным.

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Пример:

|  |
| --- |
| Чтение.ОткрытьФайл("c:/docs/data.xml"); Пока Чтение.Прочитать() Цикл     // Обработка узла XML  КонецЦикла; |

Использование в версии:

Доступен, начиная с версии 8.1.

---
