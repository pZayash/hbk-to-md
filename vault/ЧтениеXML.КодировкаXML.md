# ЧтениеXML.КодировкаXML

**↑** <a href="obsidian://open?file=_index.md">Главная</a> › <a href="obsidian://open?file=_index__Объекты.md">Объекты</a> › <a href="obsidian://open?file=Общие_объекты.md">Общие объекты</a> › <a href="obsidian://open?file=objects__catalog63__catalog565.md">XML</a> › [ЧтениеXML](ЧтениеXML.md)

<!-- signature:start -->
`КодировкаXML`: `Строка`
<!-- signature:end -->

ЧтениеXML (XMLReader)

КодировкаXML (XMLEncoding)

Доступен, начиная с версии 8.1.

Использование:

Только чтение.

Описание:

Тип: Строка.   
Кодировка исходного документа XML.  
Содержит значение атрибута encoding объявления XML.   
Если атрибут не указан или объявление не прочитано (отсутствует), то будет возвращена кодировка [UTF8](КодировкаТекста.UTF8.md).

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Примечание:

Поддерживаемые коды кодировок (с учетом правил http://www.w3.org/TR/2004/REC-xml-20040204/#NT-EncName):

- UTF-8
- UTF-16
- UTF-16BE
- UTF-16LE
- ISO-8859-1
- US-ASCII
- gb18030
- iso-8859-2
- iso-8859-3
- iso-8859-4
- iso-8859-5
- iso-8859-6
- iso-8859-7
- iso-8859-8
- iso-8859-9
- iso-8859-13
- iso-8859-15
- Shift\_JIS
- EUC-JP
- Big5
- Big5-HKSCS
- GBK
- GB2312
- GB\_2312-80
- EUC-KR
- KSC\_5601
- windows-949
- windows-874
- cp866
- KOI8-R
- KOI8-U
- windows-1250
- windows-1251
- windows-1252
- windows-1253
- windows-1254
- windows-1255
- windows-1256
- windows-1257
- windows-1258
- macintosh
- x-mac-cyrillic
- ISO-2022-JP
- ISO-2022-KR
- ISO-2022-CN
- ISO-2022-CN-EXT
- HZ-GB-2312

Использование в версии:

Доступен, начиная с версии 8.1.

---
