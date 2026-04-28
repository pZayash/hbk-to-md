# COMSafeArray

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Универсальные коллекции значений](Универсальные_коллекции_значений.md)

Доступен, начиная с версии 8.0.

Методы:

[GetDimensions (GetDimensions)](COMSafeArray.GetDimensions_(COMSafeArray.GetDimensions).md)  
[GetLength (GetLength)](COMSafeArray.GetLength_(COMSafeArray.GetLength).md)  
[GetLowerBound (GetLowerBound)](COMSafeArray.GetLowerBound_(COMSafeArray.GetLowerBound).md)  
[GetType (GetType)](COMSafeArray.GetType_(COMSafeArray.GetType).md)  
[GetUpperBound (GetUpperBound)](COMSafeArray.GetUpperBound_(COMSafeArray.GetUpperBound).md)  
[GetValue (GetValue)](COMSafeArray.GetValue_(COMSafeArray.GetValue).md)  
[IsResizable (IsResizable)](COMSafeArray.IsResizable_(COMSafeArray.IsResizable).md)  
[Resize (Resize)](COMSafeArray.Resize_(COMSafeArray.Resize).md)  
[SetValue (SetValue)](COMSafeArray.SetValue_(COMSafeArray.SetValue).md)  
[Выгрузить (Unload)](COMSafeArray.Выгрузить_(COMSafeArray.Unload).md)  

Конструкторы:

[Из COMSafeArray](COMSafeArray.Из_COMSafeArray.md)  
[Из массива 1](COMSafeArray.Из_массива_1.md)  
[Из массива 2](COMSafeArray.Из_массива_2.md)  
[По типу элемента 1](COMSafeArray.По_типу_элемента_1.md)  
[По типу элемента 2](COMSafeArray.По_типу_элемента_2.md)  

Описание:

Объектная оболочка над многомерным массивом SAFEARRAY из COM. Позволяет создавать и использовать SAFEARRAY для обмена данными между COM-объектами.  
Для передачи массива в качестве параметра метода COM-объекта необходимо построить [COMSafeArray](COMSafeArray_(COMSafeArray).md) нужной размерности с нужным типом элемента и указать построенный [COMSafeArray](COMSafeArray_(COMSafeArray).md) в качестве значения входного параметра. Другие объекты 1С:Предприятия можно использовать в качестве значений входных параметров типа [Массив](Массив_(Array).md) только при наличии исчерпывающей информации о типах параметров в библиотеке типа COM-объекта.  
Результат метода COM-объекта или значение выходного параметра типа [Массив](Массив_(Array).md) всегда представляется объектом [COMSafeArray](COMSafeArray_(COMSafeArray).md).

Доступность:

Тонкий клиент, сервер, толстый клиент, внешнее соединение.

Пример:

|  |
| --- |
| Массив = Новый COMSafeArray("VT\_I4", 2); Массив.SetValue(0, 23); Массив.SetValue(1, 13.5); COMОбъект = Новый COMObject("ExampleCOMObject.ECOMClass"); COMОбъект.ProcessSafeArray(Массив); |

См. также:

[COMSafeArray](COMSafeArray_(COMSafeArray).md), конструктор [Из COMSafeArray](COMSafeArray.Из_COMSafeArray.md)  

Использование в версии:

Доступен, начиная с версии 8.0.

---

<!-- toc:start -->
## Оглавление

### Подразделы (2)

- [Конструкторы (5 страниц)](Универсальные_коллекции_значений__Конструкторы.md)
- [Методы (10 страниц)](Универсальные_коллекции_значений__Методы.md)
<!-- toc:end -->
