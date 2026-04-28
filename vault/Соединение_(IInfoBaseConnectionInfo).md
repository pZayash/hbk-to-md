# Соединение

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Средства интеграции и администрирования](Средства_интеграции_и_администрирования.md) › [Менеджер COM-соединений](Менеджер_COM-соединений.md) › [Администрирование кластера серверов](Администрирование_кластера_серверов.md)

Доступен, начиная с версии 8.2.

Свойства:

[AppID (AppID)](Соединение.AppID_(IInfoBaseConnectionInfo.AppID).md)  
[blockedByDBMS (blockedByDBMS)](Соединение.blockedByDBMS_(IInfoBaseConnectionInfo.blockedByDBMS).md)  
[bytesAll (bytesAll)](Соединение.bytesAll_(IInfoBaseConnectionInfo.bytesAll).md)  
[bytesLast5Min (bytesLast5Min)](Соединение.bytesLast5Min_(IInfoBaseConnectionInfo.bytesLast5Min).md)  
[callsAll (callsAll)](Соединение.callsAll_(IInfoBaseConnectionInfo.callsAll).md)  
[callsLast5Min (callsLast5Min)](Соединение.callsLast5Min_(IInfoBaseConnectionInfo.callsLast5Min).md)  
[ConnectedAt (ConnectedAt)](Соединение.ConnectedAt_(IInfoBaseConnectionInfo.ConnectedAt).md)  
[ConnID (ConnID)](Соединение.ConnID_(IInfoBaseConnectionInfo.ConnID).md)  
[CurrentServiceName (CurrentServiceName)](Соединение.CurrentServiceName_(IInfoBaseConnectionInfo.CurrentServiceName).md)  
[dbConnMode (dbConnMode)](Соединение.dbConnMode_(IInfoBaseConnectionInfo.dbConnMode).md)  
[dbmsBytesAll (dbmsBytesAll)](Соединение.dbmsBytesAll_(IInfoBaseConnectionInfo.dbmsBytesAll).md)  
[dbmsBytesLast5Min (dbmsBytesLast5Min)](Соединение.dbmsBytesLast5Min_(IInfoBaseConnectionInfo.dbmsBytesLast5Min).md)  
[dbProcInfo (dbProcInfo)](Соединение.dbProcInfo_(IInfoBaseConnectionInfo.dbProcInfo).md)  
[dbProcTook (dbProcTook)](Соединение.dbProcTook_(IInfoBaseConnectionInfo.dbProcTook).md)  
[dbProcTookAt (dbProcTookAt)](Соединение.dbProcTookAt_(IInfoBaseConnectionInfo.dbProcTookAt).md)  
[durationAll (durationAll)](Соединение.durationAll_(IInfoBaseConnectionInfo.durationAll).md)  
[durationAllDBMS (durationAllDBMS)](Соединение.durationAllDBMS_(IInfoBaseConnectionInfo.durationAllDBMS).md)  
[durationAllService (durationAllService)](Соединение.durationAllService_(IInfoBaseConnectionInfo.durationAllService).md)  
[durationCurrent (durationCurrent)](Соединение.durationCurrent_(IInfoBaseConnectionInfo.durationCurrent).md)  
[durationCurrentDBMS (durationCurrentDBMS)](Соединение.durationCurrentDBMS_(IInfoBaseConnectionInfo.durationCurrentDBMS).md)  
[durationCurrentService (durationCurrentService)](Соединение.durationCurrentService_(IInfoBaseConnectionInfo.durationCurrentService).md)  
[durationLast5Min (durationLast5Min)](Соединение.durationLast5Min_(IInfoBaseConnectionInfo.durationLast5Min).md)  
[durationLast5MinDBMS (durationLast5MinDBMS)](Соединение.durationLast5MinDBMS_(IInfoBaseConnectionInfo.durationLast5MinDBMS).md)  
[durationLast5MinService (durationLast5MinService)](Соединение.durationLast5MinService_(IInfoBaseConnectionInfo.durationLast5MinService).md)  
[HostName (HostName)](Соединение.HostName_(IInfoBaseConnectionInfo.HostName).md)  
[IBConnMode (IBConnMode)](Соединение.IBConnMode_(IInfoBaseConnectionInfo.IBConnMode).md)  
[InBytesAll (InBytesAll)](Соединение.InBytesAll_(IInfoBaseConnectionInfo.InBytesAll).md)  
[InBytesCurrent (InBytesCurrent)](Соединение.InBytesCurrent_(IInfoBaseConnectionInfo.InBytesCurrent).md)  
[InBytesLast5Min (InBytesLast5Min)](Соединение.InBytesLast5Min_(IInfoBaseConnectionInfo.InBytesLast5Min).md)  
[MemoryAll (MemoryAll)](Соединение.MemoryAll_(IInfoBaseConnectionInfo.MemoryAll).md)  
[MemoryCurrent (MemoryCurrent)](Соединение.MemoryCurrent_(IInfoBaseConnectionInfo.MemoryCurrent).md)  
[MemoryLast5Min (MemoryLast5Min)](Соединение.MemoryLast5Min_(IInfoBaseConnectionInfo.MemoryLast5Min).md)  
[OutBytesAll (OutBytesAll)](Соединение.OutBytesAll_(IInfoBaseConnectionInfo.OutBytesAll).md)  
[OutBytesCurrent (OutBytesCurrent)](Соединение.OutBytesCurrent_(IInfoBaseConnectionInfo.OutBytesCurrent).md)  
[OutBytesLast5Min (OutBytesLast5Min)](Соединение.OutBytesLast5Min_(IInfoBaseConnectionInfo.OutBytesLast5Min).md)  
[UserName (UserName)](Соединение.UserName_(IInfoBaseConnectionInfo.UserName).md)  

Описание:

Содержит параметры одного соединения клиентского приложения с информационной базой на кластере серверов 1С:Предприятия.   
Представляет собой объект с интерфейсом IInfoBaseConnectionInfo.

Доступность:

Интеграция.

Пример:

|  |
| --- |
| Rem Пример удаления всех соединений (фрагмент на VBScript): Set connector = CreateObject("V83.COMConnector") Set ragent = connector.ConnectAgent("CentralServer") ragent.AuthenticateAgent "CentralAdminName", "Password" clusters = ragent.GetClusters() Set cluster = clusters(0) ragent.Authenticate cluster, "ClusterAdminName", "Password" processes = ragent.GetWorkingProcesses(cluster) Set process0 = processes(0) WorkingAddress = process0.HostName  ":"  process0.MainPort Set server = connector.ConnectWorkingProcess(WorkingAddress) server.AddAuthentication "InfoBaseUserName", "Password" Set ibDesc = server.CreateInfoBaseInfo() ibDesc.Name = "InfoBaseName" connections = server.GetInfoBaseConnections(ibDesc) Dim i For i = LBound(connections) To UBound(connections)     set connection = connections(i)     server.Disconnect connection Next |

См. также:

[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [Disconnect](Соединение_с_рабочим_процессом.Disconnect_(IWorkingProcessConnection.Disconnect).md)  

Использование в версии:

Доступен, начиная с версии 8.2.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Свойства (36 страниц)](Соединение__Свойства.md)
<!-- toc:end -->
