# TEST_PROBLEMS — Zorluk Sıralaması (Junior → Senior)

Bu liste [`TEST_PROBLEMS.md`](TEST_PROBLEMS.md) dosyasındaki tüm problemlerin **çözüm ve kavrama zorluğuna** göre sıralanmış halidir.

## Nasıl kullanılır?

1. **Seviye 1**'den başla; her maddeyi `TEST_PROBLEMS.md` içindeki senaryo ile eşleştir.
2. Aynı seviyede **Lab** etiketli maddelere öncelik ver (bu repoda reproduce edilebilir).
3. Bir seviyeyi bitirdikten sonra bir üst seviyeye geç.

## Seviye tanımları

| Seviye | Etiket | Deneyim (kabaca) | Odak |
|--------|--------|------------------|------|
| 1 | Junior | 0–2 yıl | Validation, temel güvenlik, config, basit JPA hataları |
| 2 | Junior+ | 1–3 yıl | N+1, index, pagination, Hibernate tuzakları (Lab) |
| 3 | Mid | 2–4 yıl | İzolasyon seviyeleri, Redis/MQ/Docker temelleri, migration |
| 4 | Mid+ | 3–6 yıl | Concurrency, lock, pool, cache stampede, 50M veri, observability |
| 5 | Senior | 5+ yıl | Sharding, saga, outbox, split-brain, exactly-once |
| 6 | Staff / Teori | 7+ yıl | CAP, FLP, Byzantine — mimari trade-off, mülakat derinliği |

---

## Seviye 1 — Junior

1. **API değişikliklerinde backward compatibility sorunları.**
   - Kaynak: Bölüm 14 / a) API Versioning

2. **Farklı environment'larda farklı config'ler.**
   - Kaynak: Bölüm 22 / a) Configuration Drift

3. **Internal exception'lar client'a expose edilir.**
   - Kaynak: Bölüm 15 / a) Exception Leakage

4. **Kullanıcı input'u doğrudan SQL query'ye eklenirse SQL injection riski oluşur.**
   - Kaynak: Bölüm 13 / a) SQL Injection

5. **Secret'lar (password, API key) kodda hardcode.**
   - Kaynak: Bölüm 22 / b) Secret Management

6. **Production'da stack trace client'a gönderilir.**
   - Kaynak: Bölüm 15 / b) Stack Trace Exposure

7. **Kullanıcı input'u HTML'e render edilirse XSS riski oluşur.**
   - Kaynak: Bölüm 13 / b) XSS (Cross-Site Scripting)

8. **Kullanıcı farkında olmadan istek gönderilebilir.**
   - Kaynak: Bölüm 13 / c) CSRF (Cross-Site Request Forgery)

9. **Error mesajlarında sensitive bilgi (database schema, file paths) olabilir.**
   - Kaynak: Bölüm 15 / c) Error Message Information Disclosure

10. **Hibernate Session (Transaction) kapandıktan sonra lazy-loaded bir koleksiyona veya proxy'ye erişilmeye çalışılması.**
   - Kaynak: Bölüm 32 / c) LazyInitializationException

11. **OrderStatus transition - InvalidStatusTransitionException**
   - Kaynak: Bölüm 4 / c) Order Status Inconsistency

12. **Büyük result set'lerde pagination yoksa memory problemi.**
   - Kaynak: Bölüm 14 / c) Pagination Problemleri

13. **Endpoint'ler authentication/authorization kontrolü yapmıyor.**
   - Kaynak: Bölüm 13 / d) Authentication ve Authorization

14. **API değişikliklerinde eski client'lar çalışmaz.**
   - Kaynak: Bölüm 14 / d) Backward Compatibility

15. **Kaydedilmemiş (transient) bir child entity, parent ile birlikte kaydedilmeye çalışılıyor ama cascade ayarı eksik.**
   - Kaynak: Bölüm 32 / d) TransientPropertyValueException

16. **Health check yoksa down container'a request gönderilir.**
   - Kaynak: Bölüm 31 / e) Docker Container Health Check

17. **Response'larda sensitive data (password, credit card) dönebilir.**
   - Kaynak: Bölüm 13 / e) Sensitive Data Exposure

18. **Veritabanında Non-Nullable olan bir kolona null değer atanarak kaydedilmeye çalışılması.**
   - Kaynak: Bölüm 32 / f) PropertyValueException (not-null property references a null or transient value)

19. **Service dependency yanlış tanımlanırsa startup sırası yanlış olur.**
   - Kaynak: Bölüm 31 / h) Docker Compose Service Dependencies

20. **Lazy proxy initialize edilirken session kapalıysa LazyInitializationException oluşur.**
   - Kaynak: Bölüm 32 / l) Hibernate Proxy Initialization

---

## Seviye 2 — Junior+

21. **Container resource limit yoksa host resource'ları tükenir.**
   - Kaynak: Bölüm 31 / a) Docker Container Resource Limits

22. **Aynı request iki kez gönderilirse duplicate işlem yapılır.**
   - Kaynak: Bölüm 17 / a) Duplicate Request

23. **Bir query sonucu için N tane ek query çalışır.**
   - Kaynak: Bölüm 3 / a) N+1 Query Problem

24. **Product güncellendi ama cache temizlenmedi - Kullanıcılar eski veriyi görür.**
   - Kaynak: Bölüm 6 / b) Cache Invalidation

25. **Volume mount permission problemi oluşur.**
   - Kaynak: Bölüm 31 / b) Docker Volume Permission

26. **Payment processing - Idempotency yoksa aynı order için iki kez ödeme yapılabilir.**
   - Kaynak: Bölüm 4 / b) Double Payment

27. **WHERE clause'da index kullanılmayan kolonlar.**
   - Kaynak: Bölüm 3 / b) Missing Index

28. **Aynı order için iki kez ödeme yapılabilir.**
   - Kaynak: Bölüm 17 / b) Payment Duplication

29. **API'ye sınırsız istek gönderilebilir, DDoS riski.**
   - Kaynak: Bölüm 14 / b) Rate Limiting

30. **Container'lar aynı network'te birbirine erişebilir.**
   - Kaynak: Bölüm 31 / c) Docker Network Isolation

31. **WHERE clause'da index kullanılmayan kolonlar.**
   - Kaynak: Bölüm 3 / c) Full Table Scan

32. **Retry mekanizması yoksa, geçici hatalar kalıcı hata gibi görünür.**
   - Kaynak: Bölüm 16 / c) Retry Logic Yetersizliği

33. **Image layer cache invalidate olursa rebuild çok uzun sürer.**
   - Kaynak: Bölüm 31 / d) Docker Image Layer Caching

34. **Session cache içerisinde aynı ID'ye sahip iki farklı Java nesne instance'ının bulunması.**
   - Kaynak: Bölüm 32 / e) NonUniqueObjectException

35. **Multi-stage build kullanılmazsa image size çok büyük olur.**
   - Kaynak: Bölüm 31 / f) Docker Multi-Stage Build

36. **Pipeline kullanılmazsa her command için round-trip yapılır.**
   - Kaynak: Bölüm 30 / f) Redis Pipeline Performance

37. **Container log'ları disk'i doldurur.**
   - Kaynak: Bölüm 31 / g) Docker Container Logging

38. **Query cache invalidate edilmezse eski veri döner.**
   - Kaynak: Bölüm 32 / g) Hibernate Query Cache Invalidation

39. **@ManyToOne ilişkilerde N+1 query problemi oluşur.**
   - Kaynak: Bölüm 32 / i) Hibernate N+1 Problem with @ManyToOne

40. **Çok fazla container çalışırsa host resource'ları tükenir.**
   - Kaynak: Bölüm 31 / k) Docker Resource Exhaustion

41. **Batch insert yapılmazsa her insert için ayrı round-trip yapılır.**
   - Kaynak: Bölüm 32 / k) Hibernate Batch Insert Performance

42. **Volume backup yapılmazsa data loss riski oluşur.**
   - Kaynak: Bölüm 31 / l) Docker Volume Backup

---

## Seviye 3 — Mid

43. **Bir transaction commit olmadan diğeri okuyabilir.**
   - Kaynak: Bölüm 2 / b) Dirty Read

44. **Aynı query iki kez çalıştırıldığında farklı sonuçlar döner.**
   - Kaynak: Bölüm 2 / c) Phantom Read

45. **Aynı transaction içinde aynı row iki kez okunduğunda farklı değerler.**
   - Kaynak: Bölüm 2 / d) Non-Repeatable Read

46. **Backup yoksa data loss riski.**
   - Kaynak: Bölüm 24 / a) Backup Strategy

47. **Migration başarısız olursa database inconsistent olur.**
   - Kaynak: Bölüm 23 / a) Migration Failure

48. **Consumer yavaşsa queue dolar, memory problemi oluşur.**
   - Kaynak: Bölüm 29 / a) Queue Backpressure

49. **Redis memory dolunca eviction policy ile key'ler silinir.**
   - Kaynak: Bölüm 30 / a) Redis Memory Eviction

50. **API Gateway down olursa tüm sistem down.**
   - Kaynak: Bölüm 27 / a) Single Point of Failure

51. **Belirli bir zamana geri dönülemez.**
   - Kaynak: Bölüm 24 / b) Point-in-Time Recovery

52. **Priority queue yoksa önemli mesajlar bekler.**
   - Kaynak: Bölüm 29 / b) Queue Priority

53. **Channel close edilmezse channel limit'e ulaşılır.**
   - Kaynak: Bölüm 33 / b) RabbitMQ Channel Leak

54. **Cache'de olmayan key'ler için sürekli DB query yapılır.**
   - Kaynak: Bölüm 30 / b) Redis Cache Penetration

55. **Pipeline'da atomicity garantisi yok, bazı command'lar başarısız olabilir.**
   - Kaynak: Bölüm 34 / b) Redis Pipeline Atomicity

56. **Yanlış service'e route edilir.**
   - Kaynak: Bölüm 27 / b) Request Routing

57. **Multi-instance cache - Instance-1'de product güncellendi, Instance-2 cache'i eski.**
   - Kaynak: Bölüm 6 / c) Cache Coherence

58. **Queue partition edilmezse hot partition problemi oluşur.**
   - Kaynak: Bölüm 29 / c) Queue Partitioning

59. **Message acknowledgment yapılmazsa mesaj tekrar kuyruğa döner.**
   - Kaynak: Bölüm 33 / c) RabbitMQ Message Acknowledgment

60. **Çok sayıda key aynı anda expire olunca DB'ye stampede oluşur.**
   - Kaynak: Bölüm 30 / c) Redis Cache Avalanche

61. **Redis memory limit'e ulaşınca OOM (Out of Memory) oluşur.**
   - Kaynak: Bölüm 34 / c) Redis Memory Pressure ve OOM

62. **Çok büyük mesajlar queue'yu bloklar.**
   - Kaynak: Bölüm 29 / d) Queue Message Size

63. **Prefetch count yüksek olursa load balancing bozulur.**
   - Kaynak: Bölüm 33 / d) RabbitMQ Prefetch Count

64. **Belirli key'lere çok fazla access olur, hot key problemi.**
   - Kaynak: Bölüm 30 / d) Redis Hot Key

65. **Blocking command'lar (BLPOP, BRPOP) Redis'i bloklar.**
   - Kaynak: Bölüm 34 / d) Redis Slow Log ve Blocking Commands

66. **Consumer sayısı artırıldığında duplicate processing oluşur.**
   - Kaynak: Bölüm 29 / e) Queue Consumer Scaling

67. **Queue durable değilse RabbitMQ restart'ta queue kaybolur.**
   - Kaynak: Bölüm 33 / e) RabbitMQ Queue Durability

68. **Çok büyük key'ler Redis'i bloklar.**
   - Kaynak: Bölüm 30 / e) Redis Big Key

69. **Subscriber down olursa mesajlar kaybolur (fire-and-forget).**
   - Kaynak: Bölüm 34 / e) Redis Pub/Sub Message Loss

70. **Dead letter queue dolunca yeni mesajlar kaybolur.**
   - Kaynak: Bölüm 29 / f) Queue Dead Letter Queue Overflow

71. **Message persistent değilse RabbitMQ crash'te mesaj kaybolur.**
   - Kaynak: Bölüm 33 / f) RabbitMQ Message Durability

72. **Transaction içinde exception oluşursa DISCARD yapılmazsa partial commit olur.**
   - Kaynak: Bölüm 34 / f) Redis Transaction DISCARD

73. **Message TTL çok kısa olursa mesajlar expire olur.**
   - Kaynak: Bölüm 29 / g) Queue Message TTL

74. **Exchange routing key yanlış olursa mesaj kaybolur.**
   - Kaynak: Bölüm 33 / g) RabbitMQ Exchange Routing

75. **Master'dan replica'ya replication lag oluşursa eski veri okunur.**
   - Kaynak: Bölüm 34 / g) Redis Replication Lag

76. **WATCH kullanılmazsa optimistic locking çalışmaz.**
   - Kaynak: Bölüm 30 / g) Redis Transaction WATCH

77. **Second level cache güncellenmezse eski veri okunur.**
   - Kaynak: Bölüm 32 / h) Hibernate Second Level Cache Stale Data

78. **Batch processing yapılmazsa throughput düşer.**
   - Kaynak: Bölüm 29 / h) Queue Batch Processing

79. **Message TTL çok kısa olursa mesaj expire olur.**
   - Kaynak: Bölüm 33 / h) RabbitMQ TTL (Time To Live)

80. **Subscriber down olursa mesajlar kaybolur.**
   - Kaynak: Bölüm 30 / h) Redis Pub/Sub Message Loss

81. **Container root user ile çalışırsa security risk oluşur.**
   - Kaynak: Bölüm 31 / i) Docker Container Security

82. **Consumer group rebalancing sırasında duplicate processing.**
   - Kaynak: Bölüm 29 / i) Queue Consumer Group Rebalancing

83. **Dead letter exchange yoksa başarısız mesajlar kaybolur.**
   - Kaynak: Bölüm 33 / i) RabbitMQ Dead Letter Exchange

84. **Sentinel failover sırasında data loss oluşabilir.**
   - Kaynak: Bölüm 30 / i) Redis Sentinel Failover

85. **Base image'de vulnerability varsa security risk oluşur.**
   - Kaynak: Bölüm 31 / j) Docker Image Vulnerability

86. **Consumer prefetch yüksek olursa memory problemi oluşur.**
   - Kaynak: Bölüm 33 / j) RabbitMQ Consumer Prefetch

87. **Cluster slot migration sırasında request'ler başarısız olur.**
   - Kaynak: Bölüm 30 / j) Redis Cluster Slot Migration

88. **Lua script'te exception oluşursa script rollback yapmaz.**
   - Kaynak: Bölüm 34 / j) Redis Lua Script Error Handling

89. **Memory fragmentation nedeniyle memory kullanımı artar.**
   - Kaynak: Bölüm 30 / k) Redis Memory Fragmentation

90. **Key space notification subscriber down olursa event'ler kaybolur.**
   - Kaynak: Bölüm 34 / l) Redis Key Space Notification Loss

91. **Lua script çok uzun sürerse Redis block olur.**
   - Kaynak: Bölüm 30 / l) Redis Lua Script Timeout

---

## Seviye 4 — Mid+

92. **Sistemin darboğazı nerede?**
   - Kaynak: Bölüm 20 / a) Bottleneck Detection

93. **Product cache expire olunca 1000 request aynı anda cache miss → 1000 DB query.**
   - Kaynak: Bölüm 6 / a) Cache Stampede

94. **Multi-service request'lerde trace kaybolur.**
   - Kaynak: Bölüm 21 / a) Distributed Tracing

95. **RabbitMQ'da aynı mesaj iki kez işlenebilir.**
   - Kaynak: Bölüm 18 / a) Duplicate Messages

96. **İki transaction aynı veriyi okur, her ikisi de günceller, son güncelleme kaybolur.**
   - Kaynak: Bölüm 2 / a) Lost Update

97. **Stock kontrolü yapılıyor ama eşzamanlı order'larda race condition olabilir.**
   - Kaynak: Bölüm 4 / a) Negative Stock

98. **Connection close edilmezse connection pool tükenir.**
   - Kaynak: Bölüm 33 / a) RabbitMQ Connection Leak

99. **Aynı anda birden fazla kullanıcı aynı üründen satın almaya çalışırsa, stock kontrolü yetersiz kalabilir.**
   - Kaynak: Bölüm 1 / a) Race Condition - Stock Güncellemesi

100. **Write yapıldıktan sonra read yapıldığında eski veri okunabilir.**
   - Kaynak: Bölüm 19 / a) Read-Your-Writes

101. **Key expire olurken aynı anda update edilirse data loss oluşur.**
   - Kaynak: Bölüm 34 / a) Redis Key Expiration Race Condition

102. **API response time zamanla artar, kullanıcı deneyimi kötüleşir.**
   - Kaynak: Bölüm 35 / a) Response Time Degradation

103. **Retry mekanizması yoksa, başarısız istekler tekrar tekrar gönderilir.**
   - Kaynak: Bölüm 16 / a) Retry Storm

104. **Yeni instance register olmazsa keşfedilmez.**
   - Kaynak: Bölüm 26 / a) Service Registration

105. **Load balancer session'ı farklı instance'a yönlendirir.**
   - Kaynak: Bölüm 25 / a) Sticky Session

106. **İki transaction farklı row'ları okur, her ikisi de günceller, ama constraint violation oluşur.**
   - Kaynak: Bölüm 27b / a) Write Skew (Phantom Write)

107. **Down service'e sürekli istek gönderilir.**
   - Kaynak: Bölüm 16 / b) Circuit Breaker

108. **İki transaction birbirini beklerken deadlock oluşabilir.**
   - Kaynak: Bölüm 1 / b) Deadlock

109. **Down instance'a istek gönderilir.**
   - Kaynak: Bölüm 25 / b) Health Check

110. **Tek instance yeterli değil, scale out gerekli.**
   - Kaynak: Bölüm 20 / b) Horizontal Scaling

111. **Multi-instance log'ları toplamak zor.**
   - Kaynak: Bölüm 21 / b) Log Aggregation

112. **Memory kullanımı sürekli artar, GC çalışsa bile memory düşmez.**
   - Kaynak: Bölüm 35 / b) Memory Leak Detection

113. **Mesajlar sırayla işlenmeyebilir.**
   - Kaynak: Bölüm 18 / b) Message Ordering

114. **Instance down olunca deregister olmaz.**
   - Kaynak: Bölüm 26 / b) Service Deregistration

115. **Check ve use arasında state değişir.**
   - Kaynak: Bölüm 27b / b) Time-of-Check-Time-of-Use (TOCTOU)

116. **Bir service down olunca diğer service'ler de down olur.**
   - Kaynak: Bölüm 27b / c) Cascading Failure

117. **Yüksek concurrency'de connection pool tükenir.**
   - Kaynak: Bölüm 20 / c) Database Connection Pool Exhaustion

118. **Connection pool kullanımı %100'e ulaşır, yeni request'ler bekler.**
   - Kaynak: Bölüm 35 / c) Database Connection Pool Monitoring

119. **Başarısız mesajlar kaybolur.**
   - Kaynak: Bölüm 18 / c) Dead Letter Queue

120. **Performance metrikleri toplanmıyor.**
   - Kaynak: Bölüm 21 / c) Metrics Collection

121. **HikariCP pool size küçükse, yüksek concurrency'de connection bekler.**
   - Kaynak: Bölüm 3 / d) Connection Pool Exhaustion

122. **Error rate aniden artar, başarısız request sayısı yükselir.**
   - Kaynak: Bölüm 35 / d) Error Rate Spike

123. **Mesajlar kaybolabilir.**
   - Kaynak: Bölüm 18 / d) Message Loss

124. **Cache expire olunca tüm request'ler aynı anda DB'ye gider.**
   - Kaynak: Bölüm 27b / d) Thundering Herd Problem

125. **CPU kullanımı normalden farklı pattern gösterir, bottleneck oluşur.**
   - Kaynak: Bölüm 35 / e) CPU Usage Pattern Anomaly

126. **Recursive CTE'ler büyük veri setlerinde çok yavaş çalışır.**
   - Kaynak: Bölüm 28 / e) CTE (Common Table Expression) - Recursive Query Performance

127. **Transaction çok uzun sürerse lock'lar uzun süre tutulur.**
   - Kaynak: Bölüm 27b / e) Long Transaction Problem

128. **Birden fazla CTE kullanıldığında query plan kötüleşir.**
   - Kaynak: Bölüm 28 / f) CTE - Multiple CTE Performance

129. **Transaction commit/rollback olmazsa connection pool'da leak oluşur.**
   - Kaynak: Bölüm 27b / f) Database Connection Leak

130. **Disk I/O yüksek olur, database query'ler yavaşlar.**
   - Kaynak: Bölüm 35 / f) Disk I/O Bottleneck

131. **Materialized view güncellenmezse eski veri gösterilir.**
   - Kaynak: Bölüm 28 / g) Materialized View - Stale Data

132. **Entity Manager'da entity'ler clear edilmezse memory leak oluşur.**
   - Kaynak: Bölüm 27b / g) Memory Leak in Entity Manager

133. **Network latency artar, external service call'lar yavaşlar.**
   - Kaynak: Bölüm 35 / g) Network Latency Increase

134. **Materialized view refresh çok uzun sürer, lock oluşur.**
   - Kaynak: Bölüm 28 / h) Materialized View - Refresh Performance

135. **Farklı parametrelerle aynı query farklı plan kullanır.**
   - Kaynak: Bölüm 27b / h) Query Plan Cache Pollution

136. **Thread pool'daki thread'ler tükenir, yeni task'lar bekler.**
   - Kaynak: Bölüm 35 / h) Thread Pool Exhaustion

137. **GC pause süresi uzar, application freeze olur.**
   - Kaynak: Bölüm 35 / i) Garbage Collection Pause

138. **Çok fazla row-level lock table-level lock'a escalate olur.**
   - Kaynak: Bölüm 27b / i) Lock Escalation

139. **Full refresh yerine incremental refresh yapılmazsa performans düşer.**
   - Kaynak: Bölüm 28 / i) Materialized View - Incremental Refresh

140. **Database query execution time artar, timeout oluşur.**
   - Kaynak: Bölüm 35 / j) Database Query Slowdown

141. **Detached entity merge edilirken optimistic locking hatası oluşur.**
   - Kaynak: Bölüm 32 / j) Hibernate Detached Entity Merge

142. **Bir update birden fazla disk write'a neden olur.**
   - Kaynak: Bölüm 27b / j) Write Amplification

143. **Cache hit rate düşer, database load artar.**
   - Kaynak: Bölüm 35 / k) Cache Hit Rate Decrease

144. **READ COMMITTED isolation level'da snapshot isolation kullanılırsa version store büyür.**
   - Kaynak: Bölüm 27b / k) Read Committed Snapshot Isolation (RCSI) Problemleri

145. **Connection pool size küçükse yüksek concurrency'de connection bekler.**
   - Kaynak: Bölüm 34 / k) Redis Connection Pool Exhaustion

146. **Belirli row'lara çok fazla concurrent access olur.**
   - Kaynak: Bölüm 27b / l) Hot Spot Problem

147. **Queue depth sürekli artar, mesajlar işlenemez.**
   - Kaynak: Bölüm 35 / l) Message Queue Depth Increase

148. **Active session sayısı sürekli artar, memory tükenir.**
   - Kaynak: Bölüm 35 / m) Active Session Count Growth

149. **Farklı thread'ler aynı cache line'ı kullanır.**
   - Kaynak: Bölüm 27b / m) False Sharing (CPU Cache)

150. **Lock-free data structure'larda value değişir ama aynı değere geri döner.**
   - Kaynak: Bölüm 27b / n) ABA Problem

151. **Database lock wait time artar, transaction'lar bekler.**
   - Kaynak: Bölüm 35 / n) Database Lock Wait Time

152. **API throughput düşer, sistem kapasitesi azalır.**
   - Kaynak: Bölüm 35 / o) API Throughput Decrease

153. **Yüksek öncelikli thread düşük öncelikli thread'i bekler.**
   - Kaynak: Bölüm 27b / o) Priority Inversion

154. **Thread'ler sürekli çalışır ama ilerleme kaydetmez.**
   - Kaynak: Bölüm 27b / p) Livelock

155. **Bazı thread'ler hiç çalışmaz.**
   - Kaynak: Bölüm 27b / q) Starvation

156. **CPU reordering nedeniyle instruction'lar farklı sırada execute edilir.**
   - Kaynak: Bölüm 27b / r) Memory Ordering Problem

157. **Optimistic locking false positive verir (gerçekte conflict yok).**
   - Kaynak: Bölüm 27b / s) False Positive in Optimistic Locking

158. **Farklı instance'larda saat farklı → Event ordering problemi.**
   - Kaynak: Bölüm 27b / t) Distributed System Clock Skew

---

## Seviye 5 — Senior

159. **Sharded database'de cross-shard query'ler çok yavaş çalışır.**
   - Kaynak: Bölüm 28 / a) Database Sharding - Cross-Shard Query

160. **Order creation → Payment → Shipment - Bir adım başarısız olursa rollback nasıl yapılır?**
   - Kaynak: Bölüm 5 / a) Distributed Transaction

161. **RabbitMQ ile async event'ler - Order created ama payment event henüz işlenmedi.**
   - Kaynak: Bölüm 5 / b) Eventual Consistency

162. **Distributed system'de veri tutarsızlığı.**
   - Kaynak: Bölüm 19 / b) Eventual Consistency

163. **Yanlış shard key seçilirse hot shard problemi oluşur.**
   - Kaynak: Bölüm 28 / b) Shard Key Selection

164. **Migration sırasında downtime olur.**
   - Kaynak: Bölüm 23 / b) Zero-Downtime Migration

165. **Read replica'da replication lag oluşur, eski veri okunur.**
   - Kaynak: Bölüm 28 / c) Database Cluster - Read Replica Lag

166. **Redis ile distributed lock - Multi-instance environment'ta stock güncellemesi.**
   - Kaynak: Bölüm 5 / c) Distributed Lock

167. **Network partition durumunda iki master oluşur.**
   - Kaynak: Bölüm 19 / c) Split-Brain Problem

168. **Cluster'da network partition olursa split-brain oluşur.**
   - Kaynak: Bölüm 28 / d) Database Cluster - Split-Brain

169. **Sentinel network partition durumunda iki master seçer.**
   - Kaynak: Bölüm 34 / h) Redis Sentinel Split-Brain

170. **Hash slot migration sırasında key'ler iki node'da da olabilir.**
   - Kaynak: Bölüm 34 / i) Redis Cluster Hash Slot Migration

171. **Shard rebalancing sırasında data migration problemi.**
   - Kaynak: Bölüm 28 / j) Database Sharding - Rebalancing

172. **Exactly-once semantics garantisi yoksa duplicate veya loss oluşur.**
   - Kaynak: Bölüm 29 / j) Queue Exactly-Once Semantics

173. **RabbitMQ cluster'da network partition olursa split-brain oluşur.**
   - Kaynak: Bölüm 33 / k) RabbitMQ Cluster Split-Brain

174. **Mirror queue sync lag oluşursa failover'da data loss olur.**
   - Kaynak: Bölüm 33 / l) RabbitMQ Mirror Queue Sync

175. **Network partition durumunda iki instance aynı lock'u alır.**
   - Kaynak: Bölüm 27b / u) Split-Brain in Distributed Lock

---

## Seviye 6 — Staff / İleri Teori

176. **Bir node yanlış bilgi gönderir (malicious veya buggy).**
   - Kaynak: Bölüm 27b / v) Byzantine Failure

177. **Consistency, Availability, Partition tolerance - İkisini seçmek zorundasın.**
   - Kaynak: Bölüm 27b / w) CAP Theorem Trade-offs

178. **Network'te mesaj kaybolabilir, acknowledgment garantisi yok.**
   - Kaynak: Bölüm 27b / x) Two Generals Problem

179. **Asynchronous system'de consensus imkansız (Fischer-Lynch-Paterson).**
   - Kaynak: Bölüm 27b / y) FLP Impossibility

180. **Distributed system'de operation ordering garantisi.**
   - Kaynak: Bölüm 27b / z) Linearizability vs Sequential Consistency

---

## Özet

| Seviye | Madde sayısı |
|--------|--------------|
| 1 — Junior | 20 |
| 2 — Junior+ | 22 |
| 3 — Mid | 49 |
| 4 — Mid+ | 67 |
| 5 — Senior | 17 |
| 6 — Staff / İleri Teori | 5 |
| **Toplam** | **180** |

---

*Otomatik sıralama + manuel kural seti ile üretildi. Detaylı senaryolar için her maddenin kaynak bölümüne bakın.*