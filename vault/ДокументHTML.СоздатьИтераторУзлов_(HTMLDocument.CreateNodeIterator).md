# ДокументHTML.СоздатьИтераторУзлов

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [HTML](HTML.md) › [ДокументHTML](ДокументHTML_(HTMLDocument).md) › [Методы](ДокументHTML__Методы.md)

ДокументHTML (HTMLDocument)

СоздатьИтераторУзлов (CreateNodeIterator)

Доступен, начиная с версии 8.2.

Синтаксис:

СоздатьИтераторУзлов(<Узел>)

Параметры:

<Узел> (обязательный)

Тип: [АтрибутHTML](АтрибутHTML_(HTMLAttribute).md), [ЭлементHTML](ЭлементHTML_(HTMLElement).md), [ЭлементКнопкаHTML](ЭлементКнопкаHTML_(HTMLButtonElement).md), [ЭлементВводаHTML](ЭлементВводаHTML_(HTMLInputElement).md), [ЭлементЗаголовокHTML](ЭлементЗаголовокHTML_(HTMLHeadElement).md), [ЭлементРазметкаHTML](ЭлементРазметкаHTML_(HTMLHtmlElement).md), [ЭлементПлавающийФреймHTML](ЭлементПлавающийФреймHTML_(HTMLIFrameElement).md), [ЭлементВставкаHTML](ЭлементВставкаHTML_(HTMLEmbedElement).md), [ЭлементФреймHTML](ЭлементФреймHTML_(HTMLFrameElement).md), [ЭлементНаборФреймовHTML](ЭлементНаборФреймовHTML_(HTMLFrameSetElement).md), [ЭлементМетаHTML](ЭлементМетаHTML_(HTMLMetaElement).md), [ЭлементОбъектHTML](ЭлементОбъектHTML_(HTMLObjectElement).md), [ЭлементСкриптHTML](ЭлементСкриптHTML_(HTMLScriptElement).md), [ЭлементТаблицаHTML](ЭлементТаблицаHTML_(HTMLTableElement).md), [ЭлементСтрокаТаблицыHTML](ЭлементСтрокаТаблицыHTML_(HTMLTableRowElement).md), [ЭлементЯчейкаТаблицыHTML](ЭлементЯчейкаТаблицыHTML_(HTMLTableCellElement).md), [ЭлементКолонкаТаблицыHTML](ЭлементКолонкаТаблицыHTML_(HTMLTableColElement).md), [ЭлементЗаголовокТаблицыHTML](ЭлементЗаголовокТаблицыHTML_(HTMLTableCaptionElement).md), [ЭлементБлокHTML](ЭлементБлокHTML_(HTMLDivElement).md), [ЭлементЛинияHTML](ЭлементЛинияHTML_(HTMLHRElement).md), [ЭлементФорматированногоТекстаHTML](ЭлементФорматированногоТекстаHTML_(HTMLPreElement).md), [ЭлементКартинкаHTML](ЭлементКартинкаHTML_(HTMLImageElement).md), [ЭлементСвязьHTML](ЭлементСвязьHTML_(HTMLLinkElement).md), [ЭлементЯкорьHTML](ЭлементЯкорьHTML_(HTMLAnchorElement).md), [ЭлементАплетHTML](ЭлементАплетHTML_(HTMLAppletElement).md), [ЭлементФормаHTML](ЭлементФормаHTML_(HTMLFormElement).md), [ДокументHTML](ДокументHTML_(HTMLDocument).md), [ТекстHTML](ТекстHTML_(HTMLText).md), [КомментарийHTML](КомментарийHTML_(HTMLComment).md).   
Узел HTMLDOM - стартовый узел итератора.

Возвращаемое значение:

Тип: [ИтераторУзловDOM](ИтераторУзловDOM_(DOMNodeIterator).md).   

Описание:

Создает новый итератор по поддереву документа HTML, начиная с указанного узла.  
При создании итератор устанавливается на позицию перед указанным узлом.  
Метод соответствует интерфейсу NodeIterator стандарта W3C (Подробнее см. <http://www.w3.org/TR/2000/REC-DOM-Level-2-Traversal-Range-20001113/traversal.html#Traversal-NodeIterator>).

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.2.

---
