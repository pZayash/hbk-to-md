# ЧтениеJSON.ОткрытьПоток

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [JSON](JSON-2.md) › [ЧтениеJSON](ЧтениеJSON_(JSONReader).md) › [Методы](ЧтениеJSON__Методы.md)

ЧтениеJSON (JSONReader)

ОткрытьПоток (OpenStream)

Доступен, начиная с версии 8.3.10.

Синтаксис:

ОткрытьПоток(<Поток>, <Кодировка>)

Параметры:

<Поток> (обязательный)

Тип: [Поток](Поток_(Stream).md), [ПотокВПамяти](ПотокВПамяти_(MemoryStream).md), [ФайловыйПоток](ФайловыйПоток_(FileStream).md).   
Поток для чтения.

<Кодировка> (необязательный)

Тип: [Строка](lang__def_String.md), [КодировкаТекста](КодировкаТекста_(TextEncoding).md).   
Позволяет задать кодировку текста во входном потоке.  
Следует указывать для потоков в кодировках:

- Big5 (Big5)
- UTF-32 (UTF-32)
- UTF-32BE (UTF-32BE)
- UTF-32LE (UTF-32LE)
- UTF32\_PlatformEndian (UTF32\_PlatformEndian)
- UTF32\_OppositeEndian (UTF32\_OppositeEndian)
- SCSU (SCSU)
- BOCU-1 (BOCU-1)
- US-ASCII (US-ASCII)
- ISO-8859-1 (ISO-8859-1)
- iso-8859-13 (iso-8859-13)
- iso-8859-15 (iso-8859-15)
- iso-8859-2 (iso-8859-2)
- iso-8859-3 (iso-8859-3)
- iso-8859-4 (iso-8859-4)
- iso-8859-6 (iso-8859-6)
- iso-8859-7 (iso-8859-7)
- iso-8859-8 (iso-8859-8)
- iso-8859-9 (iso-8859-9)
- GB\_2312-80 (GB\_2312-80)
- cp437 (cp437)
- cp737 (cp737)
- cp775 (cp775)
- cp850 (cp850)
- cp851 (cp851)
- cp852 (cp852)
- cp856 (cp856)
- cp857 (cp857)
- cp858 (cp858)
- cp860 (cp860)
- cp861 (cp861)
- cp862 (cp862)
- cp863 (cp863)
- cp864 (cp864)
- cp865 (cp865)
- CP868 (CP868)
- cp869 (cp869)
- cp874 (cp874)
- cp875 (cp875)
- cp922 (cp922)
- cp930 (cp930)
- cp933 (cp933)
- cp935 (cp935)
- cp937 (cp937)
- cp939 (cp939)
- cp1006 (cp1006)
- cp1025 (cp1025)
- cp1097 (cp1097)
- cp1098 (cp1098)
- cp1112 (cp1112)
- cp1122 (cp1122)
- cp1123 (cp1123)
- windows-874 (windows-874)
- windows-950 (windows-950)
- windows-1250 (windows-1250)
- windows-1252 (windows-1252)
- windows-1253 (windows-1253)
- windows-1254 (windows-1254)
- windows-1255 (windows-1255)
- windows-1256 (windows-1256)
- windows-1257 (windows-1257)
- windows-1258 (windows-1258)
- macintosh (macintosh)
- x-mac-greek (x-mac-greek)
- x-mac-centraleurroman (x-mac-centraleurroman)
- x-mac-turkish (x-mac-turkish)
- hp-roman8 (hp-roman8)
- Adobe-Standard-Encoding (Adobe-Standard-Encoding)
- ISO-2022-KR (ISO-2022-KR)
- ISO-2022-CN (ISO-2022-CN)
- ISO-2022-CN-EXT (ISO-2022-CN-EXT)
- HZ-GB-2312 (HZ-GB-2312)
- windows-57002 (windows-57002)
- windows-57003 (windows-57003)
- windows-57004 (windows-57004)
- windows-57005 (windows-57005)
- windows-57007 (windows-57007)
- windows-57008 (windows-57008)
- windows-57009 (windows-57009)
- windows-57010 (windows-57010)
- windows-57011 (windows-57011)
- ebcdic-ar (ebcdic-ar)
- ebcdic-de (ebcdic-de)
- ebcdic-dk (ebcdic-dk)
- ebcdic-he (ebcdic-he)
- ebcdic-xml-us (ebcdic-xml-us)
- IBM037 (IBM037)
- IBM278 (IBM278)
- IBM280 (IBM280)
- IBM284 (IBM284)
- IBM285 (IBM285)
- IBM290 (IBM290)
- IBM297 (IBM297)
- IBM367 (IBM367)
- IBM420 (IBM420)
- IBM424 (IBM424)
- IBM500 (IBM500)
- ibm-803 (ibm-803)
- IBM-Thai (IBM-Thai)
- ibm-867 (ibm-867)
- IBM870 (IBM870)
- IBM871 (IBM871)
- ibm-901 (ibm-901)
- ibm-902 (ibm-902)
- IBM918 (IBM918)
- ibm-971 (ibm-971)
- IBM1026 (IBM1026)
- ibm-1129 (ibm-1129)
- IBM1047 (IBM1047)
- ibm-1130 (ibm-1130)
- ibm-1132 (ibm-1132)
- ibm-1133 (ibm-1133)
- ibm-1137 (ibm-1137)
- IBM01140 (IBM01140)
- IBM01141 (IBM01141)
- IBM01142 (IBM01142)
- IBM01143 (IBM01143)
- IBM01144 (IBM01144)
- IBM01145 (IBM01145)
- IBM01146 (IBM01146)
- IBM01147 (IBM01147)
- IBM01148 (IBM01148)
- IBM01149 (IBM01149)
- ibm-1153 (ibm-1153)
- ibm-1154 (ibm-1154)
- ibm-1155 (ibm-1155)
- ibm-1156 (ibm-1156)
- ibm-1157 (ibm-1157)
- ibm-1158 (ibm-1158)
- ibm-1160 (ibm-1160)
- ibm-1162 (ibm-1162)
- ibm-1164 (ibm-1164)
- ibm-1364 (ibm-1364)
- ibm-1371 (ibm-1371)
- ibm-1388 (ibm-1388)
- ibm-1390 (ibm-1390)
- ibm-1399 (ibm-1399)
- ibm-4899 (ibm-4899)
- ibm-4971 (ibm-4971)
- ibm-4909 (ibm-4909)
- ibm-5123 (ibm-5123)
- ibm-8482 (ibm-8482)
- ibm-16684 (ibm-16684)

.  
Значение по умолчанию: [UTF8](КодировкаТекста.UTF8_(TextEncoding.UTF8).md).

Описание:

Устанавливает поток для чтения JSON данным объектом. Если перед вызовом данного метода уже выполнялось чтение данных JSON из другого файла или строки, то чтение прекращается и объект инициализируется для чтения из указанного потока.

Доступность:

Тонкий клиент, сервер, толстый клиент, внешнее соединение.

Использование в версии:

Доступен, начиная с версии 8.3.10.

---
