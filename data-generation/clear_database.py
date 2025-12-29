import psycopg
from psycopg.rows import tuple_row


def get_postgresql_connection():
    return psycopg.connect(
        "dbname=ecommerce user=fsk password=fsk host=localhost port=2345",
        autocommit=False
    )


def clear_database():
    with get_postgresql_connection() as conn:
        with conn.cursor(row_factory=tuple_row) as cur:
            print("Clearing database...")
            
            # Foreign key constraint'leri devre dışı bırak
            cur.execute("SET session_replication_role = 'replica';")
            
            # Tüm tabloları bul ve sil
            cur.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            
            tables = [row[0] for row in cur.fetchall()]
            print(f"Found {len(tables)} tables: {tables}")
            
            if tables:
                # Tüm tabloları drop et
                for table in tables:
                    try:
                        cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
                        print(f"Dropped table: {table}")
                    except Exception as e:
                        print(f"Error dropping table {table}: {e}")
                
                conn.commit()
                print("All tables dropped successfully!")
            else:
                print("No tables found in database.")
            
        
            print("Database cleared successfully!")


if __name__ == "__main__":
    confirm = input("Are you sure you want to delete ALL tables? (yes/no): ")
    if confirm.lower() == "yes":
        clear_database()
    else:
        print("Operation cancelled.")

