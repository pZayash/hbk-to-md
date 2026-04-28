# Информационная база

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Средства интеграции и администрирования](Средства_интеграции_и_администрирования.md) › [Менеджер COM-соединений](Менеджер_COM-соединений.md) › [Администрирование кластера серверов](Администрирование_кластера_серверов.md)

Доступен, начиная с версии 8.1.

Свойства:

[ConfigurationUnloadDelayByWorkingProcessWithoutActiveUsers (ConfigurationUnloadDelayByWorkingProcessWithoutActiveUsers)](Информационная_база.ConfigurationUnloadDelayByWorkingProcessWithoutActiveUsers_(IInfoBaseInfo.ConfigurationUnloadDelayByWorkingProcessWithoutActiveUsers).md)  
[DateOffset (DateOffset)](Информационная_база.DateOffset_(IInfoBaseInfo.DateOffset).md)  
[DBMS (DBMS)](Информационная_база.DBMS_(IInfoBaseInfo.DBMS).md)  
[dbName (dbName)](Информационная_база.dbName_(IInfoBaseInfo.dbName).md)  
[dbPassword (dbPassword)](Информационная_база.dbPassword_(IInfoBaseInfo.dbPassword).md)  
[dbServerName (dbServerName)](Информационная_база.dbServerName_(IInfoBaseInfo.dbServerName).md)  
[dbUser (dbUser)](Информационная_база.dbUser_(IInfoBaseInfo.dbUser).md)  
[DeniedFrom (DeniedFrom)](Информационная_база.DeniedFrom_(IInfoBaseInfo.DeniedFrom).md)  
[DeniedMessage (DeniedMessage)](Информационная_база.DeniedMessage_(IInfoBaseInfo.DeniedMessage).md)  
[DeniedParameter (DeniedParameter)](Информационная_база.DeniedParameter_(IInfoBaseInfo.DeniedParameter).md)  
[DeniedTo (DeniedTo)](Информационная_база.DeniedTo_(IInfoBaseInfo.DeniedTo).md)  
[Descr (Descr)](Информационная_база.Descr_(IInfoBaseInfo.Descr).md)  
[DisableLocalSpeechToText (DisableLocalSpeechToText)](Информационная_база.DisableLocalSpeechToText_(IInfoBaseInfo.DisableLocalSpeechToText).md)  
[ExternalSessionManagerConnectionString (ExternalSessionManagerConnectionString)](Информационная_база.ExternalSessionManagerConnectionString_(IInfoBaseInfo.ExternalSessionManagerConnectionString).md)  
[ExternalSessionManagerRequired (ExternalSessionManagerRequired)](Информационная_база.ExternalSessionManagerRequired_(IInfoBaseInfo.ExternalSessionManagerRequired).md)  
[LicenseDistributionAllowed (LicenseDistributionAllowed)](Информационная_база.LicenseDistributionAllowed_(IInfoBaseInfo.LicenseDistributionAllowed).md)  
[Locale (Locale)](Информационная_база.Locale_(IInfoBaseInfo.Locale).md)  
[MaxScheduledJobsStartShiftWithoutActiveUsers (MaxScheduledJobsStartShiftWithoutActiveUsers)](Информационная_база.MaxScheduledJobsStartShiftWithoutActiveUsers_(IInfoBaseInfo.MaxScheduledJobsStartShiftWithoutActiveUsers).md)  
[MinScheduledJobsStartPeriodWithoutActiveUsers (MinScheduledJobsStartPeriodWithoutActiveUsers)](Информационная_база.MinScheduledJobsStartPeriodWithoutActiveUsers_(IInfoBaseInfo.MinScheduledJobsStartPeriodWithoutActiveUsers).md)  
[Name (Name)](Информационная_база.Name_(IInfoBaseInfo.Name).md)  
[PermissionCode (PermissionCode)](Информационная_база.PermissionCode_(IInfoBaseInfo.PermissionCode).md)  
[SafeModeSecurityProfileName (SafeModeSecurityProfileName)](Информационная_база.SafeModeSecurityProfileName_(IInfoBaseInfo.SafeModeSecurityProfileName).md)  
[ScheduledJobsDenied (ScheduledJobsDenied)](Информационная_база.ScheduledJobsDenied_(IInfoBaseInfo.ScheduledJobsDenied).md)  
[SecurityLevel (SecurityLevel)](Информационная_база.SecurityLevel_(IInfoBaseInfo.SecurityLevel).md)  
[SecurityProfileName (SecurityProfileName)](Информационная_база.SecurityProfileName_(IInfoBaseInfo.SecurityProfileName).md)  
[SessionsDenied (SessionsDenied)](Информационная_база.SessionsDenied_(IInfoBaseInfo.SessionsDenied).md)  

Описание:

Содержит параметры информационной базы 1С:Предприятия. Объект может быть построен программно. Для этого необходимо его создать методом [CreateInfoBaseInfo](Соединение_с_рабочим_процессом.CreateInfoBaseInfo_(IWorkingProcessConnection.CreateInfoBaseInfo).md) и заполнить его свойства путем присваивания им новых значений. Уже заполненные объекты могут быть получены методом [GetInfoBases](Соединение_с_рабочим_процессом.GetInfoBases_(IWorkingProcessConnection.GetInfoBases).md). В последнем случае для чтения значений всех их свойств, кроме Name, необходимы административные права.  
Представляет собой объект с интерфейсом IInfoBaseInfo.

Доступность:

Интеграция.

См. также:

[Соединение с агентом сервера](Соединение_с_агентом_сервера_(IServerAgentConnection).md), метод [GetInfoBaseConnections](Соединение_с_агентом_сервера.GetInfoBaseConnections_(IServerAgentConnection.GetInfoBaseConnections).md)  
[Соединение с агентом сервера](Соединение_с_агентом_сервера_(IServerAgentConnection).md), метод [GetInfoBaseLocks](Соединение_с_агентом_сервера.GetInfoBaseLocks_(IServerAgentConnection.GetInfoBaseLocks).md)  
[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [Connect](Соединение_с_рабочим_процессом.Connect_(IWorkingProcessConnection.Connect).md)  
[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [CreateInfoBase](Соединение_с_рабочим_процессом.CreateInfoBase_(IWorkingProcessConnection.CreateInfoBase).md)  
[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [CreateInfoBaseInfo](Соединение_с_рабочим_процессом.CreateInfoBaseInfo_(IWorkingProcessConnection.CreateInfoBaseInfo).md)  
[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [DropInfoBase](Соединение_с_рабочим_процессом.DropInfoBase_(IWorkingProcessConnection.DropInfoBase).md)  
[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [GetInfoBaseConnections](Соединение_с_рабочим_процессом.GetInfoBaseConnections_(IWorkingProcessConnection.GetInfoBaseConnections).md)  
[Соединение с рабочим процессом](Соединение_с_рабочим_процессом_(IWorkingProcessConnection).md), метод [UpdateInfoBase](Соединение_с_рабочим_процессом.UpdateInfoBase_(IWorkingProcessConnection.UpdateInfoBase).md)  

Использование в версии:

Доступен, начиная с версии 8.1.

Описание изменено в версии 8.3.25.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Свойства (26 страниц)](Информационная_база__Свойства.md)
<!-- toc:end -->
