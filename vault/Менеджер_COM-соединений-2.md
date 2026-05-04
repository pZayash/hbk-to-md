# Менеджер COM-соединений

**↑** <a href="obsidian://open?file=_index.md">Главная</a> › <a href="obsidian://open?file=_index__Объекты.md">Объекты</a> › <a href="obsidian://open?file=Средства_интеграции_и_администрирования.md">Средства интеграции и администрирования</a> › [Менеджер COM-соединений](Менеджер_COM-соединений.md)

Доступен, начиная с версии 8.2.

Свойства:

[HighBoundDefault (HighBoundDefault)](Менеджер_COM-соединений.HighBoundDefault.md)  
[LowBoundDefault (LowBoundDefault)](Менеджер_COM-соединений.LowBoundDefault.md)  
[MaxConnections (MaxConnections)](Менеджер_COM-соединений.MaxConnections.md)  
[PoolCapacity (PoolCapacity)](Менеджер_COM-соединений.PoolCapacity.md)  
[PoolTimeout (PoolTimeout)](Менеджер_COM-соединений.PoolTimeout.md)  
[RAgentPortDefault (RAgentPortDefault)](Менеджер_COM-соединений.RAgentPortDefault.md)  
[RMngrPortDefault (RMngrPortDefault)](Менеджер_COM-соединений.RMngrPortDefault.md)  

Методы:

[Connect (Connect)](Менеджер_COM-соединений.Connect.md)  
[ConnectAgent (ConnectAgent)](Менеджер_COM-соединений.ConnectAgent.md)  
[ConnectWorkingProcess (ConnectWorkingProcess)](Менеджер_COM-соединений.ConnectWorkingProcess.md)  

Описание:

С помощью данного объекта выполняется установка внешнего соединения с информационной базой 1С:Предприятия 8 и администрирование кластера серверов. С помощью одного экземпляра объекта может быть установлено неограниченное число соединений.   
Установка соединения с информационной базой 1С:Предприятия 8 осуществляется с помощью метода [Connect](Менеджер_COM-соединений.Connect.md).  
Администрирование кластера серверов выполняется с помощью методов [ConnectAgent](Менеджер_COM-соединений.ConnectAgent.md) и [ConnectWorkingProcess](Менеджер_COM-соединений.ConnectWorkingProcess.md).

Доступность:

Интеграция.

Пример:

|  |
| --- |
| // Пример создания объекта  Соединитель = Новый COMObject("V83.COMConnector"); |

Использование в версии:

Доступен, начиная с версии 8.2.

---
