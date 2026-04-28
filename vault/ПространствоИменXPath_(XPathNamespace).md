# ПространствоИменXPath

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [DOM](DOM-2.md)

Доступен, начиная с версии 8.1.

Свойства:

[URIПространстваИмен (NamespaceURI)](ПространствоИменXPath.URIПространстваИмен_(XPathNamespace.NamespaceURI).md)  
[Атрибуты (Attributes)](ПространствоИменXPath.Атрибуты_(XPathNamespace.Attributes).md)  
[БазовыйURI (BaseURI)](ПространствоИменXPath.БазовыйURI_(XPathNamespace.BaseURI).md)  
[ДокументВладелец (OwnerDocument)](ПространствоИменXPath.ДокументВладелец_(XPathNamespace.OwnerDocument).md)  
[ДочерниеУзлы (ChildNodes)](ПространствоИменXPath.ДочерниеУзлы_(XPathNamespace.ChildNodes).md)  
[ЗначениеУзла (NodeValue)](ПространствоИменXPath.ЗначениеУзла_(XPathNamespace.NodeValue).md)  
[ИмяУзла (NodeName)](ПространствоИменXPath.ИмяУзла_(XPathNamespace.NodeName).md)  
[ЛокальноеИмя (LocalName)](ПространствоИменXPath.ЛокальноеИмя_(XPathNamespace.LocalName).md)  
[ПервыйДочерний (FirstChild)](ПространствоИменXPath.ПервыйДочерний_(XPathNamespace.FirstChild).md)  
[ПоследнийДочерний (LastChild)](ПространствоИменXPath.ПоследнийДочерний_(XPathNamespace.LastChild).md)  
[ПредыдущийСоседний (PreviousSibling)](ПространствоИменXPath.ПредыдущийСоседний_(XPathNamespace.PreviousSibling).md)  
[Префикс (Prefix)](ПространствоИменXPath.Префикс_(XPathNamespace.Prefix).md)  
[РодительскийУзел (ParentNode)](ПространствоИменXPath.РодительскийУзел_(XPathNamespace.ParentNode).md)  
[СледующийСоседний (NextSibling)](ПространствоИменXPath.СледующийСоседний_(XPathNamespace.NextSibling).md)  
[ТекстовоеСодержимое (TextContent)](ПространствоИменXPath.ТекстовоеСодержимое_(XPathNamespace.TextContent).md)  
[ТипУзла (NodeType)](ПространствоИменXPath.ТипУзла_(XPathNamespace.NodeType).md)  
[ЭлементВладелец (OwnerElement)](ПространствоИменXPath.ЭлементВладелец_(XPathNamespace.OwnerElement).md)  

Методы:

[ВставитьПеред (InsertBefore)](ПространствоИменXPath.ВставитьПеред_(XPathNamespace.InsertBefore).md)  
[ДобавитьДочерний (AppendChild)](ПространствоИменXPath.ДобавитьДочерний_(XPathNamespace.AppendChild).md)  
[ЕстьАтрибуты (HasAttributes)](ПространствоИменXPath.ЕстьАтрибуты_(XPathNamespace.HasAttributes).md)  
[ЕстьДочерниеУзлы (HasChildNodes)](ПространствоИменXPath.ЕстьДочерниеУзлы_(XPathNamespace.HasChildNodes).md)  
[ЗаменитьДочерний (ReplaceChild)](ПространствоИменXPath.ЗаменитьДочерний_(XPathNamespace.ReplaceChild).md)  
[КлонироватьУзел (CloneNode)](ПространствоИменXPath.КлонироватьУзел_(XPathNamespace.CloneNode).md)  
[НайтиURIПространстваИмен (LookupNamespaceURI)](ПространствоИменXPath.НайтиURIПространстваИмен_(XPathNamespace.LookupNamespaceURI).md)  
[НайтиПрефикс (LookupPrefix)](ПространствоИменXPath.НайтиПрефикс_(XPathNamespace.LookupPrefix).md)  
[Нормализовать (Normalize)](ПространствоИменXPath.Нормализовать_(XPathNamespace.Normalize).md)  
[ПолучитьПользовательскиеДанные (GetUserData)](ПространствоИменXPath.ПолучитьПользовательскиеДанные_(XPathNamespace.GetUserData).md)  
[ПространствоИменПоУмолчанию (IsDefaultNamespace)](ПространствоИменXPath.ПространствоИменПоУмолчанию_(XPathNamespace.IsDefaultNamespace).md)  
[СравнитьПозициюВДокументе (CompareDocumentPosition)](ПространствоИменXPath.СравнитьПозициюВДокументе_(XPathNamespace.CompareDocumentPosition).md)  
[УдалитьДочерний (RemoveChild)](ПространствоИменXPath.УдалитьДочерний_(XPathNamespace.RemoveChild).md)  
[УзелИдентичен (IsSameNode)](ПространствоИменXPath.УзелИдентичен_(XPathNamespace.IsSameNode).md)  
[УзелРавен (IsEqualNode)](ПространствоИменXPath.УзелРавен_(XPathNamespace.IsEqualNode).md)  
[УстановитьПользовательскиеДанные (SetUserData)](ПространствоИменXPath.УстановитьПользовательскиеДанные_(XPathNamespace.SetUserData).md)  

Описание:

Специализированный узел DOM. Может появляться только в результате вычисления выражения XPath. Представляет собой узел объявления соответствия URI пространства имен. Узел пространства имен является узлом только для чтения. Все попытки изменения, добавления и удаления узла приводят к вызову исключения.  
Все атрибуты узла DOM, не описанные ниже, имеют либо значение [Ложь](lang__def_BooleanFalse.md), либо [Неопределено](lang__def_Undefined.md):

- [ПространствоИменXPath.ДокументВладелец](ПространствоИменXPath.ДокументВладелец_(XPathNamespace.OwnerDocument).md) - (одноименные атрибуты разных объектов) соответствует документу-владельцу элемента-владельца данного узла;
- [ПространствоИменXPath.ИмяУзла](ПространствоИменXPath.ИмяУзла_(XPathNamespace.NodeName).md) - (одноименные атрибуты разных объектов) всегда равен "#namespace";
- [ПространствоИменXPath.Префикс](ПространствоИменXPath.Префикс_(XPathNamespace.Prefix).md) - (одноименные атрибуты разных объектов) префикс пространства имен, представляемого данным узлом;
- [ПространствоИменXPath.ЛокальноеИмя](ПространствоИменXPath.ЛокальноеИмя_(XPathNamespace.LocalName).md) - (одноименные атрибуты разных объектов) то же, что и [ПространствоИменXPath.Префикс](ПространствоИменXPath.Префикс_(XPathNamespace.Prefix).md);
- [ПространствоИменXPath.ТипУзла](ПространствоИменXPath.ТипУзла_(XPathNamespace.NodeType).md) - (одноименные атрибуты разных объектов) [ПространствоИменXPath](ПространствоИменXPath_(XPathNamespace).md);
- [ПространствоИменXPath.URIПространстваИмен](ПространствоИменXPath.URIПространстваИмен_(XPathNamespace.NamespaceURI).md) - URI пространства имен, представляемого данным узлом;
- [ПространствоИменXPath.ЗначениеУзла](ПространствоИменXPath.ЗначениеУзла_(XPathNamespace.NodeValue).md) - (одноименные атрибуты разных объектов) то же, что и [ПространствоИменXPath.URIПространстваИмен](ПространствоИменXPath.URIПространстваИмен_(XPathNamespace.NamespaceURI).md) (одноименные атрибуты разных объектов);
- [АдаптироватьУзел](ДокументDOM.АдаптироватьУзел_(DOMDocument.AdoptNode).md), [ПространствоИменXPath.КлонироватьУзел](ПространствоИменXPath.КлонироватьУзел_(XPathNamespace.CloneNode).md) и [ИмпортироватьУзел](ДокументDOM.ИмпортироватьУзел_(DOMDocument.ImportNode).md) - не поддерживаются и вызывают исключения.

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.

Использование в версии:

Доступен, начиная с версии 8.1.

---

<!-- toc:start -->
## Оглавление

### Подразделы (2)

- [Методы (16 страниц)](ПространствоИменXPath__Методы.md)
- [Свойства (17 страниц)](ПространствоИменXPath__Свойства.md)
<!-- toc:end -->
