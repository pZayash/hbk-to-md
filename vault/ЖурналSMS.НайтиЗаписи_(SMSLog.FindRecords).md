# ЖурналSMS.НайтиЗаписи

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [Телефония](Телефония-2.md) › [ЖурналSMS](ЖурналSMS_(SMSLog).md) › [Методы](ЖурналSMS__Методы.md)

ЖурналSMS (SMSLog)

НайтиЗаписи (FindRecords)

Доступен, начиная с версии 8.3.11.

Синтаксис:

НайтиЗаписи(<Отбор>)

Параметры:

<Отбор> (необязательный)

Тип: [ОтборКомпоновкиДанных](ОтборКомпоновкиДанных_(DataCompositionFilter).md).   
Задает условия поиска.  
В качестве условий отбора могут быть указаны следующие поля:

- НомераТелефонов – тип массив строк, [Строка](lang__def_String.md). Допускаются виды сравнения:
  - Для массива: [ВСписке](ВидСравненияКомпоновкиДанных.ВСписке_(DataCompositionComparisonType.InList).md), [НеВСписке](ВидСравненияКомпоновкиДанных.НеВСписке_(DataCompositionComparisonType.NotInList).md).
  - Для строки: [Равно](ВидСравненияКомпоновкиДанных.Равно_(DataCompositionComparisonType.Equal).md), [НеРавно](ВидСравненияКомпоновкиДанных.НеРавно_(DataCompositionComparisonType.NotEqual).md), [Содержит](ВидСравненияКомпоновкиДанных.Содержит_(DataCompositionComparisonType.Contains).md), [НеСодержит](ВидСравненияКомпоновкиДанных.НеСодержит_(DataCompositionComparisonType.NotContains).md).
- ДатаПолучения – тип [Дата](lang__def_Date.md). Допускаются виды сравнения: [Больше](ВидСравненияКомпоновкиДанных.Больше_(DataCompositionComparisonType.Greater).md), [Меньше](ВидСравненияКомпоновкиДанных.Меньше_(DataCompositionComparisonType.Less).md), [Равно](ВидСравненияКомпоновкиДанных.Равно_(DataCompositionComparisonType.Equal).md), [БольшеИлиРавно](ВидСравненияКомпоновкиДанных.БольшеИлиРавно_(DataCompositionComparisonType.GreaterOrEqual).md), [МеньшеИлиРавно](ВидСравненияКомпоновкиДанных.МеньшеИлиРавно_(DataCompositionComparisonType.LessOrEqual).md), [НеРавно](ВидСравненияКомпоновкиДанных.НеРавно_(DataCompositionComparisonType.NotEqual).md).
- ДатаОтправки – тип [Дата](lang__def_Date.md). Допускаются виды сравнения: [Больше](ВидСравненияКомпоновкиДанных.Больше_(DataCompositionComparisonType.Greater).md), [Меньше](ВидСравненияКомпоновкиДанных.Меньше_(DataCompositionComparisonType.Less).md), [Равно](ВидСравненияКомпоновкиДанных.Равно_(DataCompositionComparisonType.Equal).md), [БольшеИлиРавно](ВидСравненияКомпоновкиДанных.БольшеИлиРавно_(DataCompositionComparisonType.GreaterOrEqual).md), [МеньшеИлиРавно](ВидСравненияКомпоновкиДанных.МеньшеИлиРавно_(DataCompositionComparisonType.LessOrEqual).md), [НеРавно](ВидСравненияКомпоновкиДанных.НеРавно_(DataCompositionComparisonType.NotEqual).md).
- Текст – тип [Строка](lang__def_String.md). Допускаются виды сравнения: [Равно](ВидСравненияКомпоновкиДанных.Равно_(DataCompositionComparisonType.Equal).md), [НеРавно](ВидСравненияКомпоновкиДанных.НеРавно_(DataCompositionComparisonType.NotEqual).md), [Содержит](ВидСравненияКомпоновкиДанных.Содержит_(DataCompositionComparisonType.Contains).md), [НеСодержит](ВидСравненияКомпоновкиДанных.НеСодержит_(DataCompositionComparisonType.NotContains).md).
- ТипСообщения – тип значение перечисления [ТипSMSСредствТелефонии](ТипSMSСредствТелефонии_(TelephonyToolsSMSType).md). Допускаются виды сравнения: [Равно](ВидСравненияКомпоновкиДанных.Равно_(DataCompositionComparisonType.Equal).md), [НеРавно](ВидСравненияКомпоновкиДанных.НеРавно_(DataCompositionComparisonType.NotEqual).md).
- Прочитано – тип [Булево](lang__Булево_(Boolean).md). Допускаются виды сравнения: [Равно](ВидСравненияКомпоновкиДанных.Равно_(DataCompositionComparisonType.Equal).md), [НеРавно](ВидСравненияКомпоновкиДанных.НеРавно_(DataCompositionComparisonType.NotEqual).md).

Возвращаемое значение:

Тип: [Массив](Массив_(Array).md).   
Массив элементов типа [ЗаписьЖурналаSMS](ЗаписьЖурналаSMS_(SMSLogRecord).md).

Описание:

Выполняет поиск записей в журнале SMS-сообщений, отвечающих заданному отбору.

Доступность:

Мобильный клиент, мобильное приложение (клиент).

Использование в версии:

Доступен, начиная с версии 8.3.11.

---
