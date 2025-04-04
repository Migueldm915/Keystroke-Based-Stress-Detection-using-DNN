import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle

# 🔹 Load the trained model
model = keras.models.load_model("Stress_Detection_DNN.h5")

# 🔹 Load new test data
df_test = pd.read_csv("TestData.csv")  # Ensure this has the same structure as training data

# 🔹 Shuffle the dataset to remove any order bias
df_test = shuffle(df_test, random_state=42).reset_index(drop=True)

# 🔹 Drop NaN values
df_test = df_test.dropna()

# 🔹 Remove non-numeric columns
df_test = df_test.select_dtypes(include=[np.number])

# 🔹 Split features (X) and actual target variable (y)
y_actual = df_test["Condition"]  # Assuming "Condition" is the actual target column
X_test = df_test.drop(columns=["Condition"])  # Remove target column from features

# 🔹 Ensure test data has the same features as training
expected_features = 8  # Update this based on training data
X_test = X_test.iloc[:, :expected_features]  # Keep only the first N features

# 🔹 Standardize the test data using the same scaler as training
scaler = StandardScaler()
X_test_scaled = scaler.fit_transform(X_test)  #  Use the same scaler as training

# 🔹 Make predictions
predictions = model.predict(X_test_scaled)

# 🔹 Convert predictions to binary labels (0 = relaxed, 1 = stressed)
y_pred = [1 if pred > 0.5 else 0 for pred in predictions]

# 🔹 Calculate accuracy
accuracy = accuracy_score(y_actual, y_pred)
print(f"Model Accuracy on Test Data: {accuracy * 100:.2f}%")

# 🔹 Save predictions for review
df_test["Predicted Condition"] = y_pred
df_test.to_csv("Test_Predictions&Actual.csv", index=False)
print("Predictions saved in 'Test_Predictions&Actual.csv'")
