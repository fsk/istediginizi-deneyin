# E-Commerce Projesi - Test Edilebilecek Problemler

Bu dokümanda, e-commerce projesinde test edilebilecek çeşitli problemler ve senaryolar listelenmiştir.

## 1. Concurrency ve Locking Problemleri

### a) Race Condition - Stock Güncellemesi

- [ ] **Problem:** Aynı anda birden fazla kullanıcı aynı üründen satın almaya çalışırsa, stock kontrolü yetersiz kalabilir.

**Senaryo:**
- `products` tablosunda product_id='abc-123' olan ürünün `stock_quantity`=100
- 150 eşzamanlı order request gelir (her biri 1 adet satın almak istiyor)
- Sadece 100 order başarılı olmalı (`orders` ve `order_items` tablolarına kayıt)
- Diğer 50 order `QuantityNotAvailableException` almalı
- `products` tablosunda `stock_quantity` negatif olmamalı, 0 olmalı


---

### b) Deadlock

- [ ] **Problem:** İki transaction birbirini beklerken deadlock oluşabilir.

**Senaryo:**
- Thread-1: `products` tablosunda product_id='prod-A' olan ürünü lock'la, sonra product_id='prod-B' olan ürünü lock'lamaya çalışır
- Thread-2: `products` tablosunda product_id='prod-B' olan ürünü lock'la, sonra product_id='prod-A' olan ürünü lock'lamaya çalışır
- Her iki thread de birbirini bekler → Deadlock oluşur
- Database deadlock detection devreye girer, bir transaction rollback olur

---

### c) Pessimistic Locking

- [ ] **Problem:** Optimistic locking yerine pessimistic locking kullanılabilir.

**Senaryo:**
- `orders` tablosunda order_id='order-123' olan sipariş için `SELECT FOR UPDATE` ile row-level lock
- Thread-1: Order'ı lock'lar ve `status`='PROCESSING' olarak günceller
- Thread-2: Aynı order'ı güncellemeye çalışır, lock bekler
- Thread-1 commit yapınca lock release olur
- Thread-2 lock'u alır ve işlemine devam eder

---

## 2. Transaction Problemleri

### a) Lost Update

- [ ] **Problem:** İki transaction aynı veriyi okur, her ikisi de günceller, son güncelleme kaybolur.

**Senaryo:**
- `products` tablosunda product_id='abc-123', stock_quantity=100
- Thread-1: Product'ı okur (stock_quantity=100), 10 adet satış yapar, stock_quantity=90 olarak günceller
- Thread-2: Aynı product'ı okur (stock_quantity=100), 5 adet satış yapar, stock_quantity=95 olarak günceller
- Thread-2'nin güncellemesi Thread-1'in güncellemesini ezer → Lost Update
- Son durum: stock_quantity=95 (olması gereken: 85)

---

### b) Dirty Read

- [ ] **Problem:** Bir transaction commit olmadan diğeri okuyabilir.

**Senaryo:**
- `products` tablosunda product_id='abc-123', stock_quantity=100
- READ UNCOMMITTED isolation level ile
- Transaction-1: `products` tablosunda stock_quantity'yi 100'den 50'ye düşürür (henüz commit olmadı)
- Transaction-2: Aynı product'ı okur, stock_quantity=50 görür
- Transaction-1: Rollback yapar (stock_quantity tekrar 100 olur)
- Transaction-2: Yanlış veri (50) okumuş oldu, gerçek değer 100

---

### c) Phantom Read

- [ ] **Problem:** Aynı query iki kez çalıştırıldığında farklı sonuçlar döner.

**Senaryo:**
- `products` tablosunda category='Electronics' olan 100 ürün var
- Transaction-1: `SELECT * FROM products WHERE category = 'Electronics'` → 100 ürün döner
- Transaction-2: Yeni bir Electronics ürünü ekler (`products` tablosuna insert) ve commit eder
- Transaction-1: Aynı query'yi tekrar çalıştırır → 101 ürün döner (phantom row)
- Transaction-1 aynı transaction içinde farklı sonuç görür


---

### d) Non-Repeatable Read

- [ ] **Problem:** Aynı transaction içinde aynı row iki kez okunduğunda farklı değerler.

**Senaryo:**
- `products` tablosunda product_id='abc-123', stock_quantity=100
- Transaction-1: Product'ı okur, stock_quantity=100 görür
- Transaction-2: Aynı product'ın stock_quantity'sini 50'ye düşürür ve commit eder
- Transaction-1: Aynı product'ı tekrar okur → stock_quantity=50 (farklı değer!)
- Transaction-1 aynı transaction içinde aynı row'u farklı değerlerle okur


---

## 3. Database Performans Problemleri

### a) N+1 Query Problem

- [ ] **Problem:** Bir query sonucu için N tane ek query çalışır.

**Senaryo:**
- `orders` tablosundan 1000 order getirilir (1 query)
- Her `Order` entity'si için `order_items` tablosundan `OrderItem`'lar lazy load ile çekilir
- Her order için ayrı query: `SELECT * FROM order_items WHERE order_id = ?`
- Toplam: 1001 query (1 ana query + 1000 lazy load query)
- `OrderItem` entity'si `@ManyToOne(fetch = FetchType.LAZY)` ile tanımlı olduğu için N+1 problemi oluşur

---

### b) Missing Index

- [ ] **Problem:** WHERE clause'da index kullanılmayan kolonlar.

**Senaryo:**
- `products` tablosunda `name` kolonunda LIKE query çalıştırılır: `SELECT * FROM products WHERE name LIKE '%laptop%'`
- `name` kolonunda index yok
- 1 milyon ürün varsa full table scan yapılır
- Query çok yavaş çalışır (10+ saniye)

---

### c) Full Table Scan

- [ ] **Problem:** WHERE clause'da index kullanılmayan kolonlar.

**Senaryo:**
- `products` tablosunda `category` kolonu ile arama yapılır: `SELECT * FROM products WHERE category = 'Electronics'`
- `category` kolonunda index yok
- 1 milyon ürün varsa tüm `products` tablosu taranır
- Full table scan yapılır, performans düşer (5+ saniye)

---

### d) Connection Pool Exhaustion

- [ ] **Problem:** HikariCP pool size küçükse, yüksek concurrency'de connection bekler.

**Senaryo:**
- 100 eşzamanlı request gelir
- Pool size 10 ise, sadece 10 request connection alabilir
- Diğer 90 request connection bekler
- Timeout oluşabilir

---

## 4. Business Logic Problemleri

### a) Negative Stock

- [ ] **Problem:** Stock kontrolü yapılıyor ama eşzamanlı order'larda race condition olabilir.

**Senaryo:**
- `products` tablosunda product_id='abc-123', stock_quantity=1
- Thread-1: `products` tablosundan stock_quantity kontrolü yapar (stock_quantity > 0) ✅
- Thread-2: `products` tablosundan stock_quantity kontrolü yapar (stock_quantity > 0) ✅
- Thread-1: Order oluşturur (`orders` ve `order_items` tablolarına insert), stock_quantity=0 olarak günceller
- Thread-2: Order oluşturur (`orders` ve `order_items` tablolarına insert), stock_quantity=-1 olarak günceller (race condition!)
- `products` tablosunda stock_quantity negatif olur!

---

### b) Double Payment

- [ ] **Problem:** Payment processing - Idempotency yoksa aynı order için iki kez ödeme yapılabilir.

**Senaryo:**
- `orders` tablosunda order_id='order-123' olan sipariş için iki kez payment request gönderilir
- İlk request: `payments` tablosuna payment kaydı eklenir, `status`='COMPLETED', `amount`=1000
- İkinci request: `payments` tablosuna yeni bir payment kaydı eklenir, `status`='COMPLETED', `amount`=1000
- Aynı order için `payments` tablosunda 2 kayıt oluşur
- Kullanıcı iki kez ödeme yapmış olur (toplam 2000 ödemiş)

---

### c) Order Status Inconsistency

- [ ] **Problem:** OrderStatus transition - InvalidStatusTransitionException

**Senaryo:**
- `orders` tablosunda order_id='order-123', `status`='DELIVERED'
- `OrderStatus.canTransitionTo()` metodu çağrılır: DELIVERED → CANCELLED
- `OrderStatus` enum'unda DELIVERED'dan sadece REFUNDED'a geçiş yapılabilir
- DELIVERED → CANCELLED geçişi geçersiz
- `InvalidStatusTransitionException` fırlatılır

---

## 5. Distributed Systems Problemleri

### a) Distributed Transaction

- [ ] **Problem:** Order creation → Payment → Shipment - Bir adım başarısız olursa rollback nasıl yapılır?

**Senaryo:**
- `orders` tablosuna order kaydı eklenir (order_id='order-123')
- `payments` tablosuna payment kaydı eklenir (payment_id='pay-456', order_id='order-123')
- `shipments` tablosuna shipment kaydı eklenmeye çalışılır ama başarısız olur
- `orders` ve `payments` tablolarındaki kayıtlar rollback edilmeli
- Compensation transaction ile payment iptal edilmeli

---

### b) Eventual Consistency

- [ ] **Problem:** RabbitMQ ile async event'ler - Order created ama payment event henüz işlenmedi.

**Senaryo:**
- `orders` tablosuna order kaydı eklenir, "OrderCreated" event publish edilir
- RabbitMQ'da event queue'ya gönderilir
- Payment service henüz event'i işlemedi
- `orders` tablosunda order görünür ama `payments` tablosunda payment kaydı yok
- Order görünür ama payment durumu belirsiz
- Event ordering problemi oluşur

---

### c) Distributed Lock

- [ ] **Problem:** Redis ile distributed lock - Multi-instance environment'ta stock güncellemesi.

**Senaryo:**
- 3 Spring Boot instance çalışıyor (load balanced)
- `products` tablosunda product_id='abc-123' olan ürün için eşzamanlı stock güncelleme isteği gelir
- Redis distributed lock ile sadece bir instance `products` tablosunu güncellemeli
- Diğer 2 instance lock beklemeli
- Lock release olunca sıradaki instance güncelleme yapmalı

---

## 6. Cache Problemleri

### a) Cache Stampede

- [ ] **Problem:** Product cache expire olunca 1000 request aynı anda cache miss → 1000 DB query.

**Senaryo:**
- `products` tablosunda product_id='abc-123' olan ürün Redis cache'de tutulur (TTL: 5 dakika)
- 5 dakika sonra cache expire olur
- 1000 request aynı anda product_id='abc-123' için gelir
- Hepsi cache miss → 1000 kez `SELECT * FROM products WHERE product_id = 'abc-123'` query çalışır
- `products` tablosuna 1000 query aynı anda gelir, database overload olur

---

### b) Cache Invalidation

- [ ] **Problem:** Product güncellendi ama cache temizlenmedi - Kullanıcılar eski veriyi görür.

**Senaryo:**
- `products` tablosunda product_id='abc-123' olan ürünün `price` değeri 1000'den 1500'e güncellenir
- Redis cache'deki product cache invalidate edilmez
- Yeni request product_id='abc-123' için gelir
- Redis cache'den eski fiyat (1000) döner
- `products` tablosunda fiyat 1500 ama cache'de 1000 görünür
- Data inconsistency oluşur

---

### c) Cache Coherence

- [ ] **Problem:** Multi-instance cache - Instance-1'de product güncellendi, Instance-2 cache'i eski.

**Senaryo:**
- Instance-1: `products` tablosunda product_id='abc-123' olan ürünü günceller, local Redis cache'ini update eder
- Instance-2: Hala eski cache'de product verisi var (price=1000)
- Instance-1'den request gelirse price=1500 döner
- Instance-2'den request gelirse price=1000 döner
- Farklı instance'lardan farklı veri döner
- Cache coherence problemi oluşur

---


## 13. Security Problemleri

### a) SQL Injection

- [ ] **Problem:** Kullanıcı input'u doğrudan SQL query'ye eklenirse SQL injection riski oluşur.

**Senaryo:**
- `ProductController`'da `/products/search` endpoint'ine: `GET /products/search?name=' OR '1'='1`
- Eğer native query kullanılırsa: `SELECT * FROM products WHERE name = ' OR '1'='1'`
- SQL injection ile query: `SELECT * FROM products WHERE name = '' OR '1'='1'` olur
- `products` tablosundaki tüm ürünler döner
- Güvenlik açığı oluşur

---

### b) XSS (Cross-Site Scripting)

- [ ] **Problem:** Kullanıcı input'u HTML'e render edilirse XSS riski oluşur.

**Senaryo:**
- `products` tablosunda product_id='abc-123' olan ürünün `description` alanına script tag eklenir: `<script>alert('XSS')</script>`
- Frontend'de `description` HTML olarak render edilirse script çalışır
- Kullanıcı tarayıcısında XSS saldırısı oluşur
- Cookie'ler çalınabilir, session hijack yapılabilir

---

### c) CSRF (Cross-Site Request Forgery)

- [ ] **Problem:** Kullanıcı farkında olmadan istek gönderilebilir.

**Senaryo:**
- Kullanıcı başka bir sitede (evil.com) form doldurur
- Form `POST /api/orders` endpoint'ine istek gönderir
- Kullanıcı farkında olmadan `orders` tablosuna yeni order kaydı eklenir
- CSRF token yoksa saldırı başarılı olur
- Kullanıcı adına istenmeyen sipariş oluşturulur

---

### d) Authentication ve Authorization

- [ ] **Problem:** Endpoint'ler authentication/authorization kontrolü yapmıyor.

**Senaryo:**
- `OrderController`'da endpoint'lerde `@PreAuthorize` annotation yok
- `GET /api/orders/{orderId}` endpoint'ine herkes erişebilir
- User A'nın (user_id='user-A') order'ını (order_id='order-123') User B (user_id='user-B') görebilir
- `orders` tablosunda `user_id` kontrolü yapılmazsa authorization bypass oluşur

---

### e) Sensitive Data Exposure

- [ ] **Problem:** Response'larda sensitive data (password, credit card) dönebilir.

**Senaryo:**
- `UserController`'da `GET /api/users/{userId}` endpoint'i çağrılır
- Response'da `users` tablosundan `password` field'ı döner (eğer entity'de expose edilmişse)
- `credit_cards` tablosundan credit card bilgileri maskelenmemiş olarak döner
- Sensitive data exposure oluşur
- Güvenlik açığı oluşur

---

## 14. API Design Problemleri

### a) API Versioning

- [ ] **Problem:** API değişikliklerinde backward compatibility sorunları.

**Senaryo:**
- v1: `GET /api/v1/products/{productId}` → `{ "name": "Laptop", "price": 1000 }` (products tablosundan)
- v2: `GET /api/v2/products/{productId}` → `{ "productName": "Laptop", "productPrice": 1000 }` (field isimleri değişti)
- v1 client'ları v2 endpoint'ine erişirse field'ları bulamaz
- JSON deserialization hatası oluşur
- Backward compatibility bozulur

---

### b) Rate Limiting

- [ ] **Problem:** API'ye sınırsız istek gönderilebilir, DDoS riski.

**Senaryo:**
- `/api/products/search` endpoint'ine 10,000 request/saniye gönderilir
- Rate limiting yoksa tüm request'ler `products` tablosuna query yapar
- Database connection pool tükenir
- API crash olur, DDoS saldırısı başarılı olur
- Service unavailable olur

---

### c) Pagination Problemleri

- [ ] **Problem:** Büyük result set'lerde pagination yoksa memory problemi.

**Senaryo:**
- `GET /api/orders` endpoint'ine pagination parametresi gönderilmez
- `orders` tablosundan 1 milyon order getirilir
- Tüm `Order` entity'leri memory'ye yüklenir
- Memory overflow olur
- OutOfMemoryError fırlatılır

---

### d) Backward Compatibility

- [ ] **Problem:** API değişikliklerinde eski client'lar çalışmaz.

**Senaryo:**
- v1: `{ "name": "Product", "price": 100 }`
- v2: `{ "productName": "Product", "productPrice": 100 }`
- v1 client'ları field'ları bulamaz
- Hata alır, çalışmaz

---

## 15. Error Handling Problemleri

### a) Exception Leakage

- [ ] **Problem:** Internal exception'lar client'a expose edilir.

**Senaryo:**
- `OrderService.createOrder()` metodunda `order.getUser()` null döner
- NullPointerException fırlatılır
- `GlobalExceptionHandler` handle etmezse exception client'a gider
- Stack trace'de `OrderService.createOrder()` metodu, dosya yolu, satır numarası görünür
- Internal implementation detayları expose olur

---

### b) Stack Trace Exposure

- [ ] **Problem:** Production'da stack trace client'a gönderilir.

**Senaryo:**
- `ProductService.updateProduct()` metodunda exception fırlatılır
- Response'da stack trace var: `at com.fsk.ecommerce.service.ProductService.updateProduct(ProductService.java:45)`
- Production'da stack trace'de class path, method name, line number görünür
- Sensitive bilgi leak olur (code structure, technology stack)
- Güvenlik riski oluşur

---

### c) Error Message Information Disclosure

- [ ] **Problem:** Error mesajlarında sensitive bilgi (database schema, file paths) olabilir.

**Senaryo:**
- `products` tablosuna bağlanırken database connection error oluşur
- Error mesajında: `Connection to jdbc:postgresql://localhost:5432/ecommerce failed. User: fsk, Password: ***`
- Error mesajında database schema bilgisi, connection string görünür
- Sensitive bilgi exposure oluşur
- Güvenlik açığı oluşur

---

## 16. Retry ve Circuit Breaker Problemleri

### a) Retry Storm

- [ ] **Problem:** Retry mekanizması yoksa, başarısız istekler tekrar tekrar gönderilir.

**Senaryo:**
- Payment service down
- `OrderService` her order için payment service'e istek gönderir
- 1000 order için 1000 retry yapılır
- Payment service daha da yüklenir
- Retry storm oluşur
- Service recovery zorlaşır

---

### b) Circuit Breaker

- [ ] **Problem:** Down service'e sürekli istek gönderilir.

**Senaryo:**
- Payment service down
- `OrderService.createOrder()` her order için payment service'e istek gönderir
- Circuit breaker yoksa her başarısız istek için retry yapılır
- `orders` tablosuna order eklenir ama `payments` tablosuna payment eklenemez
- Resource waste oluşur (CPU, network, thread pool)

---

### c) Retry Logic Yetersizliği

- [ ] **Problem:** Retry mekanizması yoksa, geçici hatalar kalıcı hata gibi görünür.

**Senaryo:**
- Geçici network hatası oluşur
- Retry yapılmazsa hemen hata döner
- Geçici hata kalıcı hata gibi görünür
- User experience kötüleşir

---

## 17. Idempotency Problemleri

### a) Duplicate Request

- [ ] **Problem:** Aynı request iki kez gönderilirse duplicate işlem yapılır.

**Senaryo:**
- `POST /api/orders` endpoint'ine order creation request iki kez gönderilir (network retry, user double-click)
- İlk request: `orders` tablosuna order_id='order-123' eklenir
- İkinci request: `orders` tablosuna order_id='order-124' eklenir (aynı içerik)
- Duplicate order oluşur
- Data integrity problemi

---

### b) Payment Duplication

- [ ] **Problem:** Aynı order için iki kez ödeme yapılabilir.

**Senaryo:**
- `POST /api/payments` endpoint'ine payment request iki kez gönderilir
- İlk request: `payments` tablosuna payment_id='pay-123', order_id='order-123', amount=1000 eklenir
- İkinci request: `payments` tablosuna payment_id='pay-124', order_id='order-123', amount=1000 eklenir
- Aynı order için iki kez ödeme yapılır
- Kullanıcı iki kez ödeme yapmış olur (toplam 2000)
- Financial loss oluşur

---

## 18. Message Queue Problemleri

### a) Duplicate Messages

- [ ] **Problem:** RabbitMQ'da aynı mesaj iki kez işlenebilir.

**Senaryo:**
- `orders` tablosuna order eklendikten sonra "OrderCreated" event RabbitMQ'ya iki kez publish edilir
- Payment service consumer mesajı iki kez işler
- `payments` tablosuna iki kez payment kaydı eklenir
- Duplicate processing oluşur

---

### b) Message Ordering

- [ ] **Problem:** Mesajlar sırayla işlenmeyebilir.

**Senaryo:**
- RabbitMQ'da event sırası: OrderCreated → PaymentProcessed → ShipmentCreated
- Mesajlar farklı sırada consumer'a gelir: ShipmentCreated → OrderCreated → PaymentProcessed
- Shipment service `shipments` tablosuna kayıt eklemeye çalışır ama order henüz yok
- Business logic hatası oluşur

---

### c) Dead Letter Queue

- [ ] **Problem:** Başarısız mesajlar kaybolur.

**Senaryo:**
- RabbitMQ'da "OrderCreated" event'i payment service'e gönderilir
- Payment processing başarısız olur (`payments` tablosuna insert başarısız)
- Dead letter queue yoksa mesaj kaybolur
- Retry edilmez
- `orders` tablosunda order var ama `payments` tablosunda payment yok
- Data loss oluşur

---

### d) Message Loss

- [ ] **Problem:** Mesajlar kaybolabilir.

**Senaryo:**
- RabbitMQ crash olursa
- "OrderCreated" event'i unacknowledged olarak queue'da bekliyordu
- Unacknowledged mesajlar kaybolur
- `orders` tablosunda order var ama payment ve shipment işlenmedi
- Message loss oluşur
- Data consistency bozulur

---

## 19. Data Consistency Problemleri

### a) Read-Your-Writes

- [ ] **Problem:** Write yapıldıktan sonra read yapıldığında eski veri okunabilir.

**Senaryo:**
- `orders` tablosuna order create edilir (order_id='order-123')
- Hemen sonra `GET /api/orders/order-123` endpoint'i çağrılır
- Read replica'dan okuma yapılıyorsa replication lag nedeniyle order bulunamaz
- Eventual consistency problemi
- Read-your-writes guarantee yok

---

### b) Eventual Consistency

- [ ] **Problem:** Distributed system'de veri tutarsızlığı.

**Senaryo:**
- Instance-1: `products` tablosunda product_id='abc-123', stock_quantity=100
- Instance-1'de 5 adet satış yapılır, stock_quantity=95 olur
- Instance-2: Cache'de hala stock_quantity=100 görünür (henüz sync olmadı)
- Instance-1'den request gelirse stock_quantity=95 döner
- Instance-2'den request gelirse stock_quantity=100 döner
- Farklı instance'lardan farklı değer okunur
- Eventual consistency problemi

---

### c) Split-Brain Problem

- [ ] **Problem:** Network partition durumunda iki master oluşur.

**Senaryo:**
- Database cluster'da network split oluşur
- Partition-1: `orders` tablosuna order_id='order-123' ekler
- Partition-2: `orders` tablosuna order_id='order-124' ekler (aynı user için)
- Her iki partition da master olur
- Split-brain problemi oluşur
- Network birleşince data conflict oluşur

---

## 20. Scalability Problemleri

### a) Bottleneck Detection

- [ ] **Problem:** Sistemin darboğazı nerede?

**Senaryo:**
- Load test ile `/api/products/search` endpoint'ine yüksek trafik oluşturulur (10,000 req/s)
- CPU: %90+ kullanım (bottleneck)
- Memory: %80+ kullanım
- Database: `products` tablosuna 10,000 query/saniye (connection pool tükenir)
- Network: Bandwidth %70+ kullanım
- Response time artar (100ms → 2000ms)
- Throughput düşer (1000 req/s → 100 req/s)

---

### b) Horizontal Scaling

- [ ] **Problem:** Tek instance yeterli değil, scale out gerekli.

**Senaryo:**
- Spring Boot application 2 instance → 4 instance scale out yapılır
- Load balancer 4 instance'a request dağıtır
- `products` tablosuna query sayısı artar mı? (connection pool x4)
- Performance artar mı? (throughput 2x olmalı)
- Load balancing çalışır mı? (round-robin, sticky session)
- Session management problemi oluşur mu? (stateless olmalı)

---

### c) Database Connection Pool Exhaustion

- [ ] **Problem:** Yüksek concurrency'de connection pool tükenir.

**Senaryo:**
- `/api/orders` endpoint'ine 1000 eşzamanlı request gelir
- HikariCP connection pool size: 20
- Sadece 20 request `orders` tablosuna connection alabilir
- Diğer 980 request connection bekler
- Connection timeout (30 saniye) oluşur
- Request'ler başarısız olur

---

## 21. Monitoring ve Observability Problemleri

### a) Distributed Tracing

- [ ] **Problem:** Multi-service request'lerde trace kaybolur.

**Senaryo:**
- Request flow: OrderService → PaymentService → ShipmentService
- Trace ID (X-Trace-Id header) tüm service'lerde aynı mı?
- `orders`, `payments`, `shipments` tablolarına insert yapılırken trace ID log'lanıyor mu?
- Trace kaybolursa hangi service'de problem olduğu bulunamaz
- Debugging zorlaşır
- Observability eksikliği

---

### b) Log Aggregation

- [ ] **Problem:** Multi-instance log'ları toplamak zor.

**Senaryo:**
- 3 Spring Boot instance'da log'lar oluşur
- Instance-1: `orders` tablosuna insert log'u
- Instance-2: `payments` tablosuna insert log'u
- Instance-3: `shipments` tablosuna insert log'u
- Merkezi bir yerde (ELK, Splunk) toplanmıyor
- Log aggregation yok
- Troubleshooting zorlaşır (hangi instance'da problem var?)

---

### c) Metrics Collection

- [ ] **Problem:** Performance metrikleri toplanmıyor.

**Senaryo:**
- `/api/products/search` endpoint'i için request count, response time, error rate metrikleri toplanmıyor
- Prometheus, Grafana gibi monitoring tool yok
- Performance monitoring yok
- `products` tablosuna query sayısı, slow query'ler tespit edilemez
- Bottleneck tespit edilemez
- Optimization yapılamaz

---

## 22. Configuration Management Problemleri

### a) Configuration Drift

- [ ] **Problem:** Farklı environment'larda farklı config'ler.

**Senaryo:**
- Dev environment: `application.yml`'de `spring.datasource.url = jdbc:postgresql://localhost:5432/ecommerce`
- Prod environment: `application.yml`'de `spring.datasource.url = jdbc:postgresql://localhost:5432/ecommerce` (yanlış, prod-db olmalı)
- Config drift oluşur
- Production'da yanlış database'e bağlanır
- `orders`, `products` tablolarına erişilemez

---

### b) Secret Management

- [ ] **Problem:** Secret'lar (password, API key) kodda hardcode.

**Senaryo:**
- `application.yml`'de `spring.datasource.password = mypassword123` var
- Git'e commit edilmiş
- Secret management (Vault, AWS Secrets Manager) yok
- Database password expose olur
- Güvenlik açığı oluşur

---

## 23. Database Migration Problemleri

### a) Migration Failure

- [ ] **Problem:** Migration başarısız olursa database inconsistent olur.

**Senaryo:**
- Flyway/Liquibase migration çalışırken crash olur
- Migration: `ALTER TABLE products ADD COLUMN discount DECIMAL(5,2)`
- Migration yarıda kalır, `products` tablosu inconsistent olur
- Application başlatıldığında `Product` entity ile `products` tablosu uyumsuz
- Application çalışmaz

---

### b) Zero-Downtime Migration

- [ ] **Problem:** Migration sırasında downtime olur.

**Senaryo:**
- `products` tablosuna `discount` kolonu ekleme migration yapılır
- Application çalışırken migration yapılamaz (table lock)
- Application durdurulur, migration yapılır, application başlatılır
- Downtime gerekir (5-10 dakika)
- Zero-downtime migration yok

---

## 24. Backup ve Recovery Problemleri

### a) Backup Strategy

- [ ] **Problem:** Backup yoksa data loss riski.

**Senaryo:**
- PostgreSQL database crash olur
- `orders`, `products`, `users` tablolarındaki tüm data kaybolur
- Backup yoksa data recovery yapılamaz
- Data loss oluşur
- Tüm siparişler, ürünler, kullanıcılar kaybolur

---

### b) Point-in-Time Recovery

- [ ] **Problem:** Belirli bir zamana geri dönülemez.

**Senaryo:**
- 2 saat önce yanlışlıkla `orders` tablosundan tüm kayıtlar silindi
- 2 saat önceki veriye dönülmek istenir
- Point-in-time recovery (PITR) yok
- Sadece son backup'tan (24 saat önce) restore yapılabilir
- Son 24 saatteki tüm order'lar kaybolur
- Data loss oluşur

---

## 25. Load Balancing Problemleri

### a) Sticky Session

- [ ] **Problem:** Load balancer session'ı farklı instance'a yönlendirir.
**Senaryo:**
- Session-based authentication kullanılır (JSESSIONID cookie)
- User login olur, session Instance-1'de tutulur
- Request farklı instance'a (Instance-2) giderse session bulunamaz
- User logout olur
- User tekrar login olmak zorunda kalır
- User experience kötüleşir

---

### b) Health Check

- [ ] **Problem:** Down instance'a istek gönderilir.

**Senaryo:**
- Instance-2 crash olur
- Health check (`/actuator/health`) çalışmazsa load balancer down instance'a istek gönderir
- `/api/orders` endpoint'ine request gelir
- Request başarısız olur (connection refused)
- Service unavailable oluşur

---

## 26. Service Discovery Problemleri

### a) Service Registration

- [ ] **Problem:** Yeni instance register olmazsa keşfedilmez.

**Senaryo:**
- Yeni Spring Boot instance başlatılır (Instance-4)
- Eureka/Consul gibi service discovery'de register olmaz
- Instance keşfedilmez
- Load balancer Instance-4'e istek göndermez
- Instance-4 boşta kalır, load balancing çalışmaz

---

### b) Service Deregistration

- [ ] **Problem:** Instance down olunca deregister olmaz.

**Senaryo:**
- Instance-2 crash olur
- Eureka/Consul service discovery'den deregister olmaz (heartbeat timeout yok)
- Load balancer Instance-2'ye istek gönderir
- `/api/products` endpoint'ine request gelir
- Request başarısız olur (connection refused)

---

## 27. API Gateway Problemleri

### a) Single Point of Failure

- [ ] **Problem:** API Gateway down olursa tüm sistem down.

**Senaryo:**
- API Gateway (Kong, Zuul) crash olur
- Tüm request'ler (`/api/orders`, `/api/products`) API Gateway üzerinden geçer
- API Gateway down olunca tüm request'ler başarısız olur
- Single point of failure oluşur
- Service unavailable oluşur

---

### b) Request Routing

- [ ] **Problem:** Yanlış service'e route edilir.

**Senaryo:**
- `/api/orders` request'i gelir
- API Gateway'de yanlış routing config: `/api/orders` → Payment Service
- Request payment service'e gider
- Payment service'de `/api/orders` endpoint'i yok
- Request başarısız olur (404 Not Found)
- Service routing hatası


### a) Write Skew (Phantom Write)

- [ ] **Problem:** İki transaction farklı row'ları okur, her ikisi de günceller, ama constraint violation oluşur.

**Senaryo:**
- Business rule: `products` tablosunda category='Electronics' olan ürünlerin toplam stock_quantity'si 1000'den fazla olamaz
- Transaction-1: `products` tablosunda product_id='prod-A' (category='Electronics', stock_quantity=600) okur, 500'e düşürmek ister (toplam 1100 olur)
- Transaction-2: `products` tablosunda product_id='prod-B' (category='Electronics', stock_quantity=500) okur, 400'e düşürmek ister (toplam 1100 olur)
- Her ikisi de commit olur → Constraint violation! (toplam 1100 > 1000)


---

### b) Time-of-Check-Time-of-Use (TOCTOU)

- [ ] **Problem:** Check ve use arasında state değişir.

**Senaryo:**
- `products` tablosunda product_id='abc-123', stock_quantity=1
- Thread-1: `products` tablosundan stock_quantity kontrolü yapar (stock_quantity > 0) ✅
- Thread-2: `products` tablosunda stock_quantity'yi 0'a düşürür
- Thread-1: `orders` ve `order_items` tablolarına order oluşturur → stock_quantity negatif olur!


---

### c) Cascading Failure

- [ ] **Problem:** Bir service down olunca diğer service'ler de down olur.

**Senaryo:**
- Payment service down
- `OrderService.createOrder()` payment service'e istek gönderir
- Payment service timeout olur (30 saniye)
- `OrderService` timeout bekler
- Tüm `/api/orders` request'leri başarısız olur
- `orders` tablosuna order eklenemez


---

### d) Thundering Herd Problem

- [ ] **Problem:** Cache expire olunca tüm request'ler aynı anda DB'ye gider.

**Senaryo:**
- `products` tablosunda product_id='abc-123' olan ürün Redis cache'de tutulur (TTL: 5 dakika)
- 5 dakika sonra cache expire olur
- 10,000 request aynı anda product_id='abc-123' için gelir
- Hepsi cache miss → 10,000 kez `SELECT * FROM products WHERE product_id = 'abc-123'` query çalışır
- `products` tablosuna 10,000 query aynı anda gelir


---

### e) Long Transaction Problem

- [ ] **Problem:** Transaction çok uzun sürerse lock'lar uzun süre tutulur.

**Senaryo:**
- `OrderService.createOrder()` transaction'ı 30 saniye sürer (external API call, slow query)
- `products` tablosunda product_id='abc-123' olan ürün lock'ta kalır
- Diğer order request'leri aynı product için bekler
- `orders` tablosuna order eklenemez


---

### f) Database Connection Leak

- [ ] **Problem:** Transaction commit/rollback olmazsa connection pool'da leak oluşur.

**Senaryo:**
- `OrderService.createOrder()` metodunda exception fırlatılır ama `@Transactional` rollback olmaz
- HikariCP connection pool'da connection leak oluşur
- Connection pool size: 20, leak: 20
- Pool tükenir, yeni request'ler connection alamaz


---

### g) Memory Leak in Entity Manager

- [ ] **Problem:** Entity Manager'da entity'ler clear edilmezse memory leak oluşur.

**Senaryo:**
- `orders` tablosundan 100,000 order getirilir: `SELECT * FROM orders`
- Hibernate Entity Manager'da tüm `Order` entity'leri tutulur
- Her `Order` entity'si `OrderItem`, `User`, `Address` ilişkilerini de tutar
- Memory overflow oluşur (OutOfMemoryError)


---

### h) Query Plan Cache Pollution

- [ ] **Problem:** Farklı parametrelerle aynı query farklı plan kullanır.

**Senaryo:**
- `products` tablosunda: `SELECT * FROM products WHERE category = ?`
- category = 'Electronics' → Index kullanır (1000 ürün var)
- category = 'RareCategory' → Full table scan (1 ürün var)
- PostgreSQL query plan cache'de 'Electronics' için plan tutulur
- 'RareCategory' için de aynı plan kullanılır (yanlış, full table scan olmalı)


---

### i) Lock Escalation

- [ ] **Problem:** Çok fazla row-level lock table-level lock'a escalate olur.

**Senaryo:**
- `products` tablosunda category='Electronics' olan 10,000 ürünü güncelle: `UPDATE products SET price = price * 1.1 WHERE category = 'Electronics'`
- Her biri için row-level lock
- Lock escalation → Table lock (`products` tablosu lock'lanır)
- Tüm diğer transaction'lar bekler (`SELECT * FROM products` query'leri bekler)


---

### j) Write Amplification

- [ ] **Problem:** Bir update birden fazla disk write'a neden olur.

**Senaryo:**
- `products` tablosunda product_id='abc-123' olan ürünün `price` değeri güncellenir
- PostgreSQL WAL (Write-Ahead Log) write yapar
- `products` tablosundaki `price` index'i update edilir
- `version` kolonu update edilir (optimistic locking)
- Toplam: 3x write amplification (1 update → 3 disk write)


---

### k) Read Committed Snapshot Isolation (RCSI) Problemleri

- [ ] **Problem:** READ COMMITTED isolation level'da snapshot isolation kullanılırsa version store büyür.

**Senaryo:**
- Long-running transaction
- Version store'da eski versiyonlar tutulur
- Version store büyür → Disk space problemi


---

### l) Hot Spot Problem

- [ ] **Problem:** Belirli row'lara çok fazla concurrent access olur.

**Senaryo:**
- `products` tablosunda product_id='popular-123' olan ürün çok popüler (1 milyon order)
- Her order bu product'ın `stock_quantity` değerini günceller
- `products` tablosunda aynı row'a çok fazla concurrent update
- Hot spot → Lock contention oluşur
- Diğer order'lar bekler


---

### m) False Sharing (CPU Cache)

- [ ] **Problem:** Farklı thread'ler aynı cache line'ı kullanır.

**Senaryo:**
- `products` tablosunda product_id='prod-A' ve product_id='prod-B' aynı CPU cache line'da (64 byte)
- Thread-1: `products` tablosunda prod-A'nın `stock_quantity` değerini günceller
- Thread-2: `products` tablosunda prod-B'nin `stock_quantity` değerini günceller
- Cache line invalidate olur → Performance düşer (false sharing)


---

### n) ABA Problem

- [ ] **Problem:** Lock-free data structure'larda value değişir ama aynı değere geri döner.

**Senaryo:**
- `products` tablosunda product_id='abc-123', version=1
- Thread-1: Product'ı okur, version=1 görür
- Thread-2: Product'ı günceller, version=2 olur, sonra başka bir update ile version=1'e geri döner
- Thread-1: Version hala 1 mi kontrol eder → Evet! (Yanlış! Arada version=2 oldu)
- ABA Problem oluşur


---

### o) Priority Inversion

- [ ] **Problem:** Yüksek öncelikli thread düşük öncelikli thread'i bekler.

**Senaryo:**
- High-priority thread: `products` tablosunda product_id='prod-A' olan ürünü lock'lar
- Low-priority thread: Aynı product'ı lock'lamaya çalışır (bekler)
- Medium-priority thread: CPU'yu alır
- High-priority thread bekler → Priority inversion (düşük öncelikli thread yüksek öncelikli thread'i bloklar)


---

### p) Livelock

- [ ] **Problem:** Thread'ler sürekli çalışır ama ilerleme kaydetmez.

**Senaryo:**
- Thread-1: `products` tablosunda product_id='prod-A' lock'lar, product_id='prod-B' lock'lamaya çalışır (yok)
- Thread-2: `products` tablosunda product_id='prod-B' lock'lar, product_id='prod-A' lock'lamaya çalışır (yok)
- Her ikisi de lock'ları bırakıp tekrar dener
- Sonsuz döngü → Livelock (thread'ler çalışır ama ilerleme kaydetmez)


---

### q) Starvation

- [ ] **Problem:** Bazı thread'ler hiç çalışmaz.

**Senaryo:**
- 100 thread `products` tablosunda product_id='abc-123' olan ürünü güncellemek ister
- İlk 10 thread sürekli lock alır ve başarılı olur
- Diğer 90 thread hiç lock alamaz, hiç çalışmaz → Starvation
- Fairness yok


---

### r) Memory Ordering Problem

- [ ] **Problem:** CPU reordering nedeniyle instruction'lar farklı sırada execute edilir.

**Senaryo:**
- Thread-1: `x = 1; y = 2;`
- Thread-2: `if (y == 2) assert x == 1;`
- CPU reordering → `y = 2` önce execute edilir
- Assert fail olur!


---

### s) False Positive in Optimistic Locking

- [ ] **Problem:** Optimistic locking false positive verir (gerçekte conflict yok).

**Senaryo:**
- `products` tablosunda product_id='abc-123', version=1
- Thread-1: Product'ı okur (version=1), `price` field'ını günceller
- Thread-2: Product'ı okur (version=1), `description` field'ını günceller
- Thread-1: Günceller (version=2)
- Thread-2: Günceller (version=2) → StaleStateException
- Ama Thread-2 farklı field'ı (`description`) güncelliyordu, conflict yok!
- False positive in optimistic locking


---

### t) Distributed System Clock Skew

- [ ] **Problem:** Farklı instance'larda saat farklı → Event ordering problemi.

**Senaryo:**
- Instance-1: `orders` tablosuna order eklenir, `order_date`=10:00:00 (local time)
- Instance-2: `orders` tablosuna order eklenir, `order_date`=09:59:59 (local time, 1 saniye geri)
- RabbitMQ event ordering: Instance-2'nin event'i önce gelir (timestamp daha küçük)
- Event ordering yanlış olur (gerçekte Instance-1 önce oluşturdu)


---

### u) Split-Brain in Distributed Lock

- [ ] **Problem:** Network partition durumunda iki instance aynı lock'u alır.

**Senaryo:**
- Instance-1: Redis'te `products:abc-123` için distributed lock alır (TTL: 30 saniye)
- Network partition oluşur (Instance-1 Redis'e erişemez)
- Instance-2: Redis'e erişemez, lock'u expired sayar (30 saniye geçti)
- Instance-2: Aynı lock'u alır
- Her ikisi de lock'u aldığını düşünür → Split-brain in distributed lock


---

### v) Byzantine Failure

- [ ] **Problem:** Bir node yanlış bilgi gönderir (malicious veya buggy).

**Senaryo:**
- Instance-1: `products` tablosunda product_id='abc-123', stock_quantity=100 gönderir
- Instance-2: `products` tablosunda product_id='abc-123', stock_quantity=50 gönderir (yanlış! bug veya malicious)
- Hangisi doğru? Consensus mekanizması yok
- Byzantine failure oluşur


---

### w) CAP Theorem Trade-offs

- [ ] **Problem:** Consistency, Availability, Partition tolerance - İkisini seçmek zorundasın.

**Senaryo:**
- Database cluster'da network partition olursa
- CP (Consistency + Partition tolerance): `orders` tablosuna yazma yapılamaz, service down
- AP (Availability + Partition tolerance): `orders` tablosuna yazma yapılır ama farklı partition'larda farklı data
- CAP theorem trade-off: İkisini seçmek zorundasın


---

### x) Two Generals Problem

- [ ] **Problem:** Network'te mesaj kaybolabilir, acknowledgment garantisi yok.

**Senaryo:**
- Instance-1: `orders` tablosuna order eklendikten sonra RabbitMQ'ya "OrderCreated" mesajı gönderir
- Mesaj kaybolur (network problem)
- Instance-2: Mesajı almadı, tekrar gönderir mi? (duplicate riski)
- Instance-1: Acknowledgment almadı, tekrar gönderir mi? (duplicate riski)
- Two Generals Problem: Acknowledgment garantisi yok
- Sonsuz döngü riski


---

### y) FLP Impossibility

- [ ] **Problem:** Asynchronous system'de consensus imkansız (Fischer-Lynch-Paterson).

**Senaryo:**
- 3 Spring Boot instance çalışıyor (distributed system)
- Instance-1 crash olur
- Kalan 2 instance (Instance-2, Instance-3) consensus'a varabilir mi?
- `orders` tablosuna yazma yapılabilir mi?
- FLP Impossibility: Asynchronous system'de consensus imkansız!


---

### z) Linearizability vs Sequential Consistency

- [ ] **Problem:** Distributed system'de operation ordering garantisi.

**Senaryo:**
- Operation A: `products` tablosunda product_id='abc-123', stock_quantity=100 yazılır
- Operation B: `products` tablosunda product_id='abc-123', stock_quantity=50 yazılır
- Linearizability: Tüm node'lar aynı sırada görür mü? (A → B veya B → A)
- Sequential Consistency: Her node kendi sırasında görür mü? (farklı node'lar farklı sıra görebilir)
- Distributed system'de operation ordering garantisi


---

---

## 28. Database Problemleri (Sharding, Cluster, CTE, Materialized View)

### a) Database Sharding - Cross-Shard Query

- [ ] **Problem:** Sharded database'de cross-shard query'ler çok yavaş çalışır.

**Senaryo:**
- `orders` ve `order_items` tabloları shard-1'de, `products` tablosu shard-2'de
- `SELECT o.*, p.name FROM orders o JOIN order_items oi ON o.order_id = oi.order_id JOIN products p ON oi.product_id = p.product_id` query çalıştırılır
- Cross-shard join çok yavaş (her shard'tan data çekilip join yapılır)
- Query timeout olur (30+ saniye)

---

### b) Shard Key Selection

- [ ] **Problem:** Yanlış shard key seçilirse hot shard problemi oluşur.

**Senaryo:**
- `orders` tablosu shard key: `user_id`
- Popüler kullanıcının (user_id='user-123') tüm order'ları tek shard'da (shard-1)
- Shard-1'de 1 milyon order var, diğer shard'larda 1000'er order var
- Hot shard oluşur (shard-1 overload)
- Diğer shard'lar boş kalır

---

### c) Database Cluster - Read Replica Lag

- [ ] **Problem:** Read replica'da replication lag oluşur, eski veri okunur.

**Senaryo:**
- `orders` tablosuna write master'a yapılır (order_id='order-123' eklendi)
- Read replica'ya yönlendirilir: `SELECT * FROM orders WHERE order_id = 'order-123'`
- Replication lag 5 saniye
- Read replica'da order bulunamaz (henüz replicate olmadı)
- Eski veri okunur (order yok)

---

### d) Database Cluster - Split-Brain

- [ ] **Problem:** Cluster'da network partition olursa split-brain oluşur.

**Senaryo:**
- PostgreSQL cluster: 3 node
- Network partition: 2 node bir tarafta, 1 node diğer tarafta
- Her iki taraf da master olur
- Partition-1: `orders` tablosuna order_id='order-123' ekler
- Partition-2: `orders` tablosuna order_id='order-124' ekler (aynı user için)
- Data conflict oluşur (network birleşince)

---

### e) CTE (Common Table Expression) - Recursive Query Performance

- [ ] **Problem:** Recursive CTE'ler büyük veri setlerinde çok yavaş çalışır.

**Senaryo:**
- `categories` tablosunda parent_category_id ile hierarchy var
- Recursive CTE ile tüm alt kategorileri getir: `WITH RECURSIVE category_tree AS (...)`
- 10,000 kategori var (deep hierarchy)
- Recursive query çok yavaş (5+ saniye)
- Query timeout olur

---

### f) CTE - Multiple CTE Performance

- [ ] **Problem:** Birden fazla CTE kullanıldığında query plan kötüleşir.

**Senaryo:**
- `orders`, `order_items`, `products`, `users`, `payments` tabloları için 5 farklı CTE kullanılır
- Her CTE ayrı ayrı execute edilir (subquery olarak)
- Query plan optimal değil (nested loop join)
- Performance düşer (10+ saniye)

---

### g) Materialized View - Stale Data

- [ ] **Problem:** Materialized view güncellenmezse eski veri gösterilir.

**Senaryo:**
- `product_sales_summary` materialized view var (`products` ve `order_items` tablolarından hesaplanır)
- View refresh edilmez (son refresh 1 hafta önce)
- Yeni order'lar eklendi ama view'da görünmüyor
- Eski sales data gösterilir
- Data inconsistency oluşur

---

### h) Materialized View - Refresh Performance

- [ ] **Problem:** Materialized view refresh çok uzun sürer, lock oluşur.

**Senaryo:**
- `product_sales_summary` materialized view refresh yapılır
- `orders` ve `order_items` tablolarında 1 milyon order var
- Refresh 30 dakika sürer
- View lock'ta kalır (SELECT query'ler bekler)
- `SELECT * FROM product_sales_summary` query'leri bekler

---

### i) Materialized View - Incremental Refresh

- [ ] **Problem:** Full refresh yerine incremental refresh yapılmazsa performans düşer.

**Senaryo:**
- `product_sales_summary` materialized view full refresh yapılır
- `orders` tablosunda sadece 100 yeni order var (1 milyon order'dan sonra)
- Tüm view yeniden hesaplanır (1 milyon order işlenir)
- Gereksiz işlem yapılır (sadece 100 order işlenmeli)
- Incremental refresh yapılsa 10 saniye, full refresh 30 dakika

---

### j) Database Sharding - Rebalancing

- [ ] **Problem:** Shard rebalancing sırasında data migration problemi.

**Senaryo:**
- `orders` tablosu Shard-1'den Shard-2'ye data migration yapılır
- Migration sırasında yeni order'lar Shard-1'e yazılır (order_id='order-123')
- Migration tamamlanınca order Shard-2'de de görünür (duplicate)
- Veya migration sırasında order kaybolur (data loss)
- Consistency bozulur

---

## 29. Queue Problemleri (Genişletilmiş)

### a) Queue Backpressure

- [ ] **Problem:** Consumer yavaşsa queue dolar, memory problemi oluşur.

**Senaryo:**
- RabbitMQ'da "OrderCreated" event producer: 1000 mesaj/saniye (`orders` tablosuna 1000 order/saniye ekleniyor)
- Payment service consumer: 100 mesaj/saniye işler (`payments` tablosuna 100 payment/saniye ekleniyor)
- Queue dolar (900 mesaj/saniye birikir)
- Memory overflow olur (queue memory limit'e ulaşır)

---

### b) Queue Priority

- [ ] **Problem:** Priority queue yoksa önemli mesajlar bekler.

**Senaryo:**
- RabbitMQ'da "PaymentProcessed" ve "OrderNotification" mesajları aynı queue'da
- Notification mesajları önce işlenir (FIFO)
- Payment mesajı bekler (`payments` tablosuna insert gecikir)
- Payment SLA ihlali oluşur (5 saniye içinde işlenmeli, 30 saniye bekliyor)

---

### c) Queue Partitioning

- [ ] **Problem:** Queue partition edilmezse hot partition problemi oluşur.

**Senaryo:**
- RabbitMQ'da "OrderCreated" mesajları tek partition'da (partition-0)
- Tüm order mesajları partition-0'a gider
- Hot partition oluşur (partition-0 overload)
- Diğer partition'lar (partition-1, partition-2) boş
- Throughput düşer (tek partition bottleneck)

---

### d) Queue Message Size

- [ ] **Problem:** Çok büyük mesajlar queue'yu bloklar.

**Senaryo:**
- RabbitMQ'ya "OrderCreated" mesajı gönderilir (10MB - tüm order data içeriyor)
- Queue buffer size 1MB
- Mesaj işlenemez (mesaj çok büyük)
- Queue block olur
- Diğer mesajlar bekler

---

### e) Queue Consumer Scaling

- [ ] **Problem:** Consumer sayısı artırıldığında duplicate processing oluşur.

**Senaryo:**
- RabbitMQ'da "OrderCreated" event consumer: 1 consumer → 5 consumer scale out
- Aynı mesaj (order_id='order-123') birden fazla consumer tarafından işlenir
- `payments` tablosuna 2 kez payment kaydı eklenir (duplicate)
- Duplicate processing oluşur
- Data inconsistency

---

### f) Queue Dead Letter Queue Overflow

- [ ] **Problem:** Dead letter queue dolunca yeni mesajlar kaybolur.

**Senaryo:**
- RabbitMQ dead letter queue size limit: 10,000
- 10,000 başarısız "OrderCreated" mesajı var (`payments` tablosuna insert başarısız)
- Yeni başarısız mesajlar kaybolur (queue dolu)
- `orders` tablosunda order var ama `payments` tablosunda payment yok
- Data loss oluşur

---

### g) Queue Message TTL

- [ ] **Problem:** Message TTL çok kısa olursa mesajlar expire olur.

**Senaryo:**
- Message TTL: 5 dakika
- Consumer 10 dakika sonra işler
- Mesaj expire olur
- Data loss oluşur

---

### h) Queue Batch Processing

- [ ] **Problem:** Batch processing yapılmazsa throughput düşer.

**Senaryo:**
- RabbitMQ'da "OrderCreated" mesajları her biri ayrı ayrı işlenir
- 1000 mesaj için 1000 `payments` tablosuna insert işlemi
- Batch processing ile 10 batch (100 mesaj/batch, 100 insert/batch)
- Throughput artar (1000 insert → 10 batch insert)

---

### i) Queue Consumer Group Rebalancing

- [ ] **Problem:** Consumer group rebalancing sırasında duplicate processing.

**Senaryo:**
- RabbitMQ consumer group'da 3 consumer var (PaymentService-1, PaymentService-2, PaymentService-3)
- PaymentService-1 crash olur
- Rebalancing başlar (partition'lar yeniden dağıtılır)
- Aynı mesaj (order_id='order-123') birden fazla consumer'a atanır
- `payments` tablosuna duplicate payment eklenir

---

### j) Queue Exactly-Once Semantics

- [ ] **Problem:** Exactly-once semantics garantisi yoksa duplicate veya loss oluşur.

**Senaryo:**
- At-least-once: "OrderCreated" mesajı 2 kez işlenir, `payments` tablosuna 2 payment eklenir (duplicate)
- At-most-once: "OrderCreated" mesajı kaybolur, `payments` tablosuna payment eklenmez (data loss)
- Exactly-once: "OrderCreated" mesajı tam 1 kez işlenir, `payments` tablosuna 1 payment eklenir
- Implementation zor (idempotency key, distributed transaction gerekli)

---

## 30. Redis Problemleri

### a) Redis Memory Eviction

- [ ] **Problem:** Redis memory dolunca eviction policy ile key'ler silinir.

**Senaryo:**
- Redis memory limit: 10GB
- `products` tablosundan 10GB product data cache'de tutulur (key: `product:{product_id}`)
- Yeni product cache'lenir (key: `product:new-123`)
- Eviction policy (LRU) ile eski key'ler silinir
- Cache miss oluşur (`products` tablosuna query yapılır)

---

### b) Redis Cache Penetration

- [ ] **Problem:** Cache'de olmayan key'ler için sürekli DB query yapılır.

**Senaryo:**
- `products` tablosunda product_id='99999' (yok)
- Her request: `GET product:99999` → cache miss
- `SELECT * FROM products WHERE product_id = '99999'` query çalışır
- DB'de yok, null döner
- Her seferinde `products` tablosuna query yapılır (cache penetration)

---

### c) Redis Cache Avalanche

- [ ] **Problem:** Çok sayıda key aynı anda expire olunca DB'ye stampede oluşur.

**Senaryo:**
- Redis'te 10,000 product key aynı anda expire olur (TTL: 5 dakika, aynı anda cache'lenmiş)
- 10,000 request aynı anda gelir (`GET product:{product_id}`)
- Hepsi cache miss → 10,000 `SELECT * FROM products WHERE product_id = ?` query
- `products` tablosuna 10,000 query aynı anda gelir
- DB overload olur

---

### d) Redis Hot Key

- [ ] **Problem:** Belirli key'lere çok fazla access olur, hot key problemi.

**Senaryo:**
- Redis'te popular product key: `product:abc-123` (`products` tablosunda çok popüler ürün)
- 100,000 request/saniye bu key'e erişir (`GET product:abc-123`)
- Single Redis instance overload olur (CPU %100)
- Performance düşer (latency 1ms → 100ms)

---

### e) Redis Big Key

- [ ] **Problem:** Çok büyük key'ler Redis'i bloklar.

**Senaryo:**
- Redis'te key: `products:all` (10MB data - `products` tablosundaki tüm ürünler)
- Bu key serialize/deserialize edilirken Redis block olur (single-threaded)
- Diğer request'ler (`GET product:abc-123`) bekler
- Latency artar (1ms → 500ms)

---

### f) Redis Pipeline Performance

- [ ] **Problem:** Pipeline kullanılmazsa her command için round-trip yapılır.

**Senaryo:**
- Redis'te 100 product key get edilir: `GET product:1`, `GET product:2`, ..., `GET product:100`
- Her get için round-trip: 1ms (network latency)
- Toplam: 100ms (100 round-trip)
- Pipeline ile: 1 round-trip, 10ms (tüm command'lar birlikte gönderilir)

---

### g) Redis Transaction WATCH

- [ ] **Problem:** WATCH kullanılmazsa optimistic locking çalışmaz.

**Senaryo:**
- Redis'te key: `product:abc-123:stock` (stock_quantity=100)
- Transaction-1: Key'i okur (100), değeri 90'a düşürür (10 adet satış)
- Transaction-2: Aynı key'i okur (100), değeri 95'e düşürür (5 adet satış)
- WATCH yoksa her ikisi de commit olur
- Lost update oluşur (son değer 95, olması gereken 85)

---

### h) Redis Pub/Sub Message Loss

- [ ] **Problem:** Subscriber down olursa mesajlar kaybolur.

**Senaryo:**
- Publisher mesaj gönderir
- Subscriber down
- Mesaj kaybolur
- Message loss oluşur

---

### i) Redis Sentinel Failover

- [ ] **Problem:** Sentinel failover sırasında data loss oluşabilir.

**Senaryo:**
- Redis master crash olur
- Sentinel yeni master seçer (replica'dan biri master olur)
- Replication lag varsa (100 key henüz replicate olmadı) data loss
- `product:abc-123` key kaybolur
- Consistency bozulur

---

### j) Redis Cluster Slot Migration

- [ ] **Problem:** Cluster slot migration sırasında request'ler başarısız olur.

**Senaryo:**
- Redis cluster'a node eklenir, hash slot migration başlar
- `product:abc-123` key migration sırasında iki node'da da olabilir
- Request yanlış node'a gider (`GET product:abc-123`)
- MOVED error alınır (doğru node'a redirect)
- Latency artar

---

### k) Redis Memory Fragmentation

- [ ] **Problem:** Memory fragmentation nedeniyle memory kullanımı artar.

**Senaryo:**
- Redis'te `product:{product_id}` key'leri sürekli eklenir/silinir
- Memory fragmentation oluşur (10GB memory var ama 8GB kullanılabilir)
- Kullanılabilir memory azalır
- Eviction erken başlar (10GB dolmadan)
- Cache miss artar

---

### l) Redis Lua Script Timeout

- [ ] **Problem:** Lua script çok uzun sürerse Redis block olur.

**Senaryo:**
- Redis Lua script çalışır: `product:abc-123` stock güncelleme (5 saniye sürer)
- Redis single-threaded
- Tüm request'ler (`GET product:xyz-456`) bekler
- Timeout oluşur (client timeout: 3 saniye)

---

## 31. Docker Problemleri

### a) Docker Container Resource Limits

- [ ] **Problem:** Container resource limit yoksa host resource'ları tükenir.

**Senaryo:**
- Spring Boot application container memory limit yok
- Memory leak oluşur (`Order` entity'leri memory'de tutuluyor)
- Host memory tükenir (16GB → 15.9GB kullanım)
- Host crash olur (OOM killer devreye girer)

---

### b) Docker Volume Permission

- [ ] **Problem:** Volume mount permission problemi oluşur.

**Senaryo:**
- Docker compose'da host volume mount edilir (`/var/log/ecommerce:/app/logs`)
- Container user (UID 1000) farklı permission'a sahip
- Application log file write başarısız olur (`/app/logs/application.log`)
- Permission denied error

---

### c) Docker Network Isolation

- [ ] **Problem:** Container'lar aynı network'te birbirine erişebilir.

**Senaryo:**
- Docker compose'da tüm container'lar default network'te (ecommerce_default)
- PostgreSQL database container'a (postgres:5432) herkes erişebilir
- Spring Boot app, Redis, RabbitMQ container'ları database'e erişebilir
- Security risk oluşur (network isolation yok)

---

### d) Docker Image Layer Caching

- [ ] **Problem:** Image layer cache invalidate olursa rebuild çok uzun sürer.

**Senaryo:**
- Dockerfile'da Maven dependency değişir (`pom.xml` güncellenir)
- Tüm layer'lar rebuild edilir (FROM, COPY, RUN command'ları)
- Build 30 dakika sürer (dependency download, compile)
- CI/CD pipeline yavaşlar

---

### e) Docker Container Health Check

- [ ] **Problem:** Health check yoksa down container'a request gönderilir.

**Senaryo:**
- Spring Boot application container crash olur (OutOfMemoryError)
- Health check yok (`/actuator/health` endpoint kontrol edilmiyor)
- Load balancer container'a request gönderir (`/api/orders`)
- Request başarısız olur (connection refused)

---

### f) Docker Multi-Stage Build

- [ ] **Problem:** Multi-stage build kullanılmazsa image size çok büyük olur.

**Senaryo:**
- Dockerfile'da Maven build tool'lar final image'de kalır
- Image size: 2GB (Maven, JDK, dependencies)
- Multi-stage build ile: 200MB (sadece JAR file)
- Deployment yavaşlar (image pull 2GB → 200MB)

---

### g) Docker Container Logging

- [ ] **Problem:** Container log'ları disk'i doldurur.

**Senaryo:**
- Spring Boot application container sürekli log üretir (`/app/logs/application.log`)
- Log rotation yok (logback.xml'de maxFileSize yok)
- Disk dolar (100GB disk → 99.9GB log file)
- Host crash olur (disk full)

---

### h) Docker Compose Service Dependencies

- [ ] **Problem:** Service dependency yanlış tanımlanırsa startup sırası yanlış olur.

**Senaryo:**
- Docker compose'da Spring Boot app service PostgreSQL database'i bekler
- `depends_on` yok veya yanlış tanımlı
- App database'den önce başlar
- Connection error oluşur (`jdbc:postgresql://postgres:5432/ecommerce` connection refused)

---

### i) Docker Container Security

- [ ] **Problem:** Container root user ile çalışırsa security risk oluşur.

**Senaryo:**
- Spring Boot application container root user (UID 0) ile çalışır
- Container escape olursa (vulnerability exploit) host'a erişim
- Security risk oluşur (host file system'e erişim)
- Privilege escalation

---

### j) Docker Image Vulnerability

- [ ] **Problem:** Base image'de vulnerability varsa security risk oluşur.

**Senaryo:**
- Dockerfile base image: `openjdk:11` (eski, vulnerability var - CVE-2023-XXXX)
- Container'da vulnerability var
- Security scan (Trivy, Snyk) başarısız olur
- Production'a deploy edilemez (CI/CD pipeline fail)

---

### k) Docker Resource Exhaustion

- [ ] **Problem:** Çok fazla container çalışırsa host resource'ları tükenir.

**Senaryo:**
- Docker compose'da 100 Spring Boot application container aynı anda çalışır (scale up)
- Host CPU: 4 core
- CPU exhaustion oluşur (CPU %100 kullanım)
- Container'lar yavaşlar (response time 100ms → 5000ms)

---

### l) Docker Volume Backup

- [ ] **Problem:** Volume backup yapılmazsa data loss riski oluşur.

**Senaryo:**
- Docker compose'da PostgreSQL database volume var (`postgres_data:/var/lib/postgresql/data`)
- Backup yok (volume backup script yok)
- Volume silinirse (`docker volume rm postgres_data`) data kaybolur
- `orders`, `products`, `users` tablolarındaki tüm data kaybolur
- Data loss oluşur

---

## 32. ORM ve Hibernate Spesifik Problemler

### a) MultipleBagFetchException (Cannot simultaneously fetch multiple bags)

- [ ] **Problem:** Hibernate'te iki farklı `List` (Bag) aynı anda `EAGER` olarak fetch edilirse Cartesian Product oluşur ve Hibernate buna izin vermez.

**Senaryo:**
- `User` entity'sinde `List<Order>` ve `List<Address>` tanımlı (`@OneToMany`)
- Her ikisi de `@OneToMany(fetch = FetchType.EAGER)` ile işaretli
- `User` entity yüklendiğinde (`SELECT * FROM users WHERE user_id = ?`)
- Hibernate "cannot simultaneously fetch multiple bags" hatası fırlatılır
- (Çözüm: `Set` kullanmak veya `@BatchSize` kullanmak)

---

### b) StaleStateException (Optimistic Lock Exception)

- [ ] **Problem:** Versiyon kontrollü bir entity güncellenirken, başka bir transaction tarafından verinin değiştirilmiş olması.

**Senaryo:**
- `products` tablosunda product_id='abc-123', version=1
- Transaction-1: `Product` entity'sini okur (`SELECT * FROM products WHERE product_id = 'abc-123'`), version=1 görür
- Transaction-2: `Product` entity'sini okur ve günceller (`UPDATE products SET stock_quantity = 90, version = 2 WHERE product_id = 'abc-123'`)
- Transaction-1: Kendi elindeki veriyle (version=1) güncellemeye çalışır (`UPDATE products SET price = 1500, version = 2 WHERE product_id = 'abc-123' AND version = 1`)
- DB'deki version 2 olduğu için `StaleStateException` (veya `OptimisticLockException`) fırlatılır

---

### c) LazyInitializationException

- [ ] **Problem:** Hibernate Session (Transaction) kapandıktan sonra lazy-loaded bir koleksiyona veya proxy'ye erişilmeye çalışılması.

**Senaryo:**
- `ProductService.getProduct()` metodunda transaction commit edilir ve Hibernate session kapanır
- `ProductController`'da `product.getOrderItems().size()` çağrılır
- `OrderItem` listesi Lazy yüklendiği için (`@OneToMany(fetch = FetchType.LAZY)`) "no session" hatası alınır
- `LazyInitializationException` fırlatılır

---

### d) TransientPropertyValueException

- [ ] **Problem:** Kaydedilmemiş (transient) bir child entity, parent ile birlikte kaydedilmeye çalışılıyor ama cascade ayarı eksik.

**Senaryo:**
- Yeni bir `Category` oluşturulur (henüz `categories` tablosuna kaydedilmemiştir, category_id yok)
- Yeni bir `Product` oluşturulur ve bu `Category`'ye bağlanır (`product.setCategory(category)`)
- `Product` kaydedilmeye çalışılır (`productRepository.save(product)`)
- Hibernate `Category`'nin durumunu bilmediği için (`CascadeType.PERSIST` eksikliği) hata fırlatır
- `TransientPropertyValueException` fırlatılır

---

### e) NonUniqueObjectException

- [ ] **Problem:** Session cache içerisinde aynı ID'ye sahip iki farklı Java nesne instance'ının bulunması.

**Senaryo:**
- `entityManager.find(Product.class, product_id='abc-123')` ile `Product` entity yüklenir (session'da managed state)
- Dışarıdan parametre olarak gelen, yine product_id='abc-123' olan ama farklı bir Java nesnesi (Detached) `update` edilmeye çalışılır
- Hibernate session'da zaten product_id='abc-123' olan bir nesne olduğu için conflict oluşur
- `NonUniqueObjectException` fırlatılır

---

### f) PropertyValueException (not-null property references a null or transient value)

- [ ] **Problem:** Veritabanında Non-Nullable olan bir kolona null değer atanarak kaydedilmeye çalışılması.

**Senaryo:**
- `Product` entity'sinde `@Column(nullable = false)` tanımlı `name` alanı var
- Kod tarafında `product.setName(null)` veya değer atanmadan `productRepository.save(product)` çağrılır
- Hibernate DB'ye gitmeden veya giderken bu hatayı fırlatır
- `PropertyValueException` fırlatılır: "not-null property references a null or transient value"

---

### g) Hibernate Query Cache Invalidation

- [ ] **Problem:** Query cache invalidate edilmezse eski veri döner.

**Senaryo:**
- `SELECT * FROM products WHERE category = 'Electronics'` query cache'de tutulur
- `products` tablosuna yeni product eklenir (category='Electronics')
- Query cache invalidate edilmez
- Aynı query tekrar çalıştırıldığında eski liste döner (yeni product görünmez)

---

### h) Hibernate Second Level Cache Stale Data

- [ ] **Problem:** Second level cache güncellenmezse eski veri okunur.

**Senaryo:**
- `Product` entity second level cache'de tutulur (product_id='abc-123')
- `products` tablosunda product güncellenir (`UPDATE products SET price = 1500 WHERE product_id = 'abc-123'`)
- Cache invalidate edilmez
- `Product` entity okunduğunda eski veri (price=1000) okunur

---

### i) Hibernate N+1 Problem with @ManyToOne

- [ ] **Problem:** @ManyToOne ilişkilerde N+1 query problemi oluşur.
**Seviye:** Junior

**Senaryo:**
- `order_items` tablosundan 1000 `OrderItem` getirilir (1 query)
- Her `OrderItem` entity'si için `Product` ayrı query çalışır (`SELECT * FROM products WHERE product_id = ?`)
- Toplam: 1001 query (1 ana query + 1000 lazy load query)
- `OrderItem` entity'si `@ManyToOne(fetch = FetchType.LAZY)` ile `Product`'a bağlı

---

### j) Hibernate Detached Entity Merge

- [ ] **Problem:** Detached entity merge edilirken optimistic locking hatası oluşur.

**Senaryo:**
- `Product` entity detached state'de (session kapandı, product_id='abc-123', version=1)
- Başka bir transaction `products` tablosunda product'ı günceller (version=2)
- Detached `Product` merge edilmeye çalışılır (`entityManager.merge(product)`)
- OptimisticLockException fırlatılır (version mismatch: 1 vs 2)

---

### k) Hibernate Batch Insert Performance

- [ ] **Problem:** Batch insert yapılmazsa her insert için ayrı round-trip yapılır.
**Seviye:** Mid

**Senaryo:**
- `products` tablosuna 1000 product insert edilir
- Hibernate batch size ayarlanmamış (`hibernate.jdbc.batch_size` yok)
- Her insert için ayrı round-trip: 1000 `INSERT INTO products ...` query
- Batch size=50 ile: 20 query (50 product/batch)

---

### l) Hibernate Proxy Initialization

- [ ] **Problem:** Lazy proxy initialize edilirken session kapalıysa LazyInitializationException oluşur.

**Senaryo:**
- `Product` entity lazy proxy olarak döner (`SELECT * FROM products WHERE product_id = 'abc-123'`)
- Transaction commit edilir, Hibernate session kapanır
- `product.getCategory()` çağrılır (`Category` entity lazy load)
- `LazyInitializationException` fırlatılır (session kapalı, lazy load yapılamaz)

---

## 33. RabbitMQ Problemleri (Genişletilmiş)

### a) RabbitMQ Connection Leak

- [ ] **Problem:** Connection close edilmezse connection pool tükenir.

**Senaryo:**
- RabbitMQ connection açılır ("OrderCreated" event publish için)
- Exception oluşur (`RabbitTemplate.convertAndSend()` başarısız), connection close edilmez
- Connection pool tükenir (10 connection var, 10 leak)
- Yeni connection alınamaz (pool exhausted)

---

### b) RabbitMQ Channel Leak

- [ ] **Problem:** Channel close edilmezse channel limit'e ulaşılır.

**Senaryo:**
- Her `/api/orders` request'i için yeni RabbitMQ channel açılır
- Channel close edilmez (exception oluşursa)
- Channel limit'e ulaşılır (RabbitMQ default: 2047 channel/connection)
- Yeni channel açılamaz

---

### c) RabbitMQ Message Acknowledgment

- [ ] **Problem:** Message acknowledgment yapılmazsa mesaj tekrar kuyruğa döner.

**Senaryo:**
- RabbitMQ consumer "OrderCreated" mesajını işler (`payments` tablosuna insert)
- Acknowledgment yapılmaz (`channel.basicAck()` çağrılmaz)
- Connection kapanınca mesaj tekrar queue'ya döner
- Consumer mesajı tekrar işler → `payments` tablosuna duplicate payment eklenir
- Duplicate processing oluşur

---

### d) RabbitMQ Prefetch Count

- [ ] **Problem:** Prefetch count yüksek olursa load balancing bozulur.

**Senaryo:**
- RabbitMQ prefetch count: 1000
- 2 consumer var (PaymentService-1, PaymentService-2)
- PaymentService-1 tüm mesajları alır (1000 mesaj prefetch)
- PaymentService-2 boşta kalır (mesaj yok)
- Load balancing bozulur

---

### e) RabbitMQ Queue Durability

- [ ] **Problem:** Queue durable değilse RabbitMQ restart'ta queue kaybolur.

**Senaryo:**
- RabbitMQ queue "order.created" durable=false ile oluşturulur
- RabbitMQ restart olur
- Queue kaybolur
- Queue'daki "OrderCreated" mesajlar kaybolur
- `orders` tablosunda order var ama `payments` tablosunda payment yok

---

### f) RabbitMQ Message Durability

- [ ] **Problem:** Message persistent değilse RabbitMQ crash'te mesaj kaybolur.

**Senaryo:**
- RabbitMQ'ya "OrderCreated" mesajı persistent=false ile gönderilir
- RabbitMQ crash olur
- Mesaj kaybolur (memory'de tutuluyordu, disk'e yazılmadı)
- `orders` tablosunda order var ama `payments` tablosunda payment yok
- Data loss oluşur

---

### g) RabbitMQ Exchange Routing

- [ ] **Problem:** Exchange routing key yanlış olursa mesaj kaybolur.

**Senaryo:**
- RabbitMQ Topic exchange kullanılır
- Routing key: "order.created" (yanlış, "order.created" olmalı)
- Queue binding: "order.*" (tüm order event'leri)
- Mesaj doğru queue'ya gider
- Yanlış routing key ("order.create" gibi) ile mesaj kaybolur (hiçbir queue'ya gitmez)

---

### h) RabbitMQ TTL (Time To Live)

- [ ] **Problem:** Message TTL çok kısa olursa mesaj expire olur.

**Senaryo:**
- Message TTL: 5 dakika
- Consumer 10 dakika sonra işler
- Mesaj expire olur
- Data loss oluşur

---

### i) RabbitMQ Dead Letter Exchange

- [ ] **Problem:** Dead letter exchange yoksa başarısız mesajlar kaybolur.
**Seviye:** Mid

**Senaryo:**
- RabbitMQ consumer "OrderCreated" mesajı işleyemez (`payments` tablosuna insert başarısız)
- Dead letter exchange yok
- Mesaj kaybolur (queue'dan silinir)
- Retry yapılamaz
- `orders` tablosunda order var ama `payments` tablosunda payment yok

---

### j) RabbitMQ Consumer Prefetch

- [ ] **Problem:** Consumer prefetch yüksek olursa memory problemi oluşur.

**Senaryo:**
- RabbitMQ consumer prefetch: 10,000
- Payment service consumer yavaş işler (100 mesaj/saniye)
- 10,000 "OrderCreated" mesajı memory'de tutulur
- Memory overflow olur (OutOfMemoryError)

---

### k) RabbitMQ Cluster Split-Brain

- [ ] **Problem:** RabbitMQ cluster'da network partition olursa split-brain oluşur.

**Senaryo:**
- 3 node RabbitMQ cluster
- Network partition: 2 node bir tarafta, 1 node diğer tarafta
- Her iki taraf da aktif olur (her iki taraf da queue'ya mesaj alır)
- "OrderCreated" mesajları farklı node'larda farklı sırada işlenir
- Data inconsistency oluşur

---

### l) RabbitMQ Mirror Queue Sync

- [ ] **Problem:** Mirror queue sync lag oluşursa failover'da data loss olur.

**Senaryo:**
- RabbitMQ master node crash olur
- Mirror queue sync lag: 100 mesaj (henüz replicate olmadı)
- 100 "OrderCreated" mesajı kaybolur
- `orders` tablosunda 100 order var ama `payments` tablosunda payment yok
- Data loss oluşur

---

## 34. Redis Problemleri (Genişletilmiş)

### a) Redis Key Expiration Race Condition

- [ ] **Problem:** Key expire olurken aynı anda update edilirse data loss oluşur.

**Senaryo:**
- Redis'te key: `product:abc-123:stock` TTL: 10 saniye
- 9. saniyede key update edilir (`SET product:abc-123:stock 90 EX 10`)
- 10. saniyede key expire olur (TTL 0'a düşer)
- Update kaybolur (key silinir)
- `products` tablosundaki stock_quantity ile cache uyumsuz

---

### b) Redis Pipeline Atomicity

- [ ] **Problem:** Pipeline'da atomicity garantisi yok, bazı command'lar başarısız olabilir.

**Senaryo:**
- Redis pipeline'da 100 product key get edilir: `GET product:1`, `GET product:2`, ..., `GET product:100`
- 50. command başarısız olur (key yok: `product:50`)
- Diğer command'lar çalışır (99 key get edilir)
- Partial failure oluşur (bazı product'lar cache'den okunur, bazıları okunamaz)

---

### c) Redis Memory Pressure ve OOM

- [ ] **Problem:** Redis memory limit'e ulaşınca OOM (Out of Memory) oluşur.

**Senaryo:**
- Redis memory limit: 10GB
- `products` tablosundan 10GB product data cache'de tutulur
- Yeni product cache'lenir (`SET product:new-123 ...`)
- Eviction policy çalışmazsa (noeviction) OOM oluşur
- Redis crash olur

---

### d) Redis Slow Log ve Blocking Commands

- [ ] **Problem:** Blocking command'lar (BLPOP, BRPOP) Redis'i bloklar.

**Senaryo:**
- Redis BLPOP timeout: 60 saniye (queue'dan mesaj bekler)
- 100 client aynı anda BLPOP yapar (`BLPOP order:queue 60`)
- Redis 60 saniye block olur (single-threaded)
- Diğer request'ler (`GET product:abc-123`) bekler
- Latency artar (1ms → 60s)

---

### e) Redis Pub/Sub Message Loss

- [ ] **Problem:** Subscriber down olursa mesajlar kaybolur (fire-and-forget).

**Senaryo:**
- Publisher mesaj gönderir
- Subscriber down
- Mesaj kaybolur
- Message loss oluşur

---

### f) Redis Transaction DISCARD

- [ ] **Problem:** Transaction içinde exception oluşursa DISCARD yapılmazsa partial commit olur.

**Senaryo:**
- Redis MULTI başlatılır
- 5 command eklenir: `INCR product:abc-123:stock`, `INCR product:xyz-456:stock`, `INCR product:invalid:stock`, `INCR product:def-789:stock`, `INCR product:ghi-012:stock`
- 3. command başarısız olur (key yok, INCR çalışmaz)
- DISCARD yapılmazsa diğer command'lar çalışır (partial commit)
- Atomicity garantisi yok

---

### g) Redis Replication Lag

- [ ] **Problem:** Master'dan replica'ya replication lag oluşursa eski veri okunur.

**Senaryo:**
- Redis master'a write yapılır (`SET product:abc-123:stock 90`)
- Read replica'dan yapılır (`GET product:abc-123:stock`)
- Replication lag: 2 saniye (henüz replicate olmadı)
- Eski veri okunur (stock=100, yeni değer 90)

---

### h) Redis Sentinel Split-Brain

- [ ] **Problem:** Sentinel network partition durumunda iki master seçer.

**Senaryo:**
- Redis Sentinel: 3 sentinel, 1 master, 2 replica
- Network partition: 2 sentinel bir tarafta, 1 sentinel diğer tarafta
- Her iki taraf da yeni master seçer (her iki taraf da quorum'a ulaşır)
- Split-brain oluşur (2 master)
- `product:abc-123` key'i iki master'da farklı değerler alabilir

---

### i) Redis Cluster Hash Slot Migration

- [ ] **Problem:** Hash slot migration sırasında key'ler iki node'da da olabilir.

**Senaryo:**
- Redis cluster'a node eklenir, hash slot migration başlar
- `product:abc-123` key migration sırasında iki node'da da var (migration devam ediyor)
- Request yanlış node'a gider (`GET product:abc-123`)
- ASK redirect alınır (doğru node'a yönlendirilir)
- Latency artar (ekstra round-trip)

---

### j) Redis Lua Script Error Handling

- [ ] **Problem:** Lua script'te exception oluşursa script rollback yapmaz.

**Senaryo:**
- Redis Lua script 10 command çalıştırır: `product:abc-123` stock güncelleme
- 5. command başarısız olur (key yok: `product:invalid`)
- Script exception fırlatır
- İlk 4 command commit olur (partial commit)
- Atomicity garantisi yok

---

### k) Redis Connection Pool Exhaustion

- [ ] **Problem:** Connection pool size küçükse yüksek concurrency'de connection bekler.

**Senaryo:**
- Redis connection pool size: 10
- 100 eşzamanlı request gelir (`GET product:{product_id}`)
- Sadece 10 request connection alabilir
- Diğer 90 request bekler (connection timeout)
- Latency artar

---

### l) Redis Key Space Notification Loss

- [ ] **Problem:** Key space notification subscriber down olursa event'ler kaybolur.

**Senaryo:**
- Redis key space notification: `product:abc-123` key expire event'i publish edilir
- Subscriber (cache invalidation service) down
- Event kaybolur (fire-and-forget)
- `product:abc-123` cache invalidate edilmez
- Cache invalidation yapılamaz

---

## 35. Gözlemlenebilecek Problemler

### a) Response Time Degradation

- [ ] **Problem:** API response time zamanla artar, kullanıcı deneyimi kötüleşir.

**Senaryo:**
- `/api/products/search` endpoint'i başlangıçta response time: 100ms
- 1 hafta sonra: 500ms (`products` tablosunda 1 milyon ürün var)
- 1 ay sonra: 2000ms (`products` tablosunda 10 milyon ürün var, index yok)
- Kullanıcılar yavaşlıktan şikayet eder
- Timeout error'ları artar (30 saniye timeout)

---

### b) Memory Leak Detection

- [ ] **Problem:** Memory kullanımı sürekli artar, GC çalışsa bile memory düşmez.

**Senaryo:**
- Spring Boot application başlangıçta memory: 500MB
- 1 saat sonra: 1GB (`Order` entity'leri memory'de tutuluyor, clear edilmiyor)
- 24 saat sonra: 4GB (memory leak)
- GC çalışır ama memory düşmez
- OutOfMemoryError oluşur

---

### c) Database Connection Pool Monitoring

- [ ] **Problem:** Connection pool kullanımı %100'e ulaşır, yeni request'ler bekler.

**Senaryo:**
- HikariCP connection pool size: 20
- Active connections: 20 (`orders`, `products` tablolarına query yapılıyor)
- Waiting requests: 50 (`/api/orders` endpoint'ine request bekliyor)
- Request timeout oluşur (30 saniye)
- Service unavailable error'ları artar

---

### d) Error Rate Spike

- [ ] **Problem:** Error rate aniden artar, başarısız request sayısı yükselir.

**Senaryo:**
- `/api/orders` endpoint'i normal error rate: %0.1
- Aniden error rate: %10 (`products` tablosunda stock_quantity yetersiz)
- 1000 request'ten 100'ü başarısız (`QuantityNotAvailableException`)
- User experience kötüleşir
- Alert tetiklenir (error rate > %5)

---

### e) CPU Usage Pattern Anomaly

- [ ] **Problem:** CPU kullanımı normalden farklı pattern gösterir, bottleneck oluşur.

**Senaryo:**
- Spring Boot application normal CPU: %30-40
- Aniden CPU: %90-100 (`products` tablosunda full table scan query çalışıyor)
- Response time artar (100ms → 2000ms)
- Throughput düşer (1000 req/s → 100 req/s)
- System yavaşlar

---

### f) Disk I/O Bottleneck

- [ ] **Problem:** Disk I/O yüksek olur, database query'ler yavaşlar.

**Senaryo:**
- PostgreSQL disk read/write: 100 IOPS
- Aniden: 1000 IOPS (`orders` tablosuna 10,000 order/saniye insert)
- Database query'ler yavaşlar (`SELECT * FROM orders WHERE user_id = ?` 10ms → 500ms)
- Response time artar
- Timeout error'ları oluşur

---

### g) Network Latency Increase

- [ ] **Problem:** Network latency artar, external service call'lar yavaşlar.

**Senaryo:**
- Payment service external API call normal latency: 10ms
- Artış: 500ms (network problem)
- External API call'lar timeout olur (30 saniye timeout)
- Circuit breaker açılır (hystrix/resilience4j)
- `OrderService.createOrder()` payment service'i çağıramaz
- Service degradation oluşur

---

### h) Thread Pool Exhaustion

- [ ] **Problem:** Thread pool'daki thread'ler tükenir, yeni task'lar bekler.

**Senaryo:**
- Spring Boot thread pool size: 50
- Active threads: 50 (`OrderService.createOrder()` metodları çalışıyor)
- Waiting tasks: 200 (`/api/orders` endpoint'ine request bekliyor)
- Task'lar queue'da bekler
- Response time artar (100ms → 5000ms)

---

### i) Garbage Collection Pause

- [ ] **Problem:** GC pause süresi uzar, application freeze olur.

**Senaryo:**
- JVM normal GC pause: 50ms
- Aniden GC pause: 5 saniye (memory leak, çok fazla `Order` entity memory'de)
- Application 5 saniye freeze olur
- Request'ler timeout olur (`/api/orders` endpoint'i yanıt veremez)
- User experience kötüleşir

---

### j) Database Query Slowdown

- [ ] **Problem:** Database query execution time artar, timeout oluşur.

**Senaryo:**
- `products` tablosunda normal query time: 10ms (`SELECT * FROM products WHERE product_id = ?`)
- Artış: 5 saniye (index corruption, full table scan)
- Query timeout: 30 saniye
- Timeout error'ları oluşur
- Application yavaşlar (`/api/products/{productId}` endpoint'i yavaş)

---

### k) Cache Hit Rate Decrease

- [ ] **Problem:** Cache hit rate düşer, database load artar.

**Senaryo:**
- Redis cache normal hit rate: %90 (`product:{product_id}` key'leri cache'de)
- Düşüş: %50 (cache expire, eviction)
- `products` tablosuna database query sayısı 2x artar (1000 query/saniye → 2000 query/saniye)
- Response time artar (100ms → 200ms)
- Database load artar

---

### l) Message Queue Depth Increase

- [ ] **Problem:** Queue depth sürekli artar, mesajlar işlenemez.

**Senaryo:**
- RabbitMQ "OrderCreated" queue normal depth: 100
- Artış: 10,000 (payment service consumer yavaş)
- Consumer yavaş işler (100 mesaj/saniye, producer 1000 mesaj/saniye)
- Mesajlar birikir (10,000 mesaj queue'da)
- Processing delay oluşur (100 saniye gecikme)
- `orders` tablosunda order var ama `payments` tablosunda payment yok

---

### m) Active Session Count Growth

- [ ] **Problem:** Active session sayısı sürekli artar, memory tükenir.

**Senaryo:**
- Spring Session normal active sessions: 1000
- Artış: 10,000 (session timeout olmuyor)
- Memory kullanımı artar (her session 1MB → 10GB memory)
- Session timeout olmaz (TTL ayarı yok)
- Memory leak oluşur

---

### n) Database Lock Wait Time

- [ ] **Problem:** Database lock wait time artar, transaction'lar bekler.

**Senaryo:**
- `products` tablosunda normal lock wait: 10ms
- Artış: 5 saniye (hot spot, çok fazla concurrent update)
- Transaction'lar bekler (`UPDATE products SET stock_quantity = ... WHERE product_id = 'abc-123'`)
- Deadlock oluşabilir (2 transaction birbirini bekler)
- Timeout error'ları artar

---

### o) API Throughput Decrease

- [ ] **Problem:** API throughput düşer, sistem kapasitesi azalır.

**Senaryo:**
- `/api/orders` endpoint'i normal throughput: 1000 req/s
- Düşüş: 100 req/s (`products` tablosunda lock contention, slow query)
- Request'ler queue'da bekler (900 request/saniye bekliyor)
- Response time artar (100ms → 2000ms)
- Service degradation oluşur

---
