# ВыражениеXPath.Вычислить

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [DOM](DOM-2.md) › [ВыражениеXPath](ВыражениеXPath_(XPathExpression).md) › [Методы](ВыражениеXPath__Методы.md)

ВыражениеXPath (XPathExpression)

Вычислить (Evaluate)

Доступен, начиная с версии 8.1.

Синтаксис:

Вычислить(<УзелКонтекста>, <ТипРезультата>)

Параметры:

<УзелКонтекста> (обязательный)

Тип: [АтрибутDOM](АтрибутDOM_(DOMAttribute).md), [ДокументDOM](ДокументDOM_(DOMDocument).md), [ЭлементDOM](ЭлементDOM_(DOMElement).md), [ОпределениеТипаДокументаDOM](ОпределениеТипаДокументаDOM_(DOMDocumentType).md), [НотацияDOM](НотацияDOM_(DOMNotation).md), [СущностьDOM](СущностьDOM_(DOMEntity).md), [ФрагментДокументаDOM](ФрагментДокументаDOM_(DOMDocumentFragment).md), [ТекстDOM](ТекстDOM_(DOMText).md), [КомментарийDOM](КомментарийDOM_(DOMComment).md), [СекцияCDATADOM](СекцияCDATADOM_(DOMCDATASection).md), [ИнструкцияОбработкиDOM](ИнструкцияОбработкиDOM_(DOMProcessingInstruction).md), [СсылкаНаСущностьDOM](СсылкаНаСущностьDOM_(DOMEntityReference).md), [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md).   
Узел DOM - контекст для вычисления выражения XPath.   
Узел должен принадлежать тому же документу DOM, которым было создано выражение XPath (в противном случае будет вызвано исключение) и может быть следующих видов: [Документ](ТипУзлаDOM.Документ_(DOMNodeType.Document).md), [Элемент](ТипУзлаDOM.Элемент_(DOMNodeType.Element).md), [Атрибут](ТипУзлаDOM.Атрибут_(DOMNodeType.Attribute).md), [Текст](ТипУзлаDOM.Текст_(DOMNodeType.Text).md), [СекцияCDATA](ТипУзлаDOM.СекцияCDATA_(DOMNodeType.CDATASection).md), [Комментарий](ТипУзлаDOM.Комментарий_(DOMNodeType.Comment).md), [ИнструкцияОбработки](ТипУзлаDOM.ИнструкцияОбработки_(DOMNodeType.ProcessingInstruction).md), [ПространствоИменXPath](ТипУзлаDOM.ПространствоИменXPath_(DOMNodeType.XPathNamespace).md).

<ТипРезультата> (необязательный)

Тип: [ТипРезультатаDOMXPath](ТипРезультатаDOMXPath_(DOMXPathResultType).md).   
Тип результата вычисления выражения XPath.  
Значение по умолчанию: [Любой](ТипРезультатаDOMXPath.Любой_(DOMXPathResultType.Any).md).

Возвращаемое значение:

Тип: [РезультатXPath](РезультатXPath_(XPathResult).md).   

Описание:

Производит вычисление выражения XPath для указанного узла контекста.

Доступность:

Сервер, толстый клиент, внешнее соединение, мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.1.

---
