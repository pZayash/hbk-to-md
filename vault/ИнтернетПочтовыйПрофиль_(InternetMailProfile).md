# ИнтернетПочтовыйПрофиль

**↑** [Главная](_index.md) › [Объекты](_index__Объекты.md) › [Общие объекты](Общие_объекты.md) › [Почта](Почта-2.md) › [ИнтернетПочта](ИнтернетПочта.md)

Доступен, начиная с версии 8.0.

Свойства:

[POP3ПередSMTP (POP3BeforeSMTP)](ИнтернетПочтовыйПрофиль.POP3ПередSMTP_(InternetMailProfile.POP3BeforeSMTP).md)  
[АдресСервераIMAP (IMAPServerAddress)](ИнтернетПочтовыйПрофиль.АдресСервераIMAP_(InternetMailProfile.IMAPServerAddress).md)  
[АдресСервераPOP3 (POP3ServerAddress)](ИнтернетПочтовыйПрофиль.АдресСервераPOP3_(InternetMailProfile.POP3ServerAddress).md)  
[АдресСервераSMTP (SMTPServerAddress)](ИнтернетПочтовыйПрофиль.АдресСервераSMTP_(InternetMailProfile.SMTPServerAddress).md)  
[АутентификацияPOP3 (POP3Authentication)](ИнтернетПочтовыйПрофиль.АутентификацияPOP3_(InternetMailProfile.POP3Authentication).md)  
[АутентификацияSMTP (SMTPAuthentication)](ИнтернетПочтовыйПрофиль.АутентификацияSMTP_(InternetMailProfile.SMTPAuthentication).md)  
[АутентификацияПоТокену (TokenAuthentication)](ИнтернетПочтовыйПрофиль.АутентификацияПоТокену_(InternetMailProfile.TokenAuthentication).md)  
[ИспользоватьSSLIMAP (IMAPUseSSL)](ИнтернетПочтовыйПрофиль.ИспользоватьSSLIMAP_(InternetMailProfile.IMAPUseSSL).md)  
[ИспользоватьSSLPOP3 (POP3UseSSL)](ИнтернетПочтовыйПрофиль.ИспользоватьSSLPOP3_(InternetMailProfile.POP3UseSSL).md)  
[ИспользоватьSSLSMTP (SMTPUseSSL)](ИнтернетПочтовыйПрофиль.ИспользоватьSSLSMTP_(InternetMailProfile.SMTPUseSSL).md)  
[Пароль (Password)](ИнтернетПочтовыйПрофиль.Пароль_(InternetMailProfile.Password).md)  
[ПарольIMAP (IMAPPassword)](ИнтернетПочтовыйПрофиль.ПарольIMAP_(InternetMailProfile.IMAPPassword).md)  
[ПарольSMTP (SMTPPassword)](ИнтернетПочтовыйПрофиль.ПарольSMTP_(InternetMailProfile.SMTPPassword).md)  
[Пользователь (User)](ИнтернетПочтовыйПрофиль.Пользователь_(InternetMailProfile.User).md)  
[ПользовательIMAP (IMAPUser)](ИнтернетПочтовыйПрофиль.ПользовательIMAP_(InternetMailProfile.IMAPUser).md)  
[ПользовательSMTP (SMTPUser)](ИнтернетПочтовыйПрофиль.ПользовательSMTP_(InternetMailProfile.SMTPUser).md)  
[ПортIMAP (IMAPPort)](ИнтернетПочтовыйПрофиль.ПортIMAP_(InternetMailProfile.IMAPPort).md)  
[ПортPOP3 (POP3Port)](ИнтернетПочтовыйПрофиль.ПортPOP3_(InternetMailProfile.POP3Port).md)  
[ПортSMTP (SMTPPort)](ИнтернетПочтовыйПрофиль.ПортSMTP_(InternetMailProfile.SMTPPort).md)  
[Таймаут (Timeout)](ИнтернетПочтовыйПрофиль.Таймаут_(InternetMailProfile.Timeout).md)  
[ТокенДоступа (AccessToken)](ИнтернетПочтовыйПрофиль.ТокенДоступа_(InternetMailProfile.AccessToken).md)  
[ТолькоЗащищеннаяАутентификацияIMAP (IMAPSecureAuthenticationOnly)](ИнтернетПочтовыйПрофиль.ТолькоЗащищеннаяАутентификацияIMAP_(InternetMailProfile.IMAPSecureAuthenticationOnly).md)  
[ТолькоЗащищеннаяАутентификацияPOP3 (POP3SecureAuthenticationOnly)](ИнтернетПочтовыйПрофиль.ТолькоЗащищеннаяАутентификацияPOP3_(InternetMailProfile.POP3SecureAuthenticationOnly).md)  
[ТолькоЗащищеннаяАутентификацияSMTP (SMTPSecureAuthenticationOnly)](ИнтернетПочтовыйПрофиль.ТолькоЗащищеннаяАутентификацияSMTP_(InternetMailProfile.SMTPSecureAuthenticationOnly).md)  

Конструкторы:

[По умолчанию](ИнтернетПочтовыйПрофиль.По_умолчанию.md)  

Описание:

Набор свойств для соединения с сервером.

Доступность:

Тонкий клиент, мобильный клиент, сервер, толстый клиент, внешнее соединение, мобильное приложение (клиент), мобильное приложение (сервер), мобильный автономный сервер.   
Сериализуется.

Пример:

|  |
| --- |
| Профиль = Новый ИнтернетПочтовыйПрофиль;  Профиль.АдресСервераPOP3 = POP3Сервер; Профиль.АдресСервераSMTP = SMTPСервер; Если ВремяОжиданияСервера > 0 Тогда     Профиль.Таймаут = ВремяОжиданияСервера; КонецЕсли;  Профиль.Пароль           = Пароль; Профиль.Пользователь     = Логин; Профиль.ПортPOP3         = ПортPOP3; Профиль.ПортSMTP         = ПортSMTP;  Если SMTPАутентификация Тогда     Профиль.ПарольSMTP       = ПарольSMTP;     Профиль.ПользовательSMTP = ЛогинSMTP; КонецЕсли;   ИнтернетПочта = Новый ИнтернетПочта;  Попытка     ИнтернетПочта.Подключиться(Профиль); Исключение     Сообщить(ОписаниеОшибки());     Предупреждение("Произошли ошибки при проверке настроек учетной записи.        |Описание ошибки приведено в окне сообщения.");     Возврат; КонецПопытки; |

См. также:

[ИнтернетПочтовыйПрофиль](ИнтернетПочтовыйПрофиль_(InternetMailProfile).md), свойство [АдресСервераSMTP](ИнтернетПочтовыйПрофиль.АдресСервераSMTP_(InternetMailProfile.SMTPServerAddress).md)  
[ИнтернетПочтовыйПрофиль](ИнтернетПочтовыйПрофиль_(InternetMailProfile).md), свойство [АдресСервераPOP3](ИнтернетПочтовыйПрофиль.АдресСервераPOP3_(InternetMailProfile.POP3ServerAddress).md)  
[ИнтернетПочтовыйПрофиль](ИнтернетПочтовыйПрофиль_(InternetMailProfile).md), свойство [ПортSMTP](ИнтернетПочтовыйПрофиль.ПортSMTP_(InternetMailProfile.SMTPPort).md)  
[ИнтернетПочтовыйПрофиль](ИнтернетПочтовыйПрофиль_(InternetMailProfile).md), свойство [ПортPOP3](ИнтернетПочтовыйПрофиль.ПортPOP3_(InternetMailProfile.POP3Port).md)  
[ИнтернетПочтовыйПрофиль](ИнтернетПочтовыйПрофиль_(InternetMailProfile).md), свойство [Пароль](ИнтернетПочтовыйПрофиль.Пароль_(InternetMailProfile.Password).md)  
[ИнтернетПочта](ИнтернетПочта_(InternetMail).md), метод [Подключиться](ИнтернетПочта.Подключиться_(InternetMail.Logon).md)  

Использование в версии:

Доступен, начиная с версии 8.0.

---

<!-- toc:start -->
## Оглавление

### Подразделы (2)

- [Конструкторы (1 страниц)](ИнтернетПочтовыйПрофиль__Конструкторы.md)
- [Свойства (24 страниц)](ИнтернетПочтовыйПрофиль__Свойства.md)
<!-- toc:end -->
