import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Load data from CSV files
lands_df = pd.read_csv("data/lands.csv")
global_df = pd.read_csv("data/global_data.csv")

# 3. Gabungkan data lahan dan global berdasarkan waktu panen
merged_data = []
for _, land in lands_df.iterrows():
    for day in global_df["day"]:  #Iterasi melalui semua hari yang ada dalam global_df
        row = {
            "land_id": land["land_id"],
            "commodity": land["commodity"],
            "city": land["city"],
            "area": land["area"],
            "harvest_time": land["harvest_time"],
            "harvest_yield": land["harvest_yield"] if day >= land["harvest_time"] else 0,
            "day": day,
        }
        # Tambahkan data global
        global_row = global_df[global_df["day"] == day].iloc[0]
        row.update(global_row)
        merged_data.append(row)

final_df = pd.DataFrame(merged_data)


# 4. Latih model XGBoost
# Fitur dan target
features = ["area", "harvest_time", "harvest_yield", "demand", "supply", "sale", "day"]
target = "price"

X = final_df[features]
y = final_df[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model XGBoost
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, max_depth=6, eta=0.3)
model.fit(X_train, y_train)

# Prediksi dan evaluasi
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Squared Error: {mse}")

# 5. Visualisasi Prediksi Harga
results = pd.DataFrame({"Actual": y_test.values, "Predicted": y_pred})
print(results.head())

plt.plot(y_test, y_pred, alpha=0.7)
plt.xlabel("Harga Aktual")
plt.ylabel("Harga Prediksi")
plt.title("Perbandingan Harga Aktual vs Prediksi")
plt.show()

# Simpan model setelah pelatihan
joblib.dump(model, 'src/xgboost_model.pkl')
