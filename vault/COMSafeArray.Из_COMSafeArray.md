# COMSafeArray.Из COMSafeArray

**↑** <a href="obsidian://open?file=_index.md">Главная</a> › <a href="obsidian://open?file=_index__Объекты.md">Объекты</a> › <a href="obsidian://open?file=Универсальные_коллекции_значений.md">Универсальные коллекции значений</a> › [COMSafeArray](COMSafeArray.md)

<!-- signature:start -->
`COMSafeArray`(`<Источник>`: [`COMSafeArray`](COMSafeArray.md))
<!-- signature:end -->

COMSafeArray (COMSafeArray)

Из COMSafeArray

Доступен, начиная с версии 8.0.

Синтаксис:

Новый COMSafeArray(<Источник>)

Параметры:

<Источник> (обязательный)

Тип: [COMSafeArray](COMSafeArray.md).   
[COMSafeArray](COMSafeArray.md), содержимое которого будет скопировано.

Описание:

Создает [COMSafeArray](COMSafeArray.md) и копирует в него данные из другого [COMSafeArray](COMSafeArray.md).

Пример:

|  |
| --- |
| Массив1 = Новый Массив; // заполнение массива Массив1 значениями  // ...  Размер = Новый Массив; Размер.Добавить(2); Размер.Добавить(3); Массив2 = Новый COMSafeArray(Массив1, "VT\_I4", Размер); Массив3 = Новый COMSafeArray(Массив2); |

Использование в версии:

Доступен, начиная с версии 8.0.

---
