# TF-IDF Information Retrieval System

Sistem Temu Kembali Informasi menggunakan metode **TF-IDF (Term Frequency - Inverse Document Frequency)** dengan antarmuka GUI berbasis Python Tkinter.

## Fitur

1. **Preprocessing Teks**: Tokenisasi → Stopword Removal → Stemming (menggunakan Sastrawi)
2. **Perhitungan TF (Term Frequency)**: Menghitung frekuensi kemunculan kata di setiap dokumen
3. **Perhitungan DF & IDF**: Document Frequency dan Inverse Document Frequency
4. **Matrix TF-IDF**: Visualisasi lengkap bobot TF-IDF setiap kata di setiap dokumen
5. **Top Terms per Dokumen**: Menampilkan kata-kata paling penting di setiap dokumen
6. **Query & Ranking**: Pencarian query yang menampilkan skor TF-IDF dan meranking dokumen berdasarkan relevansi

## Struktur Project

```
ir-tfidf-retrieval/
├── data/                  # 20 dokumen teks (.txt)
│   ├── D1.txt - D20.txt
├── modules/
│   ├── __init__.py
│   ├── preprocessing.py   # Tokenisasi, Stopword Removal, Stemming
│   ├── indexing.py         # Perhitungan TF, DF, IDF, TF-IDF Matrix
│   ├── retrieval.py        # Query TF-IDF & Ranking dokumen
│   └── interface.py        # GUI / Tampilan Tkinter
├── main.py                 # Entry point aplikasi
├── requirements.txt
└── README.md
```

## Rumus TF-IDF

- **TF(t,d)** = Jumlah kemunculan term t dalam dokumen d / Total term dalam dokumen d
- **DF(t)** = Jumlah dokumen yang mengandung term t
- **IDF(t)** = log₁₀(N / DF(t)), dimana N = total dokumen
- **TF-IDF(t,d)** = TF(t,d) × IDF(t)

## Cara Menjalankan

```bash
pip install -r requirements.txt
python main.py
```

## Requirements

- Python 3.x
- numpy
- Sastrawi (library NLP Bahasa Indonesia)

## Pembuat

- **Nama**: Gede Yudhi Adinata
- **NIM**: 2305551142
