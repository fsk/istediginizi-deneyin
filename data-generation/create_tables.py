import psycopg
from psycopg.rows import tuple_row


def get_postgresql_connection():
    return psycopg.connect(
        "dbname=ecommerce user=fsk password=fsk host=localhost port=2345",
        autocommit=False
    )


def create_tables():
    with get_postgresql_connection() as conn:
        with conn.cursor(row_factory=tuple_row) as cur:
            print("Creating tables and foreign keys...")
            
            # 1. USERS table
            print("Creating users table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id UUID PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    phone_number VARCHAR(20),
                    bio TEXT,
                    profile_image_url VARCHAR(500),
                    date_of_birth DATE,
                    gender VARCHAR(20),
                    created_at TIMESTAMP
                )
            """)
            
            # 2. HOBBIES table
            print("Creating hobbies table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS hobbies (
                    hobby_id UUID PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    category VARCHAR(20) NOT NULL
                )
            """)
            
            # 3. ADDRESSES table
            print("Creating addresses table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS addresses (
                    address_id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    street VARCHAR(500) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    country VARCHAR(100) NOT NULL,
                    postal_code VARCHAR(20),
                    address_type VARCHAR(20) NOT NULL,
                    is_default BOOLEAN DEFAULT FALSE,
                    CONSTRAINT fk_address_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE
                )
            """)
            
            # 4. ACCOUNTS table
            print("Creating accounts table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id UUID PRIMARY KEY,
                    user_id UUID NOT NULL UNIQUE,
                    balance NUMERIC(12, 2) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    account_number VARCHAR(50) UNIQUE,
                    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP,
                    CONSTRAINT fk_account_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE
                )
            """)
            
            # 5. CREDIT_CARDS table
            print("Creating credit_cards table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS credit_cards (
                    card_id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    card_number VARCHAR(19) NOT NULL,
                    card_holder_name VARCHAR(100) NOT NULL,
                    expiry_date DATE NOT NULL,
                    card_type VARCHAR(20) NOT NULL,
                    balance NUMERIC(12, 2) NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    is_default BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP,
                    CONSTRAINT fk_credit_card_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE
                )
            """)
            
            # 6. PRODUCTS table
            print("Creating products table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id UUID PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price NUMERIC(10, 2) NOT NULL,
                    stock_quantity INTEGER NOT NULL,
                    description TEXT,
                    category VARCHAR(100),
                    brand VARCHAR(100),
                    image_url VARCHAR(500),
                    sku VARCHAR(50) UNIQUE,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP
                )
            """)
            
            # 7. ORDERS table
            print("Creating orders table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    order_date TIMESTAMP NOT NULL,
                    total_amount NUMERIC(12, 2),
                    status VARCHAR(20) NOT NULL,
                    shipping_address_id UUID,
                    billing_address_id UUID,
                    notes TEXT,
                    CONSTRAINT fk_order_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_order_shipping_address 
                        FOREIGN KEY (shipping_address_id) 
                        REFERENCES addresses(address_id) 
                        ON DELETE SET NULL,
                    CONSTRAINT fk_order_billing_address 
                        FOREIGN KEY (billing_address_id) 
                        REFERENCES addresses(address_id) 
                        ON DELETE SET NULL
                )
            """)
            
            # 8. ORDER_ITEMS table
            print("Creating order_items table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    item_id UUID PRIMARY KEY,
                    order_id UUID NOT NULL,
                    product_id UUID NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price NUMERIC(10, 2) NOT NULL,
                    discount NUMERIC(5, 2) DEFAULT 0,
                    subtotal NUMERIC(12, 2) NOT NULL,
                    CONSTRAINT fk_order_item_order 
                        FOREIGN KEY (order_id) 
                        REFERENCES orders(order_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_order_item_product 
                        FOREIGN KEY (product_id) 
                        REFERENCES products(product_id) 
                        ON DELETE CASCADE
                )
            """)
            
            # 9. PAYMENTS table
            print("Creating payments table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    payment_id UUID PRIMARY KEY,
                    order_id UUID NOT NULL UNIQUE,
                    payment_method VARCHAR(30) NOT NULL,
                    amount NUMERIC(12, 2) NOT NULL,
                    payment_date TIMESTAMP,
                    status VARCHAR(20) NOT NULL,
                    transaction_id VARCHAR(100) UNIQUE,
                    failure_reason VARCHAR(500),
                    CONSTRAINT fk_payment_order 
                        FOREIGN KEY (order_id) 
                        REFERENCES orders(order_id) 
                        ON DELETE CASCADE
                )
            """)
            
            # 10. SHIPMENTS table
            print("Creating shipments table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS shipments (
                    shipment_id UUID PRIMARY KEY,
                    order_id UUID NOT NULL UNIQUE,
                    tracking_number UUID NOT NULL,
                    status VARCHAR(30) NOT NULL,
                    shipped_at TIMESTAMP,
                    carrier VARCHAR(50),
                    estimated_delivery_date DATE,
                    actual_delivery_date DATE,
                    shipping_address_id UUID,
                    notes TEXT,
                    CONSTRAINT fk_shipment_order 
                        FOREIGN KEY (order_id) 
                        REFERENCES orders(order_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_shipment_address 
                        FOREIGN KEY (shipping_address_id) 
                        REFERENCES addresses(address_id) 
                        ON DELETE SET NULL
                )
            """)
            
            # 11. CARTS table
            print("Creating carts table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS carts (
                    cart_id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    total_amount NUMERIC(12, 2) DEFAULT 0,
                    item_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP,
                    expires_at TIMESTAMP,
                    converted_order_id UUID UNIQUE,
                    CONSTRAINT fk_cart_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_cart_converted_order 
                        FOREIGN KEY (converted_order_id) 
                        REFERENCES orders(order_id) 
                        ON DELETE SET NULL
                )
            """)
            
            # 12. CART_ITEMS table
            print("Creating cart_items table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cart_items (
                    cart_item_id UUID PRIMARY KEY,
                    cart_id UUID NOT NULL,
                    product_id UUID NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price NUMERIC(10, 2) NOT NULL,
                    subtotal NUMERIC(12, 2) NOT NULL,
                    added_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP,
                    CONSTRAINT fk_cart_item_cart 
                        FOREIGN KEY (cart_id) 
                        REFERENCES carts(cart_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_cart_item_product 
                        FOREIGN KEY (product_id) 
                        REFERENCES products(product_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT uk_cart_product 
                        UNIQUE (cart_id, product_id)
                )
            """)
            
            # 13. CATEGORIES table
            print("Creating categories table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    category_id UUID PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    parent_category_id UUID,
                    created_at TIMESTAMP NOT NULL,
                    CONSTRAINT fk_category_parent 
                        FOREIGN KEY (parent_category_id) 
                        REFERENCES categories(category_id) 
                        ON DELETE SET NULL
                )
            """)
            
            # 14. ORDER_HISTORY table
            print("Creating order_history table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS order_history (
                    history_id UUID PRIMARY KEY,
                    order_id UUID NOT NULL,
                    status VARCHAR(20) NOT NULL,
                    changed_at TIMESTAMP NOT NULL,
                    changed_by UUID,
                    notes TEXT,
                    CONSTRAINT fk_order_history_order 
                        FOREIGN KEY (order_id) 
                        REFERENCES orders(order_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_order_history_user 
                        FOREIGN KEY (changed_by) 
                        REFERENCES users(user_id) 
                        ON DELETE SET NULL
                )
            """)
            
            # 15. WISHLIST table
            print("Creating wishlist table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS wishlist (
                    wishlist_id UUID PRIMARY KEY,
                    user_id UUID NOT NULL,
                    product_id UUID NOT NULL,
                    added_at TIMESTAMP NOT NULL,
                    CONSTRAINT fk_wishlist_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_wishlist_product 
                        FOREIGN KEY (product_id) 
                        REFERENCES products(product_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT uk_wishlist_user_product 
                        UNIQUE (user_id, product_id)
                )
            """)
            
            # 16. PRODUCT_REVIEWS table
            print("Creating product_reviews table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS product_reviews (
                    review_id UUID PRIMARY KEY,
                    product_id UUID NOT NULL,
                    user_id UUID NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    comment TEXT,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP,
                    CONSTRAINT fk_review_product 
                        FOREIGN KEY (product_id) 
                        REFERENCES products(product_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_review_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT uk_review_product_user 
                        UNIQUE (product_id, user_id)
                )
            """)
            
            # 17. USER_HOBBIES join table (Many-to-Many)
            print("Creating user_hobbies join table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_hobbies (
                    user_id UUID NOT NULL,
                    hobby_id UUID NOT NULL,
                    PRIMARY KEY (user_id, hobby_id),
                    CONSTRAINT fk_user_hobby_user 
                        FOREIGN KEY (user_id) 
                        REFERENCES users(user_id) 
                        ON DELETE CASCADE,
                    CONSTRAINT fk_user_hobby_hobby 
                        FOREIGN KEY (hobby_id) 
                        REFERENCES hobbies(hobby_id) 
                        ON DELETE CASCADE
                )
            """)
            
            # # Indexes for better performance
            # print("Creating indexes...")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_addresses_user_id ON addresses(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_credit_cards_user_id ON credit_cards(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_shipping_address_id ON orders(shipping_address_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_billing_address_id ON orders(billing_address_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payments(order_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON shipments(order_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_shipments_shipping_address_id ON shipments(shipping_address_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_cart_user ON carts(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_cart_status ON carts(status)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_cart_item_cart ON cart_items(cart_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_cart_item_product ON cart_items(product_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_category_parent ON categories(parent_category_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_order_history_order ON order_history(order_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_order_history_changed_at ON order_history(changed_at)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_wishlist_user ON wishlist(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_wishlist_product ON wishlist(product_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_product_reviews_product ON product_reviews(product_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_product_reviews_user ON product_reviews(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_product_reviews_rating ON product_reviews(rating)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_user_hobbies_user_id ON user_hobbies(user_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_user_hobbies_hobby_id ON user_hobbies(hobby_id)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status)")
            # cur.execute("CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status)")
            
            conn.commit()
            print("All tables, foreign keys, and indexes created successfully!")


if __name__ == "__main__":
    create_tables()

