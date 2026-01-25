import psycopg2
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib

# --------------------------------------------------
# Database connection (Docker-safe)
# --------------------------------------------------
conn = psycopg2.connect(
    host="postgres",          # IMPORTANT: Docker service name
    port=5432,
    database="weatherdb",
    user="user",
    password="password"
)

# --------------------------------------------------
# Ensure table exists (PREVENTS CRASH)
# --------------------------------------------------
create_table_query = """
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT,
    temperature FLOAT,
    condition TEXT,
    timestamp TIMESTAMP
);
"""

cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()
cursor.close()

# --------------------------------------------------
# Read data
# --------------------------------------------------
query = """
SELECT city, temperature, condition, timestamp
FROM weather_data
ORDER BY timestamp;
"""

df = pd.read_sql(query, conn)
conn.close()

# --------------------------------------------------
# Guard: not enough data
# --------------------------------------------------
if len(df) < 5:
    print("Not enough data to train model yet.")
    exit(0)

# --------------------------------------------------
# Feature engineering
# --------------------------------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["day"] = df["timestamp"].dt.day

df = pd.get_dummies(df, columns=["city", "condition"])

X = df.drop(columns=["temperature", "timestamp"])
y = df["temperature"]

# --------------------------------------------------
# Train / Test split (time-aware)
# --------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# --------------------------------------------------
# Train model
# --------------------------------------------------
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------------------
# Evaluate
# --------------------------------------------------
preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print("MAE:", mae)

# --------------------------------------------------
# Save model
# --------------------------------------------------
joblib.dump(model, "weather_model.pkl")
print("Model saved as weather_model.pkl")
