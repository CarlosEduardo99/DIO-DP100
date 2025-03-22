import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 1. Load the data
data = pd.read_csv("vendas_sorveteria.csv")

# 2. Basic data information
print("Basic information:")
print(data.info())
print("\nDescriptive statistics:")
print(data.describe())

# Check for missing values
data.dropna(inplace=True)

# Convert temperature to integer
data["temp"] = data["temp"].astype(int)

# Selecting relevant columns
df = data[["temp", "holiday", "event", "strawberry", "chocolate", "lemon", "grape", "mango", "total"]]

# Encoding categorical variables
df = pd.get_dummies(df, columns=["holiday", "event"], drop_first=True)

# Splitting features and target
X = df.drop(columns=["total", "strawberry", "chocolate", "lemon", "grape", "mango"])
y_total = df["total"].values

# Splitting the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y_total, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the model for total sales prediction
lr_total = LinearRegression()
lr_total.fit(X_train_scaled, y_train)

# Predictions for total sales
y_train_pred = lr_total.predict(X_train_scaled)
y_test_pred = lr_total.predict(X_test_scaled)

# Evaluation
mse_train = mean_squared_error(y_train, y_train_pred)
mse_test = mean_squared_error(y_test, y_test_pred)
r2_train = r2_score(y_train, y_train_pred)
r2_test = r2_score(y_test, y_test_pred)

print(f"Train MSE: {mse_train:.2f}")
print(f"Test MSE: {mse_test:.2f}")
print(f"Train R²: {r2_train:.2f}")
print(f"Test R²: {r2_test:.2f}")

# Train separate models for each flavor
flavors = ["strawberry", "chocolate", "lemon", "grape", "mango"]
flavor_models = {}

for flavor in flavors:
    y_flavor = df[flavor].values
    X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X, y_flavor, test_size=0.2, random_state=42)
    lr_flavor = LinearRegression()
    lr_flavor.fit(scaler.transform(X_train_f), y_train_f)
    flavor_models[flavor] = lr_flavor

# Function to predict total sales and individual flavors
def predict_sales(temp, holiday=False, event=False):
    temp = int(temp)  # Ensure temperature is an integer
    input_data = pd.DataFrame({"temp": [temp], "holiday_True": [int(holiday)], "event_True": [int(event)]})
    input_scaled = scaler.transform(input_data)
    total_sales = round(lr_total.predict(input_scaled)[0])
    
    flavor_predictions = {}
    for flavor, model in flavor_models.items():
        flavor_predictions[flavor] = round(model.predict(input_scaled)[0])
    
    return total_sales, flavor_predictions

# Example usage
temp_input = 30
pred_total, pred_flavors = predict_sales(temp_input)
print(f"Predicted total sales for {temp_input}°C: {pred_total}")
for flavor, qty in pred_flavors.items():
    print(f"Predicted {flavor} sales: {qty}")

# Visualizing predictions
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_test_pred, color='blue', label='Predicted vs Actual')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='dashed', linewidth=2, label='Ideal Fit')
plt.xlabel('Actual Sales')
plt.ylabel('Predicted Sales')
plt.title('Linear Regression Predictions')
plt.legend()
plt.show()