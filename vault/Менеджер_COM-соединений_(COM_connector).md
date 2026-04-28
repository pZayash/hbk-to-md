# Менеджер COM-соединений

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Средства интеграции и администрирования](Средства_интеграции_и_администрирования.md) › [Менеджер COM-соединений](Менеджер_COM-соединений.md)

Доступен, начиная с версии 8.2.

Свойства:

[HighBoundDefault (HighBoundDefault)](Менеджер_COM-соединений.HighBoundDefault_(COM_connector.HighBoundDefault).md)  
[LowBoundDefault (LowBoundDefault)](Менеджер_COM-соединений.LowBoundDefault_(COM_connector.LowBoundDefault).md)  
[MaxConnections (MaxConnections)](Менеджер_COM-соединений.MaxConnections_(COM_connector.MaxConnections).md)  
[PoolCapacity (PoolCapacity)](Менеджер_COM-соединений.PoolCapacity_(COM_connector.PoolCapacity).md)  
[PoolTimeout (PoolTimeout)](Менеджер_COM-соединений.PoolTimeout_(COM_connector.PoolTimeout).md)  
[RAgentPortDefault (RAgentPortDefault)](Менеджер_COM-соединений.RAgentPortDefault_(COM_connector.RAgentPortDefault).md)  
[RMngrPortDefault (RMngrPortDefault)](Менеджер_COM-соединений.RMngrPortDefault_(COM_connector.RMngrPortDefault).md)  

Методы:

[Connect (Connect)](Менеджер_COM-соединений.Connect_(COM_connector.Connect).md)  
[ConnectAgent (ConnectAgent)](Менеджер_COM-соединений.ConnectAgent_(COM_connector.ConnectAgent).md)  
[ConnectWorkingProcess (ConnectWorkingProcess)](Менеджер_COM-соединений.ConnectWorkingProcess_(COM_connector.ConnectWorkingProcess).md)  

Описание:

С помощью данного объекта выполняется установка внешнего соединения с информационной базой 1С:Предприятия 8 и администрирование кластера серверов. С помощью одного экземпляра объекта может быть установлено неограниченное число соединений.   
Установка соединения с информационной базой 1С:Предприятия 8 осуществляется с помощью метода [Connect](Менеджер_COM-соединений.Connect_(COM_connector.Connect).md).  
Администрирование кластера серверов выполняется с помощью методов [ConnectAgent](Менеджер_COM-соединений.ConnectAgent_(COM_connector.ConnectAgent).md) и [ConnectWorkingProcess](Менеджер_COM-соединений.ConnectWorkingProcess_(COM_connector.ConnectWorkingProcess).md).

Доступность:

Интеграция.

Пример:

|  |
| --- |
| // Пример создания объекта  Соединитель = Новый COMObject("V83.COMConnector"); |

Использование в версии:

Доступен, начиная с версии 8.2.

---

<!-- toc:start -->
## Оглавление

### Подразделы (2)

- [Методы (3 страниц)](Менеджер_COM-соединений__Методы.md)
- [Свойства (7 страниц)](Менеджер_COM-соединений__Свойства.md)
<!-- toc:end -->
