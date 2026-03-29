# TF-IDF Information Retrieval System 🐱

Sistem Temu Kembali Informasi cerdas menggunakan metode **TF-IDF (Term Frequency - Inverse Document Frequency)** untuk melakukan perangkingan dokumen berdasarkan relevansi query.

## Preview Aplikasi
![Sistem Temu Kembali Informasi TF-IDF](screenshoot/screenshot.png)
*(Pastikan Bapak simpan gambar screenshot-nya di folder: screenshoot/screenshot.png)*

## Fitur Utama
- **Preprocessing Modern**: Case folding, penghapusan tanda baca, Stopword removal, dan Stemming menggunakan library Sastrawi.
- **Natural Sorting**: Dokumen terurut secara cerdas (D1, D2, ..., D10, D20).
- **Multi-Tab Visualization**:
  - **TF-IDF Matrix**: Bobot akhir setiap kata.
  - **Term Frequency**: Tabel frekuensi mentah dan ternormalisasi.
  - **DF & IDF**: Menampilkan tingkat keunikan setiap kata.
  - **Top Terms**: Ringkasan kata paling penting di setiap dokumen.
- **Advanced Query Search**: Pencarian yang memberikan skor relevansi dan detail perhitungan matematika untuk setiap kata kunci.

## Dataset (Corpus)
Menggunakan **20 Dokumen (D1-D20)** yang berisi informasi mendalam tentang berbagai ras kucing dunia seperti Persia, Maine Coon, Bengal, hingga Munchkin.

## Teknologi
- **Bahasa**: Python 3.x
- **GUI**: Tkinter & TTK (Custom Sleek Design)
- **Math**: Numpy
- **NLP**: Sastrawi (Indonesian Stemmer)
