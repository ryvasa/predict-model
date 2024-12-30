import pandas as pd
import numpy as np
import random

# Parameter
num_lands = 100  # Jumlah lahan yang akan dibuat

# commodity = 'Corn'
# avg_yield_per_ha = 7352

commodity = 'Rice'
avg_yield_per_ha = 5790

yield_stddev = 500  # Deviasi standar untuk variasi hasil panen


def generate_land_data(num_lands, avg_yield_per_ha, yield_stddev):
    data = []
    cities = ["CityA", "CityB", "CityC", "CityD", "CityE"]  # Contoh kota

    for land_id in range(101, 101 + num_lands):
        city = random.choice(cities)
        area = random.randint(1, 10)  # Luas lahan (1-10 hektar)
        harvest_time = random.randint(100, 200)  # Waktu panen (hari)

        # Menghasilkan hasil panen dengan variasi normal, kemudian disesuaikan dengan luas lahan
        yield_per_ha = int(np.abs(np.random.normal(avg_yield_per_ha, yield_stddev)))
        total_yield = yield_per_ha * area

        data.append({
            "land_id": land_id,
            "commodity": commodity,
            "city": city,
            "area": area,
            "harvest_time": harvest_time,
            "harvest_yield": total_yield
        })
    return pd.DataFrame(data)


# Generate data
land_df = generate_land_data(num_lands, avg_yield_per_ha, yield_stddev)

# Hitung rata-rata hasil panen per hektar untuk verifikasi
total_yield = land_df["harvest_yield"].sum()
total_area = land_df["area"].sum()
actual_avg_yield = total_yield / total_area

print(f"Rata-rata hasil panen per hektar yang dihasilkan: {actual_avg_yield:.2f}")


# Simpan ke CSV
land_df.to_csv("lands_corn.csv", index=False)

print("Data berhasil disimpan ke lands_corn.csv")
