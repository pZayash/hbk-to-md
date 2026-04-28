# ДокументHTML.ИмпортироватьУзел

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [HTML](HTML.md) › [ДокументHTML](ДокументHTML_(HTMLDocument).md) › [Методы](ДокументHTML__Методы.md)

ДокументHTML (HTMLDocument)

ИмпортироватьУзел (ImportNode)

Доступен, начиная с версии 8.2.

Синтаксис:

ИмпортироватьУзел(<Узел>, <Рекурсивно>)

Параметры:

<Узел> (обязательный)

Тип: [АтрибутHTML](АтрибутHTML_(HTMLAttribute).md), [ЭлементHTML](ЭлементHTML_(HTMLElement).md), [ЭлементКнопкаHTML](ЭлементКнопкаHTML_(HTMLButtonElement).md), [ЭлементВводаHTML](ЭлементВводаHTML_(HTMLInputElement).md), [ЭлементЗаголовокHTML](ЭлементЗаголовокHTML_(HTMLHeadElement).md), [ЭлементРазметкаHTML](ЭлементРазметкаHTML_(HTMLHtmlElement).md), [ЭлементПлавающийФреймHTML](ЭлементПлавающийФреймHTML_(HTMLIFrameElement).md), [ЭлементВставкаHTML](ЭлементВставкаHTML_(HTMLEmbedElement).md), [ЭлементФреймHTML](ЭлементФреймHTML_(HTMLFrameElement).md), [ЭлементНаборФреймовHTML](ЭлементНаборФреймовHTML_(HTMLFrameSetElement).md), [ЭлементМетаHTML](ЭлементМетаHTML_(HTMLMetaElement).md), [ЭлементОбъектHTML](ЭлементОбъектHTML_(HTMLObjectElement).md), [ЭлементСкриптHTML](ЭлементСкриптHTML_(HTMLScriptElement).md), [ЭлементТаблицаHTML](ЭлементТаблицаHTML_(HTMLTableElement).md), [ЭлементСтрокаТаблицыHTML](ЭлементСтрокаТаблицыHTML_(HTMLTableRowElement).md), [ЭлементЯчейкаТаблицыHTML](ЭлементЯчейкаТаблицыHTML_(HTMLTableCellElement).md), [ЭлементКолонкаТаблицыHTML](ЭлементКолонкаТаблицыHTML_(HTMLTableColElement).md), [ЭлементЗаголовокТаблицыHTML](ЭлементЗаголовокТаблицыHTML_(HTMLTableCaptionElement).md), [ЭлементБлокHTML](ЭлементБлокHTML_(HTMLDivElement).md), [ЭлементЛинияHTML](ЭлементЛинияHTML_(HTMLHRElement).md), [ЭлементФорматированногоТекстаHTML](ЭлементФорматированногоТекстаHTML_(HTMLPreElement).md), [ЭлементКартинкаHTML](ЭлементКартинкаHTML_(HTMLImageElement).md), [ЭлементСвязьHTML](ЭлементСвязьHTML_(HTMLLinkElement).md), [ЭлементЯкорьHTML](ЭлементЯкорьHTML_(HTMLAnchorElement).md), [ЭлементАплетHTML](ЭлементАплетHTML_(HTMLAppletElement).md), [ЭлементФормаHTML](ЭлементФормаHTML_(HTMLFormElement).md), [ДокументHTML](ДокументHTML_(HTMLDocument).md), [ТекстHTML](ТекстHTML_(HTMLText).md), [КомментарийHTML](КомментарийHTML_(HTMLComment).md).   
Импортируемый узел HTMLDOM.

<Рекурсивно> (обязательный)

Тип: [Булево](lang__Булево_(Boolean).md).   
Признак "глубокого" импортирования.   
[Истина](lang__def_BooleanTrue.md) - будут рекурсивно импортированы все дочерние узлы импортируемого узла. Исключения составляют узлы [Атрибут](ТипУзлаDOM.Атрибут_(DOMNodeType.Attribute).md) и [СсылкаНаСущность](ТипУзлаDOM.СсылкаНаСущность_(DOMNodeType.EntityReference).md).   
Для [Атрибут](ТипУзлаDOM.Атрибут_(DOMNodeType.Attribute).md) дочерние узлы импортируются всегда.  
[Ложь](lang__def_BooleanFalse.md) - импортируется только переданный узел.

Возвращаемое значение:

Тип: [АтрибутHTML](АтрибутHTML_(HTMLAttribute).md), [ЭлементHTML](ЭлементHTML_(HTMLElement).md), [ЭлементКнопкаHTML](ЭлементКнопкаHTML_(HTMLButtonElement).md), [ЭлементВводаHTML](ЭлементВводаHTML_(HTMLInputElement).md), [ЭлементЗаголовокHTML](ЭлементЗаголовокHTML_(HTMLHeadElement).md), [ЭлементРазметкаHTML](ЭлементРазметкаHTML_(HTMLHtmlElement).md), [ЭлементПлавающийФреймHTML](ЭлементПлавающийФреймHTML_(HTMLIFrameElement).md), [ЭлементВставкаHTML](ЭлементВставкаHTML_(HTMLEmbedElement).md), [ЭлементФреймHTML](ЭлементФреймHTML_(HTMLFrameElement).md), [ЭлементНаборФреймовHTML](ЭлементНаборФреймовHTML_(HTMLFrameSetElement).md), [ЭлементМетаHTML](ЭлементМетаHTML_(HTMLMetaElement).md), [ЭлементОбъектHTML](ЭлементОбъектHTML_(HTMLObjectElement).md), [ЭлементСкриптHTML](ЭлементСкриптHTML_(HTMLScriptElement).md), [ЭлементТаблицаHTML](ЭлементТаблицаHTML_(HTMLTableElement).md), [ЭлементСтрокаТаблицыHTML](ЭлементСтрокаТаблицыHTML_(HTMLTableRowElement).md), [ЭлементЯчейкаТаблицыHTML](ЭлементЯчейкаТаблицыHTML_(HTMLTableCellElement).md), [ЭлементКолонкаТаблицыHTML](ЭлементКолонкаТаблицыHTML_(HTMLTableColElement).md), [ЭлементЗаголовокТаблицыHTML](ЭлементЗаголовокТаблицыHTML_(HTMLTableCaptionElement).md), [ЭлементБлокHTML](ЭлементБлокHTML_(HTMLDivElement).md), [ЭлементЛинияHTML](ЭлементЛинияHTML_(HTMLHRElement).md), [ЭлементФорматированногоТекстаHTML](ЭлементФорматированногоТекстаHTML_(HTMLPreElement).md), [ЭлементКартинкаHTML](ЭлементКартинкаHTML_(HTMLImageElement).md), [ЭлементСвязьHTML](ЭлементСвязьHTML_(HTMLLinkElement).md), [ЭлементЯкорьHTML](ЭлементЯкорьHTML_(HTMLAnchorElement).md), [ЭлементАплетHTML](ЭлементАплетHTML_(HTMLAppletElement).md), [ЭлементФормаHTML](ЭлементФормаHTML_(HTMLFormElement).md), [ДокументHTML](ДокументHTML_(HTMLDocument).md), [ТекстHTML](ТекстHTML_(HTMLText).md), [КомментарийHTML](КомментарийHTML_(HTMLComment).md).   

Описание:

Импортирует узел из другого документа DOM в данный.  
Для каждого узла импортируются ТипУзла, ИмяУзла, а также свойства, относящиеся к пространствам имен: ЛокальноеИмя, Префикс. Пользовательские данные не переносятся.  
Правила импорта для типов узлов:

- [Атрибут](ТипУзлаDOM.Атрибут_(DOMNodeType.Attribute).md) - [ЭлементВладелец](АтрибутDOM.ЭлементВладелец_(DOMAttribute.OwnerElement).md) устанавливается в [Неопределено](lang__def_Undefined.md), признак [Указан](АтрибутDOM.Указан_(DOMAttribute.Specified).md) устанавливается в [Истина](lang__def_BooleanTrue.md), импортируются все потомки узла;
- [Документ](ТипУзлаDOM.Документ_(DOMNodeType.Document).md) - не может быть импортирован;
- [ОпределениеТипаДокумента](ТипУзлаDOM.ОпределениеТипаДокумента_(DOMNodeType.DocumentType).md) - не может быть импортирован;
- [Элемент](ТипУзлаDOM.Элемент_(DOMNodeType.Element).md) - атрибуты с установленным свойством [Указан](АтрибутDOM.Указан_(DOMAttribute.Specified).md) импортируются, для нового узла-элемента создаются атрибуты, имеющие значения по умолчанию;
- [Сущность](ТипУзлаDOM.Сущность_(DOMNodeType.Entity).md) - узлы могут быть импортированы, даже если документ находится в режиме Только для чтения. Свойства [ПубличныйИдентификатор](СущностьDOM.ПубличныйИдентификатор_(DOMEntity.PublicId).md), [СистемныйИдентификатор](СущностьDOM.СистемныйИдентификатор_(DOMEntity.SystemId).md) и [ИмяНотации](СущностьDOM.ИмяНотации_(DOMEntity.NotationName).md) копируются;
- [СсылкаНаСущность](ТипУзлаDOM.СсылкаНаСущность_(DOMNodeType.EntityReference).md) - импортируется только данный узел. Если в данном документе определена сущность с таким же именем, то формируется значение сущности для импортированной ссылки;
- [Нотация](ТипУзлаDOM.Нотация_(DOMNodeType.Notation).md) - узлы могут быть импортированы, даже если документ находится в режиме только для чтения. Свойства [ПубличныйИдентификатор](НотацияDOM.ПубличныйИдентификатор_(DOMNotation.PublicId).md), [СистемныйИдентификатор](НотацияDOM.СистемныйИдентификатор_(DOMNotation.SystemId).md) копируются;
- [ИнструкцияОбработки](ТипУзлаDOM.ИнструкцияОбработки_(DOMNodeType.ProcessingInstruction).md) - копируются свойства [Цель](ИнструкцияОбработкиDOM.Цель_(DOMProcessingInstruction.Target).md) и [Данные](ИнструкцияОбработкиDOM.Данные_(DOMProcessingInstruction.Data).md);
- [Текст](ТипУзлаDOM.Текст_(DOMNodeType.Text).md), [Комментарий](ТипУзлаDOM.Комментарий_(DOMNodeType.Comment).md) - копируются свойства [ТекстHTML.Данные](ТекстHTML.Данные_(HTMLText.Data).md), [КомментарийHTML.Данные](КомментарийHTML.Данные_(HTMLComment.Data).md) и [ТекстHTML.Размер](ТекстHTML.Размер_(HTMLText.Length).md), [КомментарийHTML.Размер](КомментарийHTML.Размер_(HTMLComment.Length).md).

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Примечание:

Причины вызова исключений:

- импортируемые имена содержат символы, недопустимые стандартом XML данного документа.

Использование в версии:

Доступен, начиная с версии 8.2.

---
