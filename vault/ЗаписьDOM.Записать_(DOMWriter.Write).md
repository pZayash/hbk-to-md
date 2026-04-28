# ЗаписьDOM.Записать

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [DOM](DOM-2.md) › [ЗаписьDOM](ЗаписьDOM_(DOMWriter).md) › [Методы](ЗаписьDOM__Методы.md)

ЗаписьDOM (DOMWriter)

Записать (Write)

Доступен, начиная с версии 8.1.

Синтаксис:

Записать(<Узел>, <ПриемникДанных>)

Параметры:

<Узел> (обязательный)

Тип: [АтрибутDOM](АтрибутDOM_(DOMAttribute).md), [ДокументDOM](ДокументDOM_(DOMDocument).md), [ЭлементDOM](ЭлементDOM_(DOMElement).md), [ОпределениеТипаДокументаDOM](ОпределениеТипаДокументаDOM_(DOMDocumentType).md), [НотацияDOM](НотацияDOM_(DOMNotation).md), [СущностьDOM](СущностьDOM_(DOMEntity).md), [ФрагментДокументаDOM](ФрагментДокументаDOM_(DOMDocumentFragment).md), [ТекстDOM](ТекстDOM_(DOMText).md), [КомментарийDOM](КомментарийDOM_(DOMComment).md), [СекцияCDATADOM](СекцияCDATADOM_(DOMCDATASection).md), [ИнструкцияОбработкиDOM](ИнструкцияОбработкиDOM_(DOMProcessingInstruction).md), [СсылкаНаСущностьDOM](СсылкаНаСущностьDOM_(DOMEntityReference).md), [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md), [АтрибутHTML](АтрибутHTML_(HTMLAttribute).md), [ЭлементHTML](ЭлементHTML_(HTMLElement).md), [ЭлементКнопкаHTML](ЭлементКнопкаHTML_(HTMLButtonElement).md), [ЭлементВводаHTML](ЭлементВводаHTML_(HTMLInputElement).md), [ЭлементЗаголовокHTML](ЭлементЗаголовокHTML_(HTMLHeadElement).md), [ЭлементРазметкаHTML](ЭлементРазметкаHTML_(HTMLHtmlElement).md), [ЭлементПлавающийФреймHTML](ЭлементПлавающийФреймHTML_(HTMLIFrameElement).md), [ЭлементВставкаHTML](ЭлементВставкаHTML_(HTMLEmbedElement).md), [ЭлементФреймHTML](ЭлементФреймHTML_(HTMLFrameElement).md), [ЭлементНаборФреймовHTML](ЭлементНаборФреймовHTML_(HTMLFrameSetElement).md), [ЭлементМетаHTML](ЭлементМетаHTML_(HTMLMetaElement).md), [ЭлементОбъектHTML](ЭлементОбъектHTML_(HTMLObjectElement).md), [ЭлементСкриптHTML](ЭлементСкриптHTML_(HTMLScriptElement).md), [ЭлементТаблицаHTML](ЭлементТаблицаHTML_(HTMLTableElement).md), [ЭлементСтрокаТаблицыHTML](ЭлементСтрокаТаблицыHTML_(HTMLTableRowElement).md), [ЭлементЯчейкаТаблицыHTML](ЭлементЯчейкаТаблицыHTML_(HTMLTableCellElement).md), [ЭлементКолонкаТаблицыHTML](ЭлементКолонкаТаблицыHTML_(HTMLTableColElement).md), [ЭлементЗаголовокТаблицыHTML](ЭлементЗаголовокТаблицыHTML_(HTMLTableCaptionElement).md), [ЭлементБлокHTML](ЭлементБлокHTML_(HTMLDivElement).md), [ЭлементЛинияHTML](ЭлементЛинияHTML_(HTMLHRElement).md), [ЭлементФорматированногоТекстаHTML](ЭлементФорматированногоТекстаHTML_(HTMLPreElement).md), [ЭлементКартинкаHTML](ЭлементКартинкаHTML_(HTMLImageElement).md), [ЭлементСвязьHTML](ЭлементСвязьHTML_(HTMLLinkElement).md), [ЭлементЯкорьHTML](ЭлементЯкорьHTML_(HTMLAnchorElement).md), [ЭлементАплетHTML](ЭлементАплетHTML_(HTMLAppletElement).md), [ЭлементФормаHTML](ЭлементФормаHTML_(HTMLFormElement).md), [ДокументHTML](ДокументHTML_(HTMLDocument).md), [ТекстHTML](ТекстHTML_(HTMLText).md), [КомментарийHTML](КомментарийHTML_(HTMLComment).md).   
Записываемый узел DOM или узел HTML.

<ПриемникДанных> (обязательный)

Тип: [ЗаписьУзловDOM](ЗаписьУзловDOM_(DOMNodeWriter).md), [ЗаписьFastInfoset](ЗаписьFastInfoset_(FastInfosetWriter).md), [ЗаписьXML](ЗаписьXML_(XMLWriter).md), [ЗаписьHTML](ЗаписьHTML_(HTMLWriter).md).   
Объект, записывающий данные XML или HTML.

Описание:

Выполняет запись узла DOM.

Доступность:

Сервер, толстый клиент, внешнее соединение, мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.1.

---
