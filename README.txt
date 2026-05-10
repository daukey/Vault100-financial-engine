this is the general flow of this app.


How will Kasa100 work? (General flow and process overview)

1. Authentication System:

There will be a login layer. Users will log in with their password, and the system will check whether they are a standard user or an admin. Standard users can perform transactions and add data, while admin users can monitor all activities and manage the system.

2. Database Architecture:

Data will be securely stored using SQLite in tables named transactions, users, and categories. Each record will include the amount, date, description, and transaction type (“income-expense”).

3. Financial Transaction Tracking:

The system will track incoming and outgoing money and handle categorization processes (such as classifying expenses as rent, bills, food, etc.). Users can evaluate their expenses by categorizing them.

4. Analysis Screen:

Users will be able to analyze their expenses through visualizations. In addition, the system will directly display the cash inflow and outflow in the register.

5. Export Feature:

Users will be able to generate account statements by selecting a desired date range.





















Kasa100 nasıl çalışacak? (Genel akış, süreç nasıl ilerleyecek?)

1) Kimlik doğrulama sistemi:

Bir giriş katmanı olacak. Giriş yapan kullanıcı şifresi ile giriş yapacak, sistem onun user mi admin mi olduğunu kontrol edecek. Standart kullanıcı(user) işlem yapıp veri ekleyebilirken admin kullanıcı tüm hareketleri izleyebilir ve sistemi yönetir.

2) Veri tabanı mimarisi:

işlemler, kullanicilar, kategoriler isimli tablolarda SQLite kullanılarak veriler güvenli bir biçimde tutulacak. Her girdi miktar, tarih, açıklama ve "gelir-gider" tipleriyle kaydedilir.

3) Finansal işlem takibi:

Giren çıkan takibi, kategorizasyon işlemleri(harcamaları kira, fatura, yemek vs. diye sınıflandırmak) yapılır. Kullanıcı giderlerini kategorize ederek değerlendirebilir.

4) Analiz ekranı:

Kullanıcı harcamalarını görselleştirerek analiz edebilir. Ayrıca sistem kasadaki giren çıkan parayı direkt gösterir. 

5) Dışa aktarma: 

Kullanıcı istediği tarih aralığını seçerek hesap ekstresi alabilir. 
