# МенеджерПолученияЛицензий

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [Получение лицензий](Получение_лицензий.md)

Доступен, начиная с версии 8.3.20.

Методы:

[АдресЦентраЛицензирования (LicensingCenterAddress)](МенеджерПолученияЛицензий.АдресЦентраЛицензирования_(LicenseAcquisitionManager.LicensingCenterAddress).md)  
[АдресЭлектроннойПочтыЦентраЛицензирования (LicensingCenterEmail)](МенеджерПолученияЛицензий.АдресЭлектроннойПочтыЦентраЛицензирования_(LicenseAcquisitionManager.LicensingCenterEmail).md)  
[ЗагрузитьЗапросНаПолучениеЛицензии (LoadLicenseAcquisitionRequest)](МенеджерПолученияЛицензий.ЗагрузитьЗапросНаПолучениеЛицензии_(LicenseAcquisitionManager.LoadLicenseAcquisitionRequest).md)  
[НомерТелефонаЦентраЛицензирования (LicensingCenterPhoneNumber)](МенеджерПолученияЛицензий.НомерТелефонаЦентраЛицензирования_(LicenseAcquisitionManager.LicensingCenterPhoneNumber).md)  
[ПолучитьДопустимыеСтраны (GetAvailableCountries)](МенеджерПолученияЛицензий.ПолучитьДопустимыеСтраны_(LicenseAcquisitionManager.GetAvailableCountries).md)  
[ПолучитьДоступностьИспользованияЛицензийДляРазработчика (GetDeveloperLicenseUsageAvailability)](МенеджерПолученияЛицензий.ПолучитьДоступностьИспользованияЛицензийДляРазработчика_(LicenseAcquisitionManager.GetDeveloperLicenseUsageAvailability).md)  
[ПолучитьДоступностьПолученияЛицензии (GetLicenseAcquisitionAvailability)](МенеджерПолученияЛицензий.ПолучитьДоступностьПолученияЛицензии_(LicenseAcquisitionManager.GetLicenseAcquisitionAvailability).md)  
[ПолучитьДоступностьЦентраЛицензирования (GetLicensingCenterAvailability)](МенеджерПолученияЛицензий.ПолучитьДоступностьЦентраЛицензирования_(LicenseAcquisitionManager.GetLicensingCenterAvailability).md)  
[ПолучитьДоступныеКлючи (GetAvailableKeys)](МенеджерПолученияЛицензий.ПолучитьДоступныеКлючи_(LicenseAcquisitionManager.GetAvailableKeys).md)  
[ПолучитьЛицензионноеСоглашениеРазработчика (GetDeveloperLicenseAgreement)](МенеджерПолученияЛицензий.ПолучитьЛицензионноеСоглашениеРазработчика_(LicenseAcquisitionManager.GetDeveloperLicenseAgreement).md)  
[ПолучитьЛицензиюАвтоматически (AcquireLicenseAutomatically)](МенеджерПолученияЛицензий.ПолучитьЛицензиюАвтоматически_(LicenseAcquisitionManager.AcquireLicenseAutomatically).md)  
[ПолучитьЛицензиюНаНосителе (AcquireLicenseFromStorageDevice)](МенеджерПолученияЛицензий.ПолучитьЛицензиюНаНосителе_(LicenseAcquisitionManager.AcquireLicenseFromStorageDevice).md)  
[ПолучитьЛицензиюПоТелефону (AcquireLicenseByPhone)](МенеджерПолученияЛицензий.ПолучитьЛицензиюПоТелефону_(LicenseAcquisitionManager.AcquireLicenseByPhone).md)  
[ПолучитьПараметрыПривязкиККомпьютеру (GetComputerFingerprintParameters)](МенеджерПолученияЛицензий.ПолучитьПараметрыПривязкиККомпьютеру_(LicenseAcquisitionManager.GetComputerFingerprintParameters).md)  
[ПредставлениеЦентраЛицензирования (LicensingCenterPresentation)](МенеджерПолученияЛицензий.ПредставлениеЦентраЛицензирования_(LicenseAcquisitionManager.LicensingCenterPresentation).md)  
[СоздатьЗапросНаПолучениеЛицензииНаНосителе (CreateLicenseAcquisitionRequestOnStorageDevice)](МенеджерПолученияЛицензий.СоздатьЗапросНаПолучениеЛицензииНаНосителе_(LicenseAcquisitionManager.CreateLicenseAcquisitionRequestOnStorageDevice).md)  
[СоздатьЗапросНаПолучениеЛицензииПоТелефону (CreateLicenseAcquisitionRequestByPhone)](МенеджерПолученияЛицензий.СоздатьЗапросНаПолучениеЛицензииПоТелефону_(LicenseAcquisitionManager.CreateLicenseAcquisitionRequestByPhone).md)  
[СохранитьЗапросНаПолучениеЛицензии (SaveLicenseAcquisitionRequest)](МенеджерПолученияЛицензий.СохранитьЗапросНаПолучениеЛицензии_(LicenseAcquisitionManager.SaveLicenseAcquisitionRequest).md)  
[СформироватьКонтрольнуюСуммуСтрокиКодаПолученияЛицензии (GenerateLicenseAcquisitionCodeStringChecksum)](МенеджерПолученияЛицензий.СформироватьКонтрольнуюСуммуСтрокиКодаПолученияЛицензии_(LicenseAcquisitionManager.GenerateLicenseAcquisitionCodeStringChecksum).md)  

Описание:

Менеджер получения программных лицензий на запуск платформы "1С:Предприятие" средствами конфигурации.  
Объект может быть получен только из свойства глобального контекста [ПолучениеЛицензий](Глобальный_контекст.ПолучениеЛицензий_(Global_context.LicenseAcquisition).md).

Доступность:

Тонкий клиент, сервер, внешнее соединение.

См. также:

[Глобальный контекст](Глобальный_контекст.md), свойство [ПолучениеЛицензий](Глобальный_контекст.ПолучениеЛицензий_(Global_context.LicenseAcquisition).md)  

Использование в версии:

Доступен, начиная с версии 8.3.20.

Описание изменено в версии 8.3.27.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Методы (19 страниц)](МенеджерПолученияЛицензий__Методы.md)
<!-- toc:end -->
