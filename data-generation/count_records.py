import psycopg
from psycopg.rows import tuple_row


def get_postgresql_connection():
    return psycopg.connect(
        "dbname=ecommerce user=fsk password=fsk host=localhost port=2345",
        autocommit=False
    )


def count_records():
    with get_postgresql_connection() as conn:
        with conn.cursor(row_factory=tuple_row) as cur:
            print("=" * 60)
            print("TABLO KAYIT SAYILARI")
            print("=" * 60)
            
            # Tüm tabloları liste
            tables = [
                "users",
                "hobbies",
                "addresses",
                "accounts",
                "credit_cards",
                "products",
                "categories",
                "orders",
                "order_items",
                "order_history",
                "payments",
                "shipments",
                "carts",
                "cart_items",
                "wishlist",
                "product_reviews",
                "user_hobbies"
            ]
            
            total_count = 0
            results = []
            
            for table in tables:
                try:
                    cur.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cur.fetchone()[0]
                    results.append((table, count))
                    total_count += count
                except Exception as e:
                    results.append((table, f"ERROR: {str(e)}"))
            
            # Sonuçları yazdır
            print(f"\n{'Tablolar':<30} {'Kayıt Sayısı':>20}")
            print("-" * 60)
            
            for table, count in results:
                if isinstance(count, int):
                    print(f"{table:<30} {count:>20,}")
                else:
                    print(f"{table:<30} {count:>20}")
            
            print("-" * 60)
            print(f"{'TOPLAM':<30} {total_count:>20,}")
            print("=" * 60)


if __name__ == "__main__":
    count_records()

