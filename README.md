# Proyek Analisis Data

## 📌 Deskripsi Proyek

Proyek ini berfokus pada analisis data menggunakan berbagai dataset terkait transaksi, pelanggan, lokasi, dan produk. Data dianalisis untuk mendapatkan wawasan yang berguna dalam pengambilan keputusan bisnis.

## 📁 Struktur Folder

```
projek-data-analys/
├── dashboard/
│   ├── __pycache__/
│   ├── all_df.csv
│   ├── dashboard.py
├── data/
│   ├── all_df.csv
│   ├── customers_dataset.csv
│   ├── geolocation.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name.csv
│   ├── products_dataset.csv
│   ├── sales_df.csv
│   ├── sellers_dataset.csv
├── logo1.png
├── README.md
├── requirements.txt
└── url.txt
```

## 🚀 Cara Menjalankan

1. **Pastikan lingkungan Python terinstal**
   - Gunakan Python versi 3.8 atau lebih baru
2. **Instal dependensi**

   ```sh
   pip install streamlit
   pip install -r requirements.txt
   ```

3. **Jalankan program**
   ```sh
   streamlit run dashboard/dashboard.py
   ```

## 📊 Dataset

| File              | Deskripsi                       |
| ----------------- | ------------------------------- |
| `all_df.csv`      | Data gabungan dari semua sumber |
| `geolocation.csv` | Data geolokasi                  |

## ⚠️ Catatan Penting

- Pastikan file `all_df.csv` dan dataset lainnya tersedia dalam folder `data/` sebelum menjalankan analisis.
- Jika ada error **`FileNotFoundError`**, periksa kembali jalur file atau pastikan Anda menjalankan skrip dari direktori yang benar.

## 📧 Kontak

Jika ada pertanyaan atau ingin berkontribusi, hubungi: **nabilaalawiyah.25@gmail.com**

---

© 2025 - Proyek Analisis Data - Nabila Alawiyah
