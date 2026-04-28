# Менеджер кластера

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Средства интеграции и администрирования](Средства_интеграции_и_администрирования.md) › [Менеджер COM-соединений](Менеджер_COM-соединений.md) › [Администрирование кластера серверов](Администрирование_кластера_серверов.md)

Доступен, начиная с версии 8.2.

Свойства:

[Descr (Descr)](Менеджер_кластера.Descr_(IClusterManagerInfo.Descr).md)  
[HostName (HostName)](Менеджер_кластера.HostName_(IClusterManagerInfo.HostName).md)  
[MainManager (MainManager)](Менеджер_кластера.MainManager_(IClusterManagerInfo.MainManager).md)  
[MainPort (MainPort)](Менеджер_кластера.MainPort_(IClusterManagerInfo.MainPort).md)  
[PID (PID)](Менеджер_кластера.PID_(IClusterManagerInfo.PID).md)  

Описание:

Содержит информацию об одном главном или дополнительном менеджере кластера.  
Для данного объекта поддерживается идентичность. Это означает, что полученные разными способами объекты, представляющие один и тот же зарегистрированный менеджер кластера, всегда будут одним и тем же объектом и допускают сравнение на равенство ссылок.  
Может быть получен методом [GetClusterManagers](Соединение_с_агентом_сервера.GetClusterManagers_(IServerAgentConnection.GetClusterManagers).md).

Доступность:

Интеграция.

См. также:

[Сервис кластера](Сервис_кластера_(IClusterServiceInfo).md), свойство [ClusterManagers](Сервис_кластера.ClusterManagers_(IClusterServiceInfo.ClusterManagers).md)  

Использование в версии:

Доступен, начиная с версии 8.2.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Свойства (5 страниц)](Менеджер_кластера__Свойства.md)
<!-- toc:end -->
