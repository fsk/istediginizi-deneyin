import psycopg
from psycopg.rows import tuple_row
from faker import Faker
import random
import uuid

fake = Faker()
random.seed(42)

# ===================== DATA POOLS =====================

HOBBIES_BY_CATEGORY = {
    "TECH": [
        "Coding", "Open Source", "System Design", "Distributed Systems",
        "Machine Learning", "Data Science", "Cyber Security"
    ],
    "MIND_GAMES": [
        "Gaming", "Chess", "Puzzle Solving", "Board Games"
    ],
    "SPORTS": [
        "Running", "Cycling", "Hiking", "Swimming", "Fitness",
        "CrossFit", "Yoga", "Climbing"
    ],
    "ARTS_MUSIC": [
        "Photography", "Drawing", "Painting", "Digital Art",
        "Music", "Guitar", "Piano", "Music Production"
    ],
    "LIFESTYLE": [
        "Traveling", "Backpacking", "Cooking", "Baking",
        "Coffee Brewing", "Wine Tasting",
        "Reading", "Writing", "Podcast Listening",
        "Movie Watching", "Netflix"
    ]
}

# Flattened list for easy random selection
HOBBIES = [hobby for hobbies in HOBBIES_BY_CATEGORY.values() for hobby in hobbies]

BIO_SENTENCES = [
    "Software engineer with a passion for scalable systems and distributed architectures. Enjoys solving complex problems and building high-performance applications.",
    "Backend developer specializing in microservices and cloud-native solutions. Always exploring new technologies and best practices in software engineering.",
    "Full-stack developer who loves working on high-traffic platforms and optimizing user experiences. Passionate about clean code and test-driven development.",
    "Open source contributor and clean code advocate. Believes in the power of community-driven development and knowledge sharing.",
    "System architect interested in performance optimization and scalability challenges. Enjoys designing robust systems that can handle millions of requests.",
    "Coffee enthusiast who spends weekends exploring new cafes and perfecting the art of pour-over brewing. Also passionate about specialty coffee origins.",
    "Avid traveler who has visited over 30 countries and loves discovering new cultures, cuisines, and local traditions. Always planning the next adventure.",
    "Bookworm and lifelong learner who reads across multiple genres. Particularly interested in science fiction, philosophy, and biographies of tech pioneers.",
    "Tech professional by day, competitive gamer by night. Enjoys both building software and playing strategy games that challenge the mind.",
    "Always curious and constantly learning. Believes that the best way to grow is by stepping outside your comfort zone and embracing new challenges.",
    "Product manager who enjoys building things and breaking them to understand how they work. Passionate about user-centered design and data-driven decisions.",
    "DevOps engineer who believes in continuous improvement and automation. Loves infrastructure as code and making deployments seamless and reliable.",
    "Music producer and audio engineer in my spare time. Enjoys creating electronic music and experimenting with different sound design techniques.",
    "Fitness enthusiast who balances coding with regular gym sessions and outdoor activities. Believes a healthy body supports a sharp mind.",
    "Movie buff and film critic who watches everything from indie films to blockbusters. Particularly interested in cinematography and storytelling techniques.",
    "Data scientist passionate about machine learning and artificial intelligence. Enjoys working on projects that combine technical skills with real-world impact.",
    "UI/UX designer who believes great design is invisible. Focuses on creating intuitive user experiences that make technology accessible to everyone.",
    "Cybersecurity expert dedicated to protecting digital assets and educating others about online safety. Always staying updated on the latest threats and defenses.",
    "Entrepreneur and startup founder with experience in building products from scratch. Enjoys the challenge of turning ideas into successful businesses.",
    "Technical writer who loves explaining complex concepts in simple terms. Believes good documentation is as important as good code.",
    "Mobile app developer specializing in iOS and Android native development. Passionate about creating smooth, responsive user interfaces.",
    "Blockchain developer exploring the potential of decentralized technologies. Interested in DeFi, NFTs, and the future of digital ownership.",
    "Photographer who captures moments and tells stories through images. Enjoys both digital and film photography, especially street and portrait photography.",
    "Chef at heart who loves experimenting with new recipes and cooking techniques. Enjoys hosting dinner parties and sharing meals with friends.",
    "Yoga instructor and mindfulness practitioner who believes in the connection between mental and physical well-being. Practices daily meditation.",
    "Marathon runner who has completed races in multiple cities. Training for the next big challenge while balancing work and personal life.",
    "Language learner currently studying my third language. Believes learning languages opens doors to understanding different cultures and perspectives.",
    "Podcast host discussing technology trends and interviewing industry leaders. Enjoys deep conversations about the future of tech and society.",
    "Maker and DIY enthusiast who builds everything from furniture to electronics. Loves the satisfaction of creating something with my own hands.",
    "Nature photographer who spends weekends hiking and capturing landscapes. Believes spending time in nature is essential for creativity and mental health.",
    "Board game designer working on my first game. Enjoys the challenge of creating engaging mechanics and balancing gameplay elements.",
    "Volunteer teacher who helps kids learn programming on weekends. Believes in making technology education accessible to everyone, regardless of background.",
    "Vintage car enthusiast who restores classic vehicles in my garage. Enjoys the mechanical challenge and the history behind each car.",
    "Home brewer experimenting with different beer styles and fermentation techniques. Always looking for the perfect recipe and flavor profile.",
    "Urban gardener growing vegetables and herbs on my balcony. Enjoys the process of growing food and the satisfaction of a home-cooked meal with fresh ingredients.",
    "Meditation and mindfulness coach who practices daily. Believes in the power of presence and awareness in both personal and professional life.",
    "Rock climber who tackles both indoor and outdoor routes. Enjoys the physical challenge and the mental problem-solving aspect of climbing.",
    "Amateur astronomer who spends clear nights observing the cosmos. Fascinated by the universe and our place within it.",
    "Sustainable living advocate who tries to minimize environmental impact. Interested in renewable energy and eco-friendly technologies.",
    "Vintage vinyl collector with a growing collection of rare records. Enjoys the warm sound of analog music and the ritual of playing records.",
    "Freelance graphic designer who works on branding and visual identity projects. Believes good design communicates ideas effectively and beautifully.",
    "Community organizer who helps bring tech professionals together through meetups and events. Enjoys building networks and fostering collaboration.",
    "Sourdough baker who has perfected the art of fermentation. Enjoys the science behind bread making and sharing fresh loaves with neighbors.",
    "Wildlife conservation volunteer who supports local environmental initiatives. Passionate about protecting biodiversity and natural habitats.",
    "Stand-up comedian who performs at local open mic nights. Enjoys the challenge of making people laugh and the vulnerability of live performance.",
    "Minimalist who believes in living with less and focusing on what truly matters. Enjoys the freedom that comes with intentional living.",
    "History buff who reads extensively about world history and ancient civilizations. Fascinated by how the past shapes our present and future.",
    "Salsa dancer who attends classes and social events regularly. Enjoys the music, movement, and social connection that dancing brings.",
    "Sustainable fashion advocate who supports ethical brands and second-hand shopping. Believes in quality over quantity and conscious consumption."
]

PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "paypal",
    "wire_transfer",
    "apple_pay",
    "google_pay",
    "crypto"
]

SHIPMENT_STATUSES = [
    "created",
    "packed",
    "shipped",
    "in_transit",
    "out_for_delivery",
    "delivered",
    "delivery_failed",
    "returned",
    "cancelled"
]

SHIPMENT_STATUS_WEIGHTS = [
    0.05,  # created
    0.10,  # packed
    0.20,  # shipped
    0.25,  # in_transit
    0.15,  # out_for_delivery
    0.20,  # delivered
    0.03,  # delivery_failed
    0.01,  # returned
    0.01   # cancelled
]

ORDER_STATUSES = [
    "PENDING",
    "CONFIRMED",
    "PROCESSING",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
    "REFUNDED"
]

ORDER_STATUS_WEIGHTS = [
    0.05,  # PENDING
    0.15,  # CONFIRMED
    0.20,  # PROCESSING
    0.15,  # SHIPPED
    0.35,  # DELIVERED
    0.05,  # CANCELLED
    0.05   # REFUNDED
]

PAYMENT_STATUSES = [
    "PENDING",
    "PROCESSING",
    "COMPLETED",
    "FAILED",
    "REFUNDED",
    "CANCELLED"
]

PAYMENT_STATUS_WEIGHTS = [
    0.05,  # PENDING
    0.10,  # PROCESSING
    0.75,  # COMPLETED
    0.05,  # FAILED
    0.03,  # REFUNDED
    0.02   # CANCELLED
]

PRODUCT_CATEGORIES = [
    "Electronics", "Clothing", "Books", "Home & Garden",
    "Sports & Outdoors", "Toys & Games", "Beauty & Personal Care",
    "Automotive", "Food & Beverages", "Health & Wellness"
]

BRANDS = [
    "TechCorp", "StyleBrand", "HomeEssentials", "SportMax",
    "BeautyPlus", "AutoPro", "FoodFresh", "WellnessCo"
]

SHIPMENT_CARRIERS = [
    "UPS", "FedEx", "DHL", "USPS", "Amazon Logistics"
]

ADDRESS_TYPES = ["HOME", "WORK", "BILLING", "SHIPPING", "OTHER"]

GENDERS = ["MALE", "FEMALE", "OTHER", "PREFER_NOT_TO_SAY"]
GENDER_WEIGHTS = [0.48, 0.48, 0.02, 0.02]  # MALE, FEMALE, OTHER, PREFER_NOT_TO_SAY

CARD_TYPES = ["VISA", "MASTERCARD", "AMEX", "DISCOVER"]
CARD_STATUSES = ["ACTIVE", "EXPIRED", "BLOCKED", "CANCELLED"]
CARD_STATUS_WEIGHTS = [0.85, 0.05, 0.05, 0.05]  # ACTIVE, EXPIRED, BLOCKED, CANCELLED

USER_COUNT = 500_000
PRODUCT_COUNT = 200_000
ORDER_COUNT = 4_000_000
BATCH_SIZE = 10_000


def get_postgresql_connection():
    return psycopg.connect(
        "dbname=ecommerce user=fsk password=fsk host=localhost port=2345",
        autocommit=False
    )


def generate_data():
    with get_postgresql_connection() as conn:
        with conn.cursor(row_factory=tuple_row) as cur:

            user_ids = []
            product_ids = []

            print("Start generating data")

            # 1. USERS
            print("Generating users")
            for i in range(0, USER_COUNT, BATCH_SIZE):
                batch = []
                for j in range(i, i + BATCH_SIZE):
                    # Phone number'ı 20 karakterle sınırla
                    phone = None
                    if random.random() < 0.8:
                        phone_raw = fake.phone_number()
                        phone = phone_raw[:20] if len(phone_raw) <= 20 else fake.numerify(text='+1-###-###-####')
                    
                    batch.append((
                        str(uuid.uuid4()),
                        fake.user_name() + str(j),
                        fake.unique.email(),
                        fake.first_name(),
                        fake.last_name(),
                        phone,
                        random.choice(BIO_SENTENCES) if random.random() < 0.7 else None,
                        fake.image_url() if random.random() < 0.5 else None,
                        fake.date_of_birth(minimum_age=18, maximum_age=80),
                        random.choices(GENDERS, weights=GENDER_WEIGHTS, k=1)[0] if random.random() < 0.9 else None
                    ))

                cur.executemany(
                    """INSERT INTO users 
                    (user_id, username, email, first_name, last_name, phone_number, 
                     bio, profile_image_url, date_of_birth, gender)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    batch
                )

                user_ids.extend([r[0] for r in batch])
                conn.commit()

            print(f"Users inserted: {len(user_ids)}")

            # 1.5. ADDRESSES
            print("Generating addresses")
            address_ids_map = {}  # user_id -> list of address_ids
            for i in range(0, len(user_ids), BATCH_SIZE):
                batch = []
                for uid in user_ids[i:i + BATCH_SIZE]:
                    # Her kullanıcı için 1-3 adres oluştur
                    num_addresses = random.randint(1, 3)
                    user_address_ids = []
                    
                    for addr_idx in range(num_addresses):
                        address_id = str(uuid.uuid4())
                        user_address_ids.append(address_id)
                        
                        is_default = addr_idx == 0  # İlk adres default
                        address_type = random.choice(ADDRESS_TYPES) if addr_idx > 0 else "HOME"
                        
                        batch.append(
                            (
                                address_id,
                                uid,
                                fake.street_address(),
                                fake.city(),
                                fake.country(),
                                fake.postcode(),
                                address_type,
                                is_default
                            )
                        )
                    
                    address_ids_map[uid] = user_address_ids

                cur.executemany(
                    """
                    INSERT INTO addresses 
                    (address_id, user_id, street, city, country, postal_code, address_type, is_default)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    batch
                )
                conn.commit()

            print(f"Addresses inserted")

            # 2. ACCOUNTS
            print("Generating accounts")
            for i in range(0, len(user_ids), BATCH_SIZE):
                batch = [
                    (
                        str(uuid.uuid4()),
                        uid,
                        round(random.uniform(0, 10_000), 2),
                        "ACTIVE",
                        fake.bothify(text='ACC-########'),
                        "USD",
                        fake.date_time_between(start_date="-2y"),
                        fake.date_time_between(start_date="-1y")
                    )
                    for uid in user_ids[i:i + BATCH_SIZE]
                ]

                cur.executemany(
                    """
                    INSERT INTO accounts 
                    (account_id, user_id, balance, status, account_number, currency, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    batch
                )
                conn.commit()

            # 2.5. CREDIT CARDS
            print("Generating credit cards")
            for i in range(0, len(user_ids), BATCH_SIZE):
                batch = []
                for uid in user_ids[i:i + BATCH_SIZE]:
                    # Her kullanıcı için 1-4 arası kart oluştur
                    num_cards = random.randint(1, 4)
                    
                    for card_idx in range(num_cards):
                        # Kart numarasını maskelenmiş formatta oluştur (son 4 hanesi görünür)
                        last_four = fake.numerify(text='####')
                        card_number = f"****-****-****-{last_four}"
                        
                        # Kart tipine göre format
                        card_type = random.choice(CARD_TYPES)
                        
                        # Kart sahibi adı
                        card_holder_name = fake.name()
                        
                        # Gelecekte bir tarih (1-5 yıl arası)
                        expiry_date = fake.date_between(start_date='today', end_date='+5y')
                        
                        # Bakiye (0-5000 arası)
                        balance = round(random.uniform(0, 5000), 2)
                        
                        # Durum
                        status = random.choices(CARD_STATUSES, weights=CARD_STATUS_WEIGHTS, k=1)[0]
                        
                        # İlk kart default
                        is_default = card_idx == 0
                        
                        # Tarihler
                        created_at = fake.date_time_between(start_date="-2y")
                        updated_at = fake.date_time_between(start_date="-1y") if random.random() < 0.5 else None
                        
                        batch.append(
                            (
                                str(uuid.uuid4()),
                                uid,
                                card_number,
                                card_holder_name,
                                expiry_date,
                                card_type,
                                balance,
                                status,
                                is_default,
                                created_at,
                                updated_at
                            )
                        )

                cur.executemany(
                    """
                    INSERT INTO credit_cards 
                    (card_id, user_id, card_number, card_holder_name, expiry_date, 
                     card_type, balance, status, is_default, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    batch
                )
                conn.commit()

            print(f"Credit cards inserted")

            # 3. PRODUCTS
            print("Generating products")
            for _ in range(0, PRODUCT_COUNT, BATCH_SIZE):
                batch = [
                    (
                        str(uuid.uuid4()),
                        fake.catch_phrase(),
                        round(random.uniform(10, 2000), 2),
                        random.randint(0, 1000),
                        fake.text(max_nb_chars=500),
                        random.choice(PRODUCT_CATEGORIES),
                        random.choice(BRANDS),
                        fake.image_url() if random.random() < 0.8 else None,
                        fake.bothify(text='SKU-####-####'),
                        fake.date_time_between(start_date="-1y"),
                        fake.date_time_between(start_date="-6m")
                    )
                    for _ in range(BATCH_SIZE)
                ]

                cur.executemany(
                    """
                    INSERT INTO products 
                    (product_id, name, price, stock_quantity, description, category, brand, 
                     image_url, sku, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    batch
                )

                product_ids.extend([r[0] for r in batch])
                conn.commit()

            print(f"Products inserted: {len(product_ids)}")

            # 3.5. HOBBIES
            print("Generating hobbies")
            hobby_ids_map = {}  # hobby_name -> hobby_id
            for category, hobbies_list in HOBBIES_BY_CATEGORY.items():
                batch = []
                for hobby_name in hobbies_list:
                    hobby_id = str(uuid.uuid4())
                    hobby_ids_map[hobby_name] = hobby_id
                    batch.append(
                        (
                            hobby_id,
                            hobby_name,
                            category
                        )
                    )
                
                cur.executemany(
                    """
                    INSERT INTO hobbies 
                    (hobby_id, name, category)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                    """,
                    batch
                )
                conn.commit()
            
            # Tüm hobby ID'lerini al (conflict durumunda mevcut ID'leri almak için)
            cur.execute("SELECT hobby_id, name FROM hobbies")
            all_hobby_ids = {row[1]: row[0] for row in cur.fetchall()}
            print(f"Hobbies inserted: {len(all_hobby_ids)}")

            # 3.6. USER_HOBBIES (Many-to-Many relationship)
            print("Generating user hobbies")
            for i in range(0, len(user_ids), BATCH_SIZE):
                batch = []
                for uid in user_ids[i:i + BATCH_SIZE]:
                    # Her kullanıcıya 1-5 arası rastgele hobby atan
                    num_hobbies = random.randint(1, 5)
                    selected_hobbies = random.sample(list(all_hobby_ids.items()), min(num_hobbies, len(all_hobby_ids)))
                    
                    for hobby_name, hobby_id in selected_hobbies:
                        batch.append(
                            (
                                uid,
                                hobby_id
                            )
                        )
                
                if batch:
                    cur.executemany(
                        """
                        INSERT INTO user_hobbies 
                        (user_id, hobby_id)
                        VALUES (%s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        batch
                    )
                    conn.commit()
            
            print(f"User hobbies inserted")

            # 4. ORDERS
            print("Generating orders")
            for _ in range(0, ORDER_COUNT, BATCH_SIZE):
                batch = []
                for _ in range(BATCH_SIZE):
                    user_id = random.choice(user_ids)
                    user_addresses = address_ids_map.get(user_id, [])
                    
                    # Shipping ve billing address seç
                    shipping_address_id = random.choice(user_addresses) if user_addresses else None
                    billing_address_id = random.choice(user_addresses) if user_addresses else None
                    
                    batch.append(
                        (
                            str(uuid.uuid4()),
                            user_id,
                            fake.date_time_between(start_date="-2y"),
                            0,
                            random.choices(ORDER_STATUSES, weights=ORDER_STATUS_WEIGHTS, k=1)[0],
                            shipping_address_id,
                            billing_address_id,
                            fake.text(max_nb_chars=200) if random.random() < 0.3 else None
                        )
                    )

                cur.executemany(
                    """
                    INSERT INTO orders 
                    (order_id, user_id, order_date, total_amount, status, 
                     shipping_address_id, billing_address_id, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    batch
                )
                conn.commit()

            # 5. FETCH ORDER IDS
            print("Fetching order ids")
            cur.execute("SELECT order_id FROM orders")
            order_ids = [r[0] for r in cur.fetchall()]

            print(f"Orders fetched: {len(order_ids)}")

            # 6. ORDER ITEMS
            print("Generating order items")
            for i in range(0, len(order_ids), BATCH_SIZE):
                batch = []

                for oid in order_ids[i:i + BATCH_SIZE]:
                    for _ in range(2):
                        unit_price = round(random.uniform(10, 500), 2)
                        quantity = random.randint(1, 3)
                        discount = round(random.uniform(0, 0.2), 2) if random.random() < 0.3 else 0
                        subtotal = round(unit_price * quantity * (1 - discount), 2)
                        batch.append(
                            (
                                str(uuid.uuid4()),
                                oid,
                                random.choice(product_ids),
                                quantity,
                                unit_price,
                                discount,
                                subtotal
                            )
                        )

                cur.executemany(
                    """
                    INSERT INTO order_items
                        (item_id, order_id, product_id, quantity, unit_price, discount, subtotal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    batch
                )
                conn.commit()

            # 7. PAYMENTS AND SHIPMENTS
            print("Generating payments and shipments")
            
            # Order'ların shipping_address_id'lerini al
            cur.execute("SELECT order_id, shipping_address_id FROM orders")
            order_address_map = {row[0]: row[1] for row in cur.fetchall()}
            
            for i in range(0, len(order_ids), BATCH_SIZE):
                orders_batch = order_ids[i:i + BATCH_SIZE]

                payments = [
                    (
                        str(uuid.uuid4()),
                        oid,
                        random.choice(PAYMENT_METHODS),
                        round(random.uniform(50, 5000), 2),
                        fake.date_time_between(start_date="-2y"),
                        random.choices(PAYMENT_STATUSES, weights=PAYMENT_STATUS_WEIGHTS, k=1)[0],
                        fake.bothify(text='TXN-########'),
                        fake.text(max_nb_chars=100) if random.random() < 0.1 else None
                    )
                    for oid in orders_batch
                ]

                shipments = [
                    (
                        str(uuid.uuid4()),
                        oid,
                        str(uuid.uuid4()),
                        random.choices(SHIPMENT_STATUSES, weights=SHIPMENT_STATUS_WEIGHTS, k=1)[0],
                        fake.date_time_between(start_date="-2y") if random.random() < 0.7 else None,
                        random.choice(SHIPMENT_CARRIERS),
                        fake.date_time_between(start_date="-1y") if random.random() < 0.5 else None,
                        fake.date_time_between(start_date="-6m") if random.random() < 0.3 else None,
                        order_address_map.get(oid),  # Order'dan shipping address'i al
                        fake.text(max_nb_chars=200) if random.random() < 0.2 else None
                    )
                    for oid in orders_batch
                ]

                cur.executemany(
                    """
                    INSERT INTO payments
                        (payment_id, order_id, payment_method, amount, payment_date, 
                         status, transaction_id, failure_reason)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    payments
                )

                cur.executemany(
                    """
                    INSERT INTO shipments
                        (shipment_id, order_id, tracking_number, status, shipped_at, 
                         carrier, estimated_delivery_date, actual_delivery_date, 
                         shipping_address_id, notes)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    shipments
                )

                conn.commit()

            print("Data generation finished successfully")


if __name__ == "__main__":
    generate_data()
