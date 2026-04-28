# ЭлементZipФайла

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [ZIP](ZIP-2.md)

Не рекомендуется использовать, начиная с версии 8.3.26.

Рекомендуется использовать:

- [ЭлементФайлаАрхива](ЭлементФайлаАрхива_(ArchiveFileEntry).md)

Доступен, начиная с версии 8.0.

Свойства:

[ВремяИзменения (Modified)](ЭлементZipФайла.ВремяИзменения_(ZipFileEntry.Modified).md)  
[Зашифрован (Encrypted)](ЭлементZipФайла.Зашифрован_(ZipFileEntry.Encrypted).md)  
[Имя (Name)](ЭлементZipФайла.Имя_(ZipFileEntry.Name).md)  
[ИмяБезРасширения (BaseName)](ЭлементZipФайла.ИмяБезРасширения_(ZipFileEntry.BaseName).md)  
[ИсходноеИмя (OriginalName)](ЭлементZipФайла.ИсходноеИмя_(ZipFileEntry.OriginalName).md)  
[ИсходноеИмяБезРасширения (OriginalBaseName)](ЭлементZipФайла.ИсходноеИмяБезРасширения_(ZipFileEntry.OriginalBaseName).md)  
[ИсходноеПолноеИмя (OriginalFullName)](ЭлементZipФайла.ИсходноеПолноеИмя_(ZipFileEntry.OriginalFullName).md)  
[ИсходноеРасширение (OriginalExtension)](ЭлементZipФайла.ИсходноеРасширение_(ZipFileEntry.OriginalExtension).md)  
[ИсходныйПуть (OriginalPath)](ЭлементZipФайла.ИсходныйПуть_(ZipFileEntry.OriginalPath).md)  
[Невидимый (Hidden)](ЭлементZipФайла.Невидимый_(ZipFileEntry.Hidden).md)  
[ПолноеИмя (FullName)](ЭлементZipФайла.ПолноеИмя_(ZipFileEntry.FullName).md)  
[Путь (Path)](ЭлементZipФайла.Путь_(ZipFileEntry.Path).md)  
[РазмерНесжатого (UncompressedSize)](ЭлементZipФайла.РазмерНесжатого_(ZipFileEntry.UncompressedSize).md)  
[РазмерСжатого (CompressedSize)](ЭлементZipФайла.РазмерСжатого_(ZipFileEntry.CompressedSize).md)  
[Расширение (Extension)](ЭлементZipФайла.Расширение_(ZipFileEntry.Extension).md)  
[ТолькоЧтение (ReadOnly)](ЭлементZipФайла.ТолькоЧтение_(ZipFileEntry.ReadOnly).md)  

Описание:

Предназначен для описания элемента в ZIP-файле.  
В именах файлов и папок в архиве запрещено использование символов: > < | ? \* / \ : ". Такие символы будут заменены на символ подчеркивания "\_".  
При этом свойства [ИсходноеИмя](ЭлементZipФайла.ИсходноеИмя_(ZipFileEntry.OriginalName).md), [ИсходноеПолноеИмя](ЭлементZipФайла.ИсходноеПолноеИмя_(ZipFileEntry.OriginalFullName).md), [ИсходноеИмяБезРасширения](ЭлементZipФайла.ИсходноеИмяБезРасширения_(ZipFileEntry.OriginalBaseName).md), [ИсходноеРасширение](ЭлементZipФайла.ИсходноеРасширение_(ZipFileEntry.OriginalExtension).md), [ИсходныйПуть](ЭлементZipФайла.ИсходныйПуть_(ZipFileEntry.OriginalPath).md) будут содержать немодифицированные значения.   
Если в архиве имена файлов дублируются, платформа устранит дублирование при работе с файлами, обеспечив уникальность имен файлов в архиве.

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

См. также:

[ЭлементыZipФайла](ЭлементыZipФайла_(ZipFileEntries).md)  
[ЧтениеZipФайла](ЧтениеZipФайла_(ZipFileReader).md), метод [Извлечь](ЧтениеZipФайла.Извлечь_(ZipFileReader.Extract).md)  
[ЭлементыZipФайла](ЭлементыZipФайла_(ZipFileEntries).md), метод [Найти](ЭлементыZipФайла.Найти_(ZipFileEntries.Find).md)  
[ЭлементыZipФайла](ЭлементыZipФайла_(ZipFileEntries).md), метод [Получить](ЭлементыZipФайла.Получить_(ZipFileEntries.Get).md)  

Использование в версии:

Доступен, начиная с версии 8.0.

Не рекомендуется использовать, начиная с версии 8.3.26.

Описание изменено в версии 8.3.26.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Свойства (16 страниц)](ЭлементZipФайла__Свойства.md)
<!-- toc:end -->
