# ЭлементФайлаАрхива

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [Файл архива](Файл_архива.md)

Доступен, начиная с версии 8.3.26.

Свойства:

[ВремяИзменения (ModificationTime)](ЭлементФайлаАрхива.ВремяИзменения_(ArchiveFileEntry.ModificationTime).md)  
[Зашифрован (Encrypted)](ЭлементФайлаАрхива.Зашифрован_(ArchiveFileEntry.Encrypted).md)  
[Имя (Name)](ЭлементФайлаАрхива.Имя_(ArchiveFileEntry.Name).md)  
[ИмяБезРасширения (BaseName)](ЭлементФайлаАрхива.ИмяБезРасширения_(ArchiveFileEntry.BaseName).md)  
[ИсходноеИмя (OriginalName)](ЭлементФайлаАрхива.ИсходноеИмя_(ArchiveFileEntry.OriginalName).md)  
[ИсходноеИмяБезРасширения (OriginalBaseName)](ЭлементФайлаАрхива.ИсходноеИмяБезРасширения_(ArchiveFileEntry.OriginalBaseName).md)  
[ИсходноеПолноеИмя (OriginalFullName)](ЭлементФайлаАрхива.ИсходноеПолноеИмя_(ArchiveFileEntry.OriginalFullName).md)  
[ИсходноеРасширение (OriginalExtension)](ЭлементФайлаАрхива.ИсходноеРасширение_(ArchiveFileEntry.OriginalExtension).md)  
[ИсходныйПуть (OriginalPath)](ЭлементФайлаАрхива.ИсходныйПуть_(ArchiveFileEntry.OriginalPath).md)  
[Невидимый (Hidden)](ЭлементФайлаАрхива.Невидимый_(ArchiveFileEntry.Hidden).md)  
[ПолноеИмя (FullName)](ЭлементФайлаАрхива.ПолноеИмя_(ArchiveFileEntry.FullName).md)  
[Путь (Path)](ЭлементФайлаАрхива.Путь_(ArchiveFileEntry.Path).md)  
[РазмерНесжатого (UncompressedSize)](ЭлементФайлаАрхива.РазмерНесжатого_(ArchiveFileEntry.UncompressedSize).md)  
[РазмерСжатого (CompressedSize)](ЭлементФайлаАрхива.РазмерСжатого_(ArchiveFileEntry.CompressedSize).md)  
[Расширение (Extension)](ЭлементФайлаАрхива.Расширение_(ArchiveFileEntry.Extension).md)  
[ТолькоЧтение (ReadOnly)](ЭлементФайлаАрхива.ТолькоЧтение_(ArchiveFileEntry.ReadOnly).md)  

Описание:

Описывает элемент в файле архива.  
В случаях, когда имя файла в архиве содержит символы > < | ? \* / \ : ". , они будут заменены на символ подчеркивания "\_". При этом свойства "[ИсходноеИмя](ЭлементФайлаАрхива.ИсходноеИмя_(ArchiveFileEntry.OriginalName).md), [ИсходноеПолноеИмя](ЭлементФайлаАрхива.ИсходноеПолноеИмя_(ArchiveFileEntry.OriginalFullName).md), [ИсходноеИмяБезРасширения](ЭлементФайлаАрхива.ИсходноеИмяБезРасширения_(ArchiveFileEntry.OriginalBaseName).md), [ИсходноеРасширение](ЭлементФайлаАрхива.ИсходноеРасширение_(ArchiveFileEntry.OriginalExtension).md), [ИсходныйПуть](ЭлементФайлаАрхива.ИсходныйПуть_(ArchiveFileEntry.OriginalPath).md)" будут содержать не модифицированные значения.  
В случае дублирования имен файлов платформа автоматически устранит дублирование при работе с файлами, обеспечив уникальность имен файлов в файле архива.

Доступность:

Тонкий клиент, сервер, толстый клиент, внешнее соединение.

Использование в версии:

Доступен, начиная с версии 8.3.26.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Свойства (16 страниц)](ЭлементФайлаАрхива__Свойства.md)
<!-- toc:end -->
