# Data Generation Scripts

Bu klasör PostgreSQL veritabanı için test verileri oluşturan scriptleri içerir.

## Kurulum

1. Virtual environment oluşturun (ilk kez):
```bash
python3 -m venv venv
```

2. Virtual environment'ı aktifleştirin:
```bash
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

**ÖNEMLİ:** Scriptleri çalıştırmadan önce virtual environment'ı aktifleştirmeyi unutmayın!

```bash
# Virtual environment'ı aktifleştir
source venv/bin/activate

# Veritabanını temizle
python clear_database.py

# Tabloları oluştur
python create_tables.py

# Test verilerini oluştur (bu işlem uzun sürebilir)
python generate_data.py
```

## Notlar

- Virtual environment aktifken terminal prompt'unda `(venv)` görünür
- Her yeni terminal oturumunda `source venv/bin/activate` komutunu çalıştırmanız gerekir
- Scriptler PostgreSQL veritabanına bağlanır (connection bilgileri script içinde tanımlı)


