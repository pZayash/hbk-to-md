# COMSafeArray

**↑** <a href="obsidian://open?file=_index.md">Главная</a> › <a href="obsidian://open?file=_index__Объекты.md">Объекты</a> › [Универсальные коллекции значений](Универсальные_коллекции_значений.md)

Доступен, начиная с версии 8.0.

Методы:

[GetDimensions (GetDimensions)](COMSafeArray.GetDimensions.md)  
[GetLength (GetLength)](COMSafeArray.GetLength.md)  
[GetLowerBound (GetLowerBound)](COMSafeArray.GetLowerBound.md)  
[GetType (GetType)](COMSafeArray.GetType.md)  
[GetUpperBound (GetUpperBound)](COMSafeArray.GetUpperBound.md)  
[GetValue (GetValue)](COMSafeArray.GetValue.md)  
[IsResizable (IsResizable)](COMSafeArray.IsResizable.md)  
[Resize (Resize)](COMSafeArray.Resize.md)  
[SetValue (SetValue)](COMSafeArray.SetValue.md)  
[Выгрузить (Unload)](COMSafeArray.Выгрузить.md)  

Конструкторы:

[Из COMSafeArray](COMSafeArray.Из_COMSafeArray.md)  
[Из массива 1](COMSafeArray.Из_массива_1.md)  
[Из массива 2](COMSafeArray.Из_массива_2.md)  
[По типу элемента 1](COMSafeArray.По_типу_элемента_1.md)  
[По типу элемента 2](COMSafeArray.По_типу_элемента_2.md)  

Описание:

Объектная оболочка над многомерным массивом SAFEARRAY из COM. Позволяет создавать и использовать SAFEARRAY для обмена данными между COM-объектами.  
Для передачи массива в качестве параметра метода COM-объекта необходимо построить [COMSafeArray](COMSafeArray.md) нужной размерности с нужным типом элемента и указать построенный [COMSafeArray](COMSafeArray.md) в качестве значения входного параметра. Другие объекты 1С:Предприятия можно использовать в качестве значений входных параметров типа [Массив](Массив.md) только при наличии исчерпывающей информации о типах параметров в библиотеке типа COM-объекта.  
Результат метода COM-объекта или значение выходного параметра типа [Массив](Массив.md) всегда представляется объектом [COMSafeArray](COMSafeArray.md).

Доступность:

Тонкий клиент, сервер, толстый клиент, внешнее соединение.

Пример:

|  |
| --- |
| Массив = Новый COMSafeArray("VT\_I4", 2); Массив.SetValue(0, 23); Массив.SetValue(1, 13.5); COMОбъект = Новый COMObject("ExampleCOMObject.ECOMClass"); COMОбъект.ProcessSafeArray(Массив); |

См. также:

[COMSafeArray](COMSafeArray.md), конструктор [Из COMSafeArray](COMSafeArray.Из_COMSafeArray.md)  

Использование в версии:

Доступен, начиная с версии 8.0.

---
