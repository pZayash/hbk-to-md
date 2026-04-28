# XDTO

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md)

Механизм XDTO позволяет создать модель представления данных (модель типов и значений), которая, с одной стороны, обеспечивает возможность просто и естественно манипулировать данными в среде 1С:Предприятия 8, а с другой стороны, данная модель хорошо приспособлена для прозрачного преобразования данных в другие форматы, главным образом XML.  
  
Для типов, определяемых конфигурацией, имя совпадает с именем типа, определенного в пространстве имен {http://v8.1c.ru/8.1/data/enterprise/current-config}.  
Соответствие имен типов платформы и XDTO указывается в описании объектов.   
Для примитивных типов используется следующее соответствие имен:  
[Булево](lang__Булево_(Boolean).md):   
 {http://www.w3.org/2001/XMLSchema}boolean   
[Дата](lang__def_Date.md):   
 {http://www.w3.org/2001/XMLSchema}date   
 {http://www.w3.org/2001/XMLSchema}dateTime   
 {http://www.w3.org/2001/XMLSchema}time   
[Число](lang__def_Number.md):   
 {http://www.w3.org/2001/XMLSchema}decimal   
 {http://www.w3.org/2001/XMLSchema}double   
 float {http://www.w3.org/2001/XMLSchema}  
[Строка](lang__def_String.md):   
 {http://www.w3.org/2001/XMLSchema}anySimpleType   
 {http://www.w3.org/2001/XMLSchema}anyURI   
 {http://www.w3.org/2001/XMLSchema}duration   
 {http://www.w3.org/2001/XMLSchema}gDay   
 {http://www.w3.org/2001/XMLSchema}gMonth   
 {http://www.w3.org/2001/XMLSchema}gMonthDay   
 {http://www.w3.org/2001/XMLSchema}gYear   
 {http://www.w3.org/2001/XMLSchema}gYearMonth   
 {http://www.w3.org/2001/XMLSchema}NOTATION   
 {http://www.w3.org/2001/XMLSchema}string   
[Тип](lang__def_Type.md):   
 {http://v8.1c.ru/8.1/data/core}Type

---

<!-- toc:start -->
## Оглавление

### Подразделы (17)

- [ВариантXDTO (4 страниц)](ВариантXDTO_(XDTOVariety).md)
- [ЗначениеXDTO (6 страниц)](ЗначениеXDTO_(XDTODataValue).md)
- [КоллекцияЗначенийXDTO (3 страниц)](КоллекцияЗначенийXDTO_(XDTODataValueCollection).md)
- [КоллекцияПакетовXDTO (3 страниц)](КоллекцияПакетовXDTO_(XDTOPackageCollection).md)
- [КоллекцияСвойствXDTO (3 страниц)](КоллекцияСвойствXDTO_(XDTOPropertyCollection).md)
- [КоллекцияТиповЗначенийXDTO (3 страниц)](КоллекцияТиповЗначенийXDTO_(XDTOValueTypeCollection).md)
- [КоллекцияФасетовXDTO (5 страниц)](КоллекцияФасетовXDTO_(XDTOFacetCollection).md)
- [ОбъектXDTO (16 страниц)](ОбъектXDTO_(XDTODataObject).md)
- [ПакетXDTO (8 страниц)](ПакетXDTO_(XDTOPackage).md)
- [ПоследовательностьXDTO (12 страниц)](ПоследовательностьXDTO_(XDTOSequence).md)
- [СвойствоXDTO (14 страниц)](СвойствоXDTO_(XDTOProperty).md)
- [СериализаторXDTO (17 страниц)](СериализаторXDTO_(XDTOSerializer).md)
- [СписокXDTO (11 страниц)](СписокXDTO_(XDTOList).md)
- [ТипЗначенияXDTO (9 страниц)](ТипЗначенияXDTO_(XDTOValueType).md)
- [ТипОбъектаXDTO (12 страниц)](ТипОбъектаXDTO_(XDTOObjectType).md)
- [ФабрикаXDTO (14 страниц)](ФабрикаXDTO_(XDTOFactory).md)
- [ФасетXDTO (3 страниц)](ФасетXDTO_(XDTOFacet).md)
<!-- toc:end -->
