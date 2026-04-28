# Расширение табличного поля списка плана счетов

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Прикладные объекты](Прикладные_объекты.md) › [Планы счетов](Планы_счетов.md)

Доступен, начиная с версии 8.0.

Свойства:

[АвтоОбновление (AutoRefresh)](Расширение_табличного_поля_списка_плана_счетов.АвтоОбновление_(Chart_of_accounts_list_table_box_extension.AutoRefresh).md)  
[ВосстанавливатьТекущуюСтроку (RestoreCurrentRow)](Расширение_табличного_поля_списка_плана_счетов.ВосстанавливатьТекущуюСтроку_(Chart_of_accounts_list_table_box_extension.RestoreCurrentRow).md)  
[Дерево (Tree)](Расширение_табличного_поля_списка_плана_счетов.Дерево_(Chart_of_accounts_list_table_box_extension.Tree).md)  
[ИерархическийПросмотр (HierarchicalView)](Расширение_табличного_поля_списка_плана_счетов.ИерархическийПросмотр_(Chart_of_accounts_list_table_box_extension.HierarchicalView).md)  
[ИзменятьАвтоОбновление (ChangeAutoRefresh)](Расширение_табличного_поля_списка_плана_счетов.ИзменятьАвтоОбновление_(Chart_of_accounts_list_table_box_extension.ChangeAutoRefresh).md)  
[ИзменятьИерархическийПросмотр (ChangeHierarchicalView)](Расширение_табличного_поля_списка_плана_счетов.ИзменятьИерархическийПросмотр_(Chart_of_accounts_list_table_box_extension.ChangeHierarchicalView).md)  
[ИзменятьСпособРедактирования (ChangeEditingMode)](Расширение_табличного_поля_списка_плана_счетов.ИзменятьСпособРедактирования_(Chart_of_accounts_list_table_box_extension.ChangeEditingMode).md)  
[ИзменятьТекущегоРодителя (ChangeCurrentParent)](Расширение_табличного_поля_списка_плана_счетов.ИзменятьТекущегоРодителя_(Chart_of_accounts_list_table_box_extension.ChangeCurrentParent).md)  
[НастройкаОтбора (FilterSettings)](Расширение_табличного_поля_списка_плана_счетов.НастройкаОтбора_(Chart_of_accounts_list_table_box_extension.FilterSettings).md)  
[НастройкаПорядка (OrderSetting)](Расширение_табличного_поля_списка_плана_счетов.НастройкаПорядка_(Chart_of_accounts_list_table_box_extension.OrderSetting).md)  
[ПериодАвтоОбновления (AutoRefreshPeriod)](Расширение_табличного_поля_списка_плана_счетов.ПериодАвтоОбновления_(Chart_of_accounts_list_table_box_extension.AutoRefreshPeriod).md)  
[ПроверкаОтображенияНовойСтроки (NewRowShowCheck)](Расширение_табличного_поля_списка_плана_счетов.ПроверкаОтображенияНовойСтроки_(Chart_of_accounts_list_table_box_extension.NewRowShowCheck).md)  
[РодительВерхнегоУровня (TopLevelParent)](Расширение_табличного_поля_списка_плана_счетов.РодительВерхнегоУровня_(Chart_of_accounts_list_table_box_extension.TopLevelParent).md)  
[СпособРедактирования (EditType)](Расширение_табличного_поля_списка_плана_счетов.СпособРедактирования_(Chart_of_accounts_list_table_box_extension.EditType).md)  

События:

[ПередИзменениемРодителя (BeforeParentChange)](Расширение_табличного_поля_списка_плана_счетов.ПередИзменениемРодителя_(Chart_of_accounts_list_table_box_extension.BeforeParentChange).md)  
[ПередНачаломДобавления (BeforeAddLine)](Расширение_табличного_поля_списка_плана_счетов.ПередНачаломДобавления_(Chart_of_accounts_list_table_box_extension.BeforeAddLine).md)  
[ПередРазворачиванием (BeforeExpand)](Расширение_табличного_поля_списка_плана_счетов.ПередРазворачиванием_(Chart_of_accounts_list_table_box_extension.BeforeExpand).md)  
[ПередСворачиванием (BeforeCollapse)](Расширение_табличного_поля_списка_плана_счетов.ПередСворачиванием_(Chart_of_accounts_list_table_box_extension.BeforeCollapse).md)  
[ПередУстановкойПометкиУдаления (BeforeSetDeletionMark)](Расширение_табличного_поля_списка_плана_счетов.ПередУстановкойПометкиУдаления_(Chart_of_accounts_list_table_box_extension.BeforeSetDeletionMark).md)  

Описание:

Дополнительные свойства и события элемента управления [ТабличноеПоле](ТабличноеПоле_(TableBox).md) для списка счетов. Для данного расширения свойство [ТекущаяСтрока](ТабличноеПоле.ТекущаяСтрока_(TableBox.CurrentRow).md) содержит значение типа [ПланСчетовСсылка.](ПланСчетовСсылка.Имя_плана_счетов_(ChartOfAccountsRef.Chart_of_accounts_name).md)<[Имя плана счетов](ПланСчетовСсылка.Имя_плана_счетов_(ChartOfAccountsRef.Chart_of_accounts_name).md)>. Свойство [ТекущиеДанные](ТабличноеПоле.ТекущиеДанные_(TableBox.CurrentData).md) содержит коллекцию значений данных строки, набор значений которой определяется колонками объекта [ПланСчетовСписок.](ПланСчетовСписок.Имя_плана_счетов_(ChartOfAccountsList.Chart_of_accounts_name).md)<[Имя плана счетов](ПланСчетовСписок.Имя_плана_счетов_(ChartOfAccountsList.Chart_of_accounts_name).md)>.

Доступность:

Толстый клиент.

Использование в версии:

Доступен, начиная с версии 8.0.

---

<!-- toc:start -->
## Оглавление

### Подразделы (2)

- [Свойства (14 страниц)](Расширение_табличного_поля_списка_плана_счетов__Свойства.md)
- [События (5 страниц)](Расширение_табличного_поля_списка_плана_счетов__События.md)
<!-- toc:end -->
