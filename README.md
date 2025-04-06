Keystroke-Based Stress Detection using DNN
This project is a machine learning-based approach to detect stress levels from keystroke dynamics. By analyzing keyboard behavior alongside sensor data (like accelerometer and gyroscope readings), a Deep Neural Network (DNN) is trained to classify user states as either Relaxed (0) or Stressed (1).

How It Works
1. Data Preprocessing

- Removes NaN and non-numeric columns
- Scales numeric features using StandardScaler

2. Model Architecture

- Input Layer → Dense(16, ReLU)
- Hidden Layer → Dense(8, ReLU)
- Output Layer → Dense(1, Sigmoid) for binary classification

3. Training

- Uses binary_crossentropy loss and adam optimizer
- Trained for 50 epochs with validation split

4. Testing

- Evaluates the trained model on unseen data
- Compares predictions to actual values and calculates accuracy

Requirements
- Python 3.8+
- TensorFlow / Keras
- pandas
- scikit-learn
- numpy

Results
The DNN achieves competitive accuracy in classifying stress from typing patterns. Ideal for real-time stress monitoring apps or ergonomic feedback systems.
