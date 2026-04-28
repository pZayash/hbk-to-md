# COMSafeArray.Из COMSafeArray

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Универсальные коллекции значений](Универсальные_коллекции_значений.md) › [COMSafeArray](COMSafeArray_(COMSafeArray).md) › [Конструкторы](Универсальные_коллекции_значений__Конструкторы.md)

COMSafeArray (COMSafeArray)

Из COMSafeArray

Доступен, начиная с версии 8.0.

Синтаксис:

Новый COMSafeArray(<Источник>)

Параметры:

<Источник> (обязательный)

Тип: [COMSafeArray](COMSafeArray_(COMSafeArray).md).   
[COMSafeArray](COMSafeArray_(COMSafeArray).md), содержимое которого будет скопировано.

Описание:

Создает [COMSafeArray](COMSafeArray_(COMSafeArray).md) и копирует в него данные из другого [COMSafeArray](COMSafeArray_(COMSafeArray).md).

Пример:

|  |
| --- |
| Массив1 = Новый Массив; // заполнение массива Массив1 значениями  // ...  Размер = Новый Массив; Размер.Добавить(2); Размер.Добавить(3); Массив2 = Новый COMSafeArray(Массив1, "VT\_I4", Размер); Массив3 = Новый COMSafeArray(Массив2); |

Использование в версии:

Доступен, начиная с версии 8.0.

---
