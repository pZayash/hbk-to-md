# ДокументHTML.НайтиПоФильтру

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [HTML](HTML.md) › [ДокументHTML](ДокументHTML_(HTMLDocument).md) › [Методы](ДокументHTML__Методы.md)

ДокументHTML (HTMLDocument)

НайтиПоФильтру (FindByFilter)

Доступен, начиная с версии 8.3.13.

Синтаксис:

НайтиПоФильтру(<Фильтр>)

Параметры:

<Фильтр> (обязательный)

Тип: [Строка](lang__def_String.md).   
Строка, содержащая текст JSON-конфигурации, описывающей узлы, которые будут возвращены.  
[Описание структуры JSON-конфигурации для фильтра](lang__JSONconffilter.md) 

Возвращаемое значение:

Тип: [Массив](Массив_(Array).md).   
Массив ссылок [АтрибутDOM](АтрибутDOM_(DOMAttribute).md), [ДокументDOM](ДокументDOM_(DOMDocument).md), [ЭлементDOM](ЭлементDOM_(DOMElement).md), [ОпределениеТипаДокументаDOM](ОпределениеТипаДокументаDOM_(DOMDocumentType).md), [НотацияDOM](НотацияDOM_(DOMNotation).md), [СущностьDOM](СущностьDOM_(DOMEntity).md), [ФрагментДокументаDOM](ФрагментДокументаDOM_(DOMDocumentFragment).md), [ТекстDOM](ТекстDOM_(DOMText).md), [КомментарийDOM](КомментарийDOM_(DOMComment).md), [СекцияCDATADOM](СекцияCDATADOM_(DOMCDATASection).md), [ИнструкцияОбработкиDOM](ИнструкцияОбработкиDOM_(DOMProcessingInstruction).md), [СсылкаНаСущностьDOM](СсылкаНаСущностьDOM_(DOMEntityReference).md), [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md) на найденные узлы.

Описание:

Выполняет разбор текста формата HTML согласно фильтру, указанному в виде конфигурации формата JSON.

Доступность:

Тонкий клиент, сервер, толстый клиент.

Примечание:

При изменении полученных ссылок на [АтрибутDOM](АтрибутDOM_(DOMAttribute).md), [ДокументDOM](ДокументDOM_(DOMDocument).md), [ЭлементDOM](ЭлементDOM_(DOMElement).md), [ОпределениеТипаДокументаDOM](ОпределениеТипаДокументаDOM_(DOMDocumentType).md), [НотацияDOM](НотацияDOM_(DOMNotation).md), [СущностьDOM](СущностьDOM_(DOMEntity).md), [ФрагментДокументаDOM](ФрагментДокументаDOM_(DOMDocumentFragment).md), [ТекстDOM](ТекстDOM_(DOMText).md), [КомментарийDOM](КомментарийDOM_(DOMComment).md), [СекцияCDATADOM](СекцияCDATADOM_(DOMCDATASection).md), [ИнструкцияОбработкиDOM](ИнструкцияОбработкиDOM_(DOMProcessingInstruction).md), [СсылкаНаСущностьDOM](СсылкаНаСущностьDOM_(DOMEntityReference).md), [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md) меняется HTML-текст, содержащийся в объкте. Таким образом можно изменять загруженный HTML-текст.

См. также:

[СохраняемыеНастройки](objects__catalog230__SavingSettings.md)  

Использование в версии:

Доступен, начиная с версии 8.3.13.

---
