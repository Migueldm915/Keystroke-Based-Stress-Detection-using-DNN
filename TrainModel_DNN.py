import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 🔹 Load the dataset
df = pd.read_csv("KeyStrokeData.csv")

# 🔹 Drop NaN values
df = df.dropna()

# 🔹 Remove non-numeric columns
df = df.select_dtypes(include=[np.number])

# 🔹 Split features (X) and target variable (y)
X = df.drop(columns=["Condition"])  # Replace "Condition" with actual target column name
y = df["Condition"]

# 🔹 Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🔹 Standardize numerical data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 🔹 Build the DNN Model
model = keras.Sequential([
    keras.layers.Dense(16, activation="relu", input_shape=(X_train_scaled.shape[1],)),
    keras.layers.Dense(8, activation="relu"),
    keras.layers.Dense(1, activation="sigmoid")  # Output layer for binary classification
])

# 🔹 Compile the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# 🔹 Train the model
model.fit(X_train_scaled, y_train, epochs=50, batch_size=16, validation_data=(X_test_scaled, y_test))

# 🔹 Save the trained model
model.save("Stress_Detection_DNN.h5")
print("Model saved as 'Stress_Detection_DNN.h5'")

# 🔹 Evaluate the model
test_loss, test_acc = model.evaluate(X_test_scaled, y_test)
print(f"Model Accuracy: {test_acc * 100:.2f}%")
