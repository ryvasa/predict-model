import pandas as pd

try:
    # Membaca data dari CSV
    df = pd.read_csv("data/price.csv")

    # Menghapus baris dengan nilai 'price' yang kosong atau bukan angka
    df = df.dropna(subset=['price'])  # Hapus baris dengan nilai price yang hilang (NaN)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')  # Ubah ke numeric, nilai non-numeric jadi NaN
    df = df.dropna(subset=['price']) #hapus lagi yg NaN

    # Hitung rata-rata
    average_price = df['price'].mean()
    count = len(df)

    print(f"Rata-rata harga: {average_price}")
    print(f"Jumlah data yang digunakan: {count}")

except FileNotFoundError:
    print("File 'data/data.csv' tidak ditemukan.")
except pd.errors.EmptyDataError:
    print("File 'data/data.csv' kosong.")
except pd.errors.ParserError:
    print("Terjadi kesalahan saat memproses file 'data/data.csv'. Periksa format file.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
