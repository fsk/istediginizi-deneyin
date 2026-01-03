import psycopg
from psycopg.rows import tuple_row
from faker import Faker
import random
import uuid
from datetime import timedelta

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

# Categories için hiyerarşik yapı
CATEGORIES_DATA = [
    {"name": "Electronics", "description": "Electronic devices and accessories"},
    {"name": "Computers", "description": "Laptops, desktops, and computer accessories", "parent": "Electronics"},
    {"name": "Smartphones", "description": "Mobile phones and accessories", "parent": "Electronics"},
    {"name": "TV & Audio", "description": "Televisions and audio equipment", "parent": "Electronics"},
    {"name": "Clothing", "description": "Apparel and fashion items"},
    {"name": "Men's Clothing", "description": "Clothing for men", "parent": "Clothing"},
    {"name": "Women's Clothing", "description": "Clothing for women", "parent": "Clothing"},
    {"name": "Kids' Clothing", "description": "Clothing for children", "parent": "Clothing"},
    {"name": "Books", "description": "Books and publications"},
    {"name": "Fiction", "description": "Fictional books", "parent": "Books"},
    {"name": "Non-Fiction", "description": "Non-fiction books", "parent": "Books"},
    {"name": "Home & Garden", "description": "Home and garden products"},
    {"name": "Furniture", "description": "Home furniture", "parent": "Home & Garden"},
    {"name": "Kitchen & Dining", "description": "Kitchen and dining products", "parent": "Home & Garden"},
    {"name": "Sports & Outdoors", "description": "Sports and outdoor equipment"},
    {"name": "Fitness", "description": "Fitness equipment and gear", "parent": "Sports & Outdoors"},
    {"name": "Outdoor Recreation", "description": "Outdoor recreation products", "parent": "Sports & Outdoors"},
]

CART_STATUSES = ["ACTIVE", "CONVERTED", "ABANDONED", "EXPIRED"]
CART_STATUS_WEIGHTS = [0.60, 0.25, 0.10, 0.05]

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
                batch = []
                for uid in user_ids[i:i + BATCH_SIZE]:
                    # Unique account number oluştur (UUID'nin ilk 8 karakterini kullan)
                    account_uuid = str(uuid.uuid4()).replace('-', '')
                    account_number = f"ACC-{account_uuid[:12].upper()}"
                    
                    batch.append((
                        str(uuid.uuid4()),
                        uid,
                        round(random.uniform(0, 10_000), 2),
                        "ACTIVE",
                        account_number,
                        "USD",
                        fake.date_time_between(start_date="-2y"),
                        fake.date_time_between(start_date="-1y")
                    ))

                cur.executemany(
                    """
                    INSERT INTO accounts 
                    (account_id, user_id, balance, status, account_number, currency, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (account_number) DO NOTHING
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
                batch = []
                for _ in range(BATCH_SIZE):
                    # Unique SKU oluştur
                    sku_uuid = str(uuid.uuid4()).replace('-', '')
                    sku = f"SKU-{sku_uuid[:8].upper()}-{sku_uuid[8:12].upper()}"
                    
                    batch.append((
                        str(uuid.uuid4()),
                        fake.catch_phrase(),
                        round(random.uniform(10, 2000), 2),
                        random.randint(0, 1000),
                        fake.text(max_nb_chars=500),
                        random.choice(PRODUCT_CATEGORIES),
                        random.choice(BRANDS),
                        fake.image_url() if random.random() < 0.8 else None,
                        sku,
                        fake.date_time_between(start_date="-1y"),
                        fake.date_time_between(start_date="-6m")
                    ))

                cur.executemany(
                    """
                    INSERT INTO products 
                    (product_id, name, price, stock_quantity, description, category, brand, 
                     image_url, sku, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (sku) DO NOTHING
                    """,
                    batch
                )

                product_ids.extend([r[0] for r in batch])
                conn.commit()

            print(f"Products inserted: {len(product_ids)}")

            # 3.4. CATEGORIES
            print("Generating categories")
            category_ids_map = {}  # category_name -> category_id
            parent_category_ids = {}  # For parent categories
            
            # Önce parent kategorileri oluştur
            for cat_data in CATEGORIES_DATA:
                if "parent" not in cat_data:
                    category_id = str(uuid.uuid4())
                    category_ids_map[cat_data["name"]] = category_id
                    parent_category_ids[cat_data["name"]] = category_id
                    
                    cur.execute(
                        """
                        INSERT INTO categories 
                        (category_id, name, description, created_at)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                        """,
                        (
                            category_id,
                            cat_data["name"],
                            cat_data.get("description"),
                            fake.date_time_between(start_date="-2y")
                        )
                    )
                    conn.commit()
            
            # Sonra child kategorileri oluştur
            for cat_data in CATEGORIES_DATA:
                if "parent" in cat_data:
                    parent_name = cat_data["parent"]
                    if parent_name in parent_category_ids:
                        category_id = str(uuid.uuid4())
                        category_ids_map[cat_data["name"]] = category_id
                        
                        cur.execute(
                            """
                            INSERT INTO categories 
                            (category_id, name, description, parent_category_id, created_at)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING
                            """,
                            (
                                category_id,
                                cat_data["name"],
                                cat_data.get("description"),
                                parent_category_ids[parent_name],
                                fake.date_time_between(start_date="-1y")
                            )
                        )
                        conn.commit()
            
            # Tüm category ID'leri al
            cur.execute("SELECT category_id, name FROM categories")
            all_category_ids = {row[1]: row[0] for row in cur.fetchall()}
            print(f"Categories inserted: {len(all_category_ids)}")

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

                payments = []
                for oid in orders_batch:
                    # Unique transaction ID oluştur
                    txn_uuid = str(uuid.uuid4()).replace('-', '')
                    transaction_id = f"TXN-{txn_uuid[:12].upper()}"
                    
                    payments.append((
                        str(uuid.uuid4()),
                        oid,
                        random.choice(PAYMENT_METHODS),
                        round(random.uniform(50, 5000), 2),
                        fake.date_time_between(start_date="-2y"),
                        random.choices(PAYMENT_STATUSES, weights=PAYMENT_STATUS_WEIGHTS, k=1)[0],
                        transaction_id,
                        fake.text(max_nb_chars=100) if random.random() < 0.1 else None
                    ))

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
                    ON CONFLICT (transaction_id) DO NOTHING
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

            # 8. ORDER HISTORY
            print("Generating order history")
            cur.execute("SELECT order_id, status, order_date FROM orders ORDER BY order_date")
            orders_data = cur.fetchall()
            
            # Status sıralaması
            status_order = ["PENDING", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED"]
            
            for i in range(0, len(orders_data), BATCH_SIZE):
                batch = []
                for order_id, current_status, order_date in orders_data[i:i + BATCH_SIZE]:
                    status_sequence = []
                    
                    if current_status in status_order:
                        current_idx = status_order.index(current_status)
                        status_sequence = status_order[:current_idx + 1]
                    elif current_status == "CANCELLED":
                        status_sequence = ["PENDING", "CONFIRMED", "CANCELLED"]
                    elif current_status == "REFUNDED":
                        status_sequence = ["PENDING", "CONFIRMED", "PROCESSING", "SHIPPED", "DELIVERED", "REFUNDED"]
                    
                    base_date = order_date
                    for idx, status in enumerate(status_sequence):
                        changed_at = base_date + timedelta(days=idx, hours=random.randint(1, 24))
                        
                        changed_by = random.choice(user_ids) if random.random() < 0.7 else None
                        
                        notes = None
                        if status in ["CANCELLED", "REFUNDED"] and random.random() < 0.3:
                            notes = fake.text(max_nb_chars=100)
                        
                        batch.append((
                            str(uuid.uuid4()),
                            order_id,
                            status,
                            changed_at,
                            changed_by,
                            notes
                        ))
                
                if batch:
                    cur.executemany(
                        """
                        INSERT INTO order_history
                        (history_id, order_id, status, changed_at, changed_by, notes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        batch
                    )
                    conn.commit()
            
            print("Order history inserted")

            # 9. WISHLIST
            print("Generating wishlist")
            wishlist_users = random.sample(user_ids, k=int(len(user_ids) * random.uniform(0.5, 0.8)))
            
            for i in range(0, len(wishlist_users), BATCH_SIZE):
                batch = []
                for user_id in wishlist_users[i:i + BATCH_SIZE]:
                    num_wishlist_items = random.randint(1, 20)
                    selected_products = random.sample(product_ids, min(num_wishlist_items, len(product_ids)))
                    
                    for product_id in selected_products:
                        batch.append((
                            str(uuid.uuid4()),
                            user_id,
                            product_id,
                            fake.date_time_between(start_date="-1y")
                        ))
                
                if batch:
                    cur.executemany(
                        """
                        INSERT INTO wishlist
                        (wishlist_id, user_id, product_id, added_at)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (user_id, product_id) DO NOTHING
                        """,
                        batch
                    )
                    conn.commit()
            
            print("Wishlist inserted")

            # 10. PRODUCT REVIEWS (Optimized for speed - 15 min target)
            print("Generating product reviews")
            # Satın alınmış ürünlerin %20-35'sine yorum yazılsın (daha agresif azaltma)
            cur.execute("SELECT DISTINCT product_id FROM order_items")
            reviewed_products = [row[0] for row in cur.fetchall()]
            reviewed_products = random.sample(reviewed_products, k=int(len(reviewed_products) * random.uniform(0.2, 0.35)))
            
            # Basit comment pool (fake.text çok yavaş)
            SIMPLE_COMMENTS = [
                "Great product!", "Good value for money", "Highly recommend", 
                "Not bad", "Could be better", "Excellent quality", "Fast shipping",
                "As described", "Very satisfied", "Good product", None, None, None
            ]
            
            # Tüm review'ları önce topla, sonra batch batch insert et
            all_reviews = []
            processed = 0
            for product_id in reviewed_products:
                # Her ürüne 1-15 arası yorum (25'ten 15'e düşürüldü)
                num_reviews = random.randint(1, 15)
                reviewers = random.sample(user_ids, min(num_reviews, len(user_ids)))
                
                for user_id in reviewers:
                    rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.15, 0.30, 0.40], k=1)[0]
                    comment = random.choice(SIMPLE_COMMENTS)  # fake.text yerine hazır comment
                    created_at = fake.date_time_between(start_date="-6m")
                    updated_at = None  # updated_at'ı kaldırdık (daha hızlı)
                    
                    all_reviews.append((
                        str(uuid.uuid4()),
                        product_id,
                        user_id,
                        rating,
                        comment,
                        created_at,
                        updated_at
                    ))
                
                processed += 1
                if processed % 5000 == 0:
                    print(f"  {processed}/{len(reviewed_products)} product işlendi, {len(all_reviews)} review hazır...", end='\r')
            
            # Şimdi batch batch insert et
            print(f"\n  Toplam {len(all_reviews)} review oluşturuldu, ekleniyor...")
            for i in range(0, len(all_reviews), BATCH_SIZE):
                batch = all_reviews[i:i + BATCH_SIZE]
                cur.executemany(
                    """
                    INSERT INTO product_reviews
                    (review_id, product_id, user_id, rating, comment, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (product_id, user_id) DO NOTHING
                    """,
                    batch
                )
                conn.commit()
                if (i + BATCH_SIZE) % (BATCH_SIZE * 5) == 0:
                    print(f"  {min(i + BATCH_SIZE, len(all_reviews))}/{len(all_reviews)} review eklendi...", end='\r')
            
            print(f"\nProduct reviews inserted: {len(all_reviews)}")

            # 11. CARTS
            print("Generating carts")
            num_cart_users = int(len(user_ids) * random.uniform(0.5, 0.8))
            cart_users = random.sample(user_ids, k=num_cart_users)
            
            cart_ids_list = []
            for i in range(0, len(cart_users), BATCH_SIZE):
                batch = []
                for user_id in cart_users[i:i + BATCH_SIZE]:
                    cart_id = str(uuid.uuid4())
                    cart_ids_list.append(cart_id)
                    
                    status = random.choices(CART_STATUSES, weights=CART_STATUS_WEIGHTS, k=1)[0]
                    created_at = fake.date_time_between(start_date="-1y")
                    expires_at = created_at + timedelta(days=30) if status == "ACTIVE" else None
                    updated_at = fake.date_time_between(start_date=created_at) if random.random() < 0.5 else None
                    
                    converted_order_id = None
                    total_amount = 0.0
                    item_count = 0
                    
                    batch.append((
                        cart_id,
                        user_id,
                        status,
                        total_amount,
                        item_count,
                        created_at,
                        updated_at,
                        expires_at,
                        converted_order_id
                    ))
                
                if batch:
                    cur.executemany(
                        """
                        INSERT INTO carts
                        (cart_id, user_id, status, total_amount, item_count, created_at, updated_at, expires_at, converted_order_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        batch
                    )
                    conn.commit()
            
            print(f"Carts inserted: {len(cart_ids_list)}")

            # 12. CART_ITEMS
            print("Generating cart items")
            cur.execute("SELECT cart_id, status FROM carts WHERE status IN ('ACTIVE', 'CONVERTED')")
            active_carts = cur.fetchall()
            
            total_cart_items = 0
            processed = 0
            for cart_id, cart_status in active_carts:
                num_items = random.randint(1, 15)
                selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
                
                cart_total = 0.0
                batch = []
                for product_id in selected_products:
                    cur.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
                    product_price_result = cur.fetchone()
                    if product_price_result:
                        product_price = product_price_result[0]
                        
                        quantity = random.randint(1, 5)
                        unit_price = float(product_price)
                        subtotal = round(unit_price * quantity, 2)
                        cart_total += subtotal
                        
                        added_at = fake.date_time_between(start_date="-6m")
                        updated_at = fake.date_time_between(start_date=added_at) if random.random() < 0.2 else None
                        
                        batch.append((
                            str(uuid.uuid4()),
                            cart_id,
                            product_id,
                            quantity,
                            unit_price,
                            subtotal,
                            added_at,
                            updated_at
                        ))
                
                if batch:
                    cur.executemany(
                        """
                        INSERT INTO cart_items
                        (cart_item_id, cart_id, product_id, quantity, unit_price, subtotal, added_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (cart_id, product_id) DO NOTHING
                        """,
                        batch
                    )
                    total_cart_items += len(batch)
                    
                    cur.execute(
                        """
                        UPDATE carts 
                        SET total_amount = %s, item_count = %s 
                        WHERE cart_id = %s
                        """,
                        (cart_total, len(selected_products), cart_id)
                    )
                    conn.commit()
                
                processed += 1
                if processed % 1000 == 0:
                    print(f"  {processed}/{len(active_carts)} cart işlendi, {total_cart_items} item eklendi...", end='\r')
            
            print(f"\nCart items inserted: {total_cart_items}")

            print("Updating converted carts with order_ids")
            cur.execute("""
                UPDATE carts c
                SET converted_order_id = o.order_id
                FROM (
                    SELECT DISTINCT ON (user_id) 
                        user_id, 
                        order_id
                    FROM orders
                    ORDER BY user_id, order_date DESC
                ) o
                WHERE c.user_id = o.user_id 
                    AND c.status = 'CONVERTED' 
                    AND c.converted_order_id IS NULL
            """)
            updated_count = cur.rowcount
            conn.commit()
            print(f"Cart conversions updated: {updated_count}")

            print("Data generation finished successfully")


if __name__ == "__main__":
    generate_data()
