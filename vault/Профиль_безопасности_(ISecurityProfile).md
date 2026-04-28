# Профиль безопасности

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Средства интеграции и администрирования](Средства_интеграции_и_администрирования.md) › [Менеджер COM-соединений](Менеджер_COM-соединений.md) › [Администрирование кластера серверов](Администрирование_кластера_серверов.md)

Доступен, начиная с версии 8.3.3.

Свойства:

[AddInFullAccess (AddInFullAccess)](Профиль_безопасности.AddInFullAccess_(ISecurityProfile.AddInFullAccess).md)  
[AllModulesExtension (AllModulesExtension)](Профиль_безопасности.AllModulesExtension_(ISecurityProfile.AllModulesExtension).md)  
[COMFullAccess (COMFullAccess)](Профиль_безопасности.COMFullAccess_(ISecurityProfile.COMFullAccess).md)  
[CryptographyAllowed (CryptographyAllowed)](Профиль_безопасности.CryptographyAllowed_(ISecurityProfile.CryptographyAllowed).md)  
[Descr (Descr)](Профиль_безопасности.Descr_(ISecurityProfile.Descr).md)  
[ExternalAppFullAccess (ExternalAppFullAccess)](Профиль_безопасности.ExternalAppFullAccess_(ISecurityProfile.ExternalAppFullAccess).md)  
[FileSystemFullAccess (FileSystemFullAccess)](Профиль_безопасности.FileSystemFullAccess_(ISecurityProfile.FileSystemFullAccess).md)  
[FullPrivilegedMode (PrivilegedModeInSafeModeAllowed)](Профиль_безопасности.FullPrivilegedMode_(ISecurityProfile.PrivilegedModeInSafeModeAllowed).md)  
[InternetFullAccess (InternetFullAccess)](Профиль_безопасности.InternetFullAccess_(ISecurityProfile.InternetFullAccess).md)  
[ModulesAvailableForExtension (ModulesAvailableForExtension)](Профиль_безопасности.ModulesAvailableForExtension_(ISecurityProfile.ModulesAvailableForExtension).md)  
[ModulesNotAvailableForExtension (ModulesNotAvailableForExtension)](Профиль_безопасности.ModulesNotAvailableForExtension_(ISecurityProfile.ModulesNotAvailableForExtension).md)  
[Name (Name)](Профиль_безопасности.Name_(ISecurityProfile.Name).md)  
[PrivilegedModeRoles (RightExtensionDefinitionRoles)](Профиль_безопасности.PrivilegedModeRoles_(ISecurityProfile.RightExtensionDefinitionRoles).md)  
[RightExtension (RightExtension)](Профиль_безопасности.RightExtension_(ISecurityProfile.RightExtension).md)  
[RightExtensionDefinitionRoles (RightExtensionDefinitionRoles)](Профиль_безопасности.RightExtensionDefinitionRoles_(ISecurityProfile.RightExtensionDefinitionRoles).md)  
[SafeModeProfile (SafeModeProfile)](Профиль_безопасности.SafeModeProfile_(ISecurityProfile.SafeModeProfile).md)  
[UnSafeExternalModuleFullAccess (UnSafeExternalModuleFullAccess)](Профиль_безопасности.UnSafeExternalModuleFullAccess_(ISecurityProfile.UnSafeExternalModuleFullAccess).md)  

Описание:

Профиль безопасности информационной базы. Определяет правила изоляции данных и регламентирует возможную внешнюю активность информационной базы.  
С профилем безопасности связаны списки объектов, определяющих различные виды внешней активности:

- [Виртуальный каталог](Виртуальный_каталог_(ISecurityProfileVirtualDirectory).md) - доступ к файлам операционной системы;
- [COM-класс](COM-класс_(ISecurityProfileCOMClass).md) - доступ к COM-объектам;
- [Внешний компонент](Внешний_компонент_(ISecurityProfileAddIn).md) - доступ к внешним компонентам;
- [Внешний модуль](Внешний_модуль_(ISecurityProfileExternalModule).md) - доступ к внешним отчетам и обработкам;
- [Приложение](Приложение_(ISecurityProfileApplication).md) - доступ к приложениям операционной системы;
- [Ресурс интернет](Ресурс_интернет_(ISecurityProfileInternetResource).md) - доступ к ресурсам Интернета.

Доступность:

Интеграция.

Использование в версии:

Доступен, начиная с версии 8.3.3.

---

<!-- toc:start -->
## Оглавление

### Подразделы (1)

- [Свойства (17 страниц)](Профиль_безопасности__Свойства.md)
<!-- toc:end -->
