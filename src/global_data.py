import numpy as np
import pandas as pd

# Rice
# commodity = 'Rice'
# avg_supply = 23327855.18
# avg_price = 6431.11

# Corn
commodity = 'Corn'
avg_supply = 1634270.58
avg_price = 5005.83

days = 365

# Tambahkan fluktuasi acak ke supply dan price.  Gunakan abs() untuk memastikan positif
supply = np.abs(np.random.normal(avg_supply, avg_supply * 0.05, days))
price = np.abs(np.random.normal(avg_price, avg_price * 0.02, days))

# Asumsi sederhana: demand berbanding terbalik dengan harga.  Gunakan abs() untuk memastikan positif.
demand = np.abs(avg_supply - (price - avg_price) * 100000)

# Sales = min(supply, demand)
sales = np.minimum(supply, demand)

# Buat DataFrame
data = pd.DataFrame({'day': range(1, days + 1),'commodity' :commodity, 'price': price, 'demand': demand, 'supply': supply, 'sale': sales})

# Pastikan angka positif (tidak perlu clip lagi karena sudah di-abs)

# Simpan ke CSV
data.to_csv('global_data.csv', index=False)

print(data.head())
