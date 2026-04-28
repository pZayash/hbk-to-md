# Расширение табличного поля списка справочника

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Прикладные объекты](Прикладные_объекты.md) › [Справочники](Справочники.md)

Доступен, начиная с версии 8.0.

Свойства:

[Автонумерация (Autonumeration)](Расширение_табличного_поля_списка_справочника.Автонумерация_(Catalog_list_table_box_extension.Autonumeration).md)  
[АвтоОбновление (AutoRefresh)](Расширение_табличного_поля_списка_справочника.АвтоОбновление_(Catalog_list_table_box_extension.AutoRefresh).md)  
[ВосстанавливатьТекущуюСтроку (RestoreCurrentRow)](Расширение_табличного_поля_списка_справочника.ВосстанавливатьТекущуюСтроку_(Catalog_list_table_box_extension.RestoreCurrentRow).md)  
[Дерево (Tree)](Расширение_табличного_поля_списка_справочника.Дерево_(Catalog_list_table_box_extension.Tree).md)  
[ИерархическийПросмотр (HierarchicalView)](Расширение_табличного_поля_списка_справочника.ИерархическийПросмотр_(Catalog_list_table_box_extension.HierarchicalView).md)  
[ИзменятьАвтоОбновление (ChangeAutoRefresh)](Расширение_табличного_поля_списка_справочника.ИзменятьАвтоОбновление_(Catalog_list_table_box_extension.ChangeAutoRefresh).md)  
[ИзменятьИерархическийПросмотр (ChangeHierarchicalView)](Расширение_табличного_поля_списка_справочника.ИзменятьИерархическийПросмотр_(Catalog_list_table_box_extension.ChangeHierarchicalView).md)  
[ИзменятьСпособРедактирования (ChangeEditingMode)](Расширение_табличного_поля_списка_справочника.ИзменятьСпособРедактирования_(Catalog_list_table_box_extension.ChangeEditingMode).md)  
[ИзменятьТекущегоРодителя (ChangeCurrentParent)](Расширение_табличного_поля_списка_справочника.ИзменятьТекущегоРодителя_(Catalog_list_table_box_extension.ChangeCurrentParent).md)  
[НастройкаОтбора (FilterSettings)](Расширение_табличного_поля_списка_справочника.НастройкаОтбора_(Catalog_list_table_box_extension.FilterSettings).md)  
[НастройкаПорядка (OrderSetting)](Расширение_табличного_поля_списка_справочника.НастройкаПорядка_(Catalog_list_table_box_extension.OrderSetting).md)  
[ПериодАвтоОбновления (AutoRefreshPeriod)](Расширение_табличного_поля_списка_справочника.ПериодАвтоОбновления_(Catalog_list_table_box_extension.AutoRefreshPeriod).md)  
[ПроверкаОтображенияНовойСтроки (NewRowShowCheck)](Расширение_табличного_поля_списка_справочника.ПроверкаОтображенияНовойСтроки_(Catalog_list_table_box_extension.NewRowShowCheck).md)  
[ПросмотрГруппИЭлементов (ViewFoldersAndItems)](Расширение_табличного_поля_списка_справочника.ПросмотрГруппИЭлементов_(Catalog_list_table_box_extension.ViewFoldersAndItems).md)  
[РодительВерхнегоУровня (TopLevelParent)](Расширение_табличного_поля_списка_справочника.РодительВерхнегоУровня_(Catalog_list_table_box_extension.TopLevelParent).md)  
[СпособРедактирования (EditType)](Расширение_табличного_поля_списка_справочника.СпособРедактирования_(Catalog_list_table_box_extension.EditType).md)  

События:

[ПередИзменениемРодителя (BeforeParentChange)](Расширение_табличного_поля_списка_справочника.ПередИзменениемРодителя_(Catalog_list_table_box_extension.BeforeParentChange).md)  
[ПередНачаломДобавления (BeforeAddLine)](Расширение_табличного_поля_списка_справочника.ПередНачаломДобавления_(Catalog_list_table_box_extension.BeforeAddLine).md)  
[ПередРазворачиванием (BeforeExpand)](Расширение_табличного_поля_списка_справочника.ПередРазворачиванием_(Catalog_list_table_box_extension.BeforeExpand).md)  
[ПередСворачиванием (BeforeCollapse)](Расширение_табличного_поля_списка_справочника.ПередСворачиванием_(Catalog_list_table_box_extension.BeforeCollapse).md)  
[ПередУстановкойПометкиУдаления (BeforeSetDeletionMark)](Расширение_табличного_поля_списка_справочника.ПередУстановкойПометкиУдаления_(Catalog_list_table_box_extension.BeforeSetDeletionMark).md)  

Описание:

Дополнительные свойства и события элемента управления [ТабличноеПоле](ТабличноеПоле_(TableBox).md) для списка справочника. Для данного расширения свойство [ТекущаяСтрока](ТабличноеПоле.ТекущаяСтрока_(TableBox.CurrentRow).md) содержит значение типа [СправочникСсылка.](СправочникСсылка.Имя_справочника_(CatalogRef.Catalog_name).md)<[Имя справочника](СправочникСсылка.Имя_справочника_(CatalogRef.Catalog_name).md)>. Свойство [ТекущиеДанные](ТабличноеПоле.ТекущиеДанные_(TableBox.CurrentData).md) содержит коллекцию значений данных строки, набор значений которой определяется колонками объекта [СправочникСписок.](СправочникСписок.Имя_справочника_(CatalogList.Catalog_name).md)<[Имя справочника](СправочникСписок.Имя_справочника_(CatalogList.Catalog_name).md)>.

Доступность:

Толстый клиент.

См. также:

[КолонкаТабличногоПоля](КолонкаТабличногоПоля_(TableBoxColumn).md), свойство [ОтображатьИерархию](КолонкаТабличногоПоля.ОтображатьИерархию_(TableBoxColumn.ShowHierarchy).md)  

Использование в версии:

Доступен, начиная с версии 8.0.

---

<!-- toc:start -->
## Оглавление

### Подразделы (2)

- [Свойства (16 страниц)](Расширение_табличного_поля_списка_справочника__Свойства.md)
- [События (5 страниц)](Расширение_табличного_поля_списка_справочника__События.md)
<!-- toc:end -->
