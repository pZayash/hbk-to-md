# ПостроительDOM.ПрочитатьВКонтексте

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [DOM](DOM-2.md) › [ПостроительDOM](ПостроительDOM_(DOMBuilder).md) › [Методы](ПостроительDOM__Методы.md)

ПостроительDOM (DOMBuilder)

ПрочитатьВКонтексте (ReadWithContext)

Доступен, начиная с версии 8.1.

Синтаксис:

ПрочитатьВКонтексте(<ИсточникДанныхXML>, <УзелКонтекстаDOM>, <Действие>)

Параметры:

<ИсточникДанныхXML> (обязательный)

Тип: [ЧтениеУзловDOM](ЧтениеУзловDOM_(DOMNodeReader).md), [ЧтениеFastInfoset](ЧтениеFastInfoset_(FastInfosetReader).md), [ЧтениеXML](ЧтениеXML_(XMLReader).md).   
Объект чтения данных XML.

<УзелКонтекстаDOM> (обязательный)

Тип: [АтрибутDOM](АтрибутDOM_(DOMAttribute).md), [ДокументDOM](ДокументDOM_(DOMDocument).md), [ЭлементDOM](ЭлементDOM_(DOMElement).md), [ОпределениеТипаДокументаDOM](ОпределениеТипаДокументаDOM_(DOMDocumentType).md), [НотацияDOM](НотацияDOM_(DOMNotation).md), [СущностьDOM](СущностьDOM_(DOMEntity).md), [ФрагментДокументаDOM](ФрагментДокументаDOM_(DOMDocumentFragment).md), [ТекстDOM](ТекстDOM_(DOMText).md), [КомментарийDOM](КомментарийDOM_(DOMComment).md), [СекцияCDATADOM](СекцияCDATADOM_(DOMCDATASection).md), [ИнструкцияОбработкиDOM](ИнструкцияОбработкиDOM_(DOMProcessingInstruction).md), [СсылкаНаСущностьDOM](СсылкаНаСущностьDOM_(DOMEntityReference).md), [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md).   
Узел контекста DOM.

<Действие> (обязательный)

Тип: [ДействиеПостроителяDOM](ДействиеПостроителяDOM_(DOMBuilderAction).md).   
Действия, выполняемые над считываемыми узлами.

Возвращаемое значение:

Тип: [АтрибутDOM](АтрибутDOM_(DOMAttribute).md), [ДокументDOM](ДокументDOM_(DOMDocument).md), [ЭлементDOM](ЭлементDOM_(DOMElement).md), [ОпределениеТипаДокументаDOM](ОпределениеТипаДокументаDOM_(DOMDocumentType).md), [НотацияDOM](НотацияDOM_(DOMNotation).md), [СущностьDOM](СущностьDOM_(DOMEntity).md), [ФрагментДокументаDOM](ФрагментДокументаDOM_(DOMDocumentFragment).md), [ТекстDOM](ТекстDOM_(DOMText).md), [КомментарийDOM](КомментарийDOM_(DOMComment).md), [СекцияCDATADOM](СекцияCDATADOM_(DOMCDATASection).md), [ИнструкцияОбработкиDOM](ИнструкцияОбработкиDOM_(DOMProcessingInstruction).md), [СсылкаНаСущностьDOM](СсылкаНаСущностьDOM_(DOMEntityReference).md), [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md).   

Описание:

Выполняет чтение узла (узлов) в контексте документа DOM.

Доступность:

Сервер, толстый клиент, внешнее соединение, мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.1.

---
