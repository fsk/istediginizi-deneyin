#!/usr/bin/env python3
"""
Product tablosuna version kolonu eklemek için migration scripti.
Bu script, optimistic locking için gerekli olan version kolonunu ekler.
"""

import psycopg
import sys

# Veritabanı bağlantı string'i (psycopg3 formatı)
CONN_STRING = "dbname=ecommerce user=fsk password=fsk host=localhost port=2345"

def add_version_column():
    """Product tablosuna version kolonu ekler."""
    try:
        with psycopg.connect(CONN_STRING, autocommit=False) as conn:
            with conn.cursor() as cur:
                # Önce version kolonunun var olup olmadığını kontrol et
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'products' AND column_name = 'version'
                """)
                
                if cur.fetchone():
                    print("⚠️  'version' kolonu zaten mevcut!")
                    # Null değerleri kontrol et ve güncelle
                    cur.execute("""
                        SELECT COUNT(*) 
                        FROM products 
                        WHERE version IS NULL
                    """)
                    null_count = cur.fetchone()[0]
                    if null_count > 0:
                        print(f"📝 {null_count} kayıtta version NULL, güncelleniyor...")
                        cur.execute("""
                            UPDATE products 
                            SET version = 0 
                            WHERE version IS NULL
                        """)
                        conn.commit()
                        print(f"✅ {null_count} kayıt güncellendi!")
                    else:
                        print("✅ Tüm kayıtlarda version değeri mevcut.")
                    return
                
                # Version kolonunu ekle (varsayılan değer 0)
                print("📝 Product tablosuna 'version' kolonu ekleniyor...")
                cur.execute("""
                    ALTER TABLE products 
                    ADD COLUMN version BIGINT DEFAULT 0 NOT NULL
                """)
                
                # Mevcut tüm kayıtlara version = 0 atanmış olacak (DEFAULT 0)
                # Ama güvenlik için tüm kayıtları güncelleyelim
                cur.execute("""
                    UPDATE products 
                    SET version = 0 
                    WHERE version IS NULL
                """)
                
                conn.commit()
                print("✅ 'version' kolonu başarıyla eklendi!")
                print("   Tüm mevcut kayıtlara version = 0 atandı.")
                
    except psycopg.Error as e:
        print(f"❌ Veritabanı hatası: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("PRODUCT TABLOSUNA VERSION KOLONU EKLEME")
    print("=" * 60)
    add_version_column()
    print("=" * 60)
