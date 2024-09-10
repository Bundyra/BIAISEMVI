import os
import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam

import pickle

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=30)
    features = []
    features.append(np.mean(librosa.feature.chroma_stft(y=y, sr=sr)))
    features.append(np.mean(librosa.feature.rms(y=y)))
    features.append(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    features.append(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
    features.append(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
    features.append(np.mean(librosa.feature.zero_crossing_rate(y)))
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features.extend(np.mean(mfccs.T, axis=0))
    return features

dataset_path = 'D:/pycharm/projects/BIAISEMVI/BIAISEMVI/DataTest/Data/genres_original'

data = []
labels = []
genres = os.listdir(dataset_path)

for genre in genres:
    genre_path = os.path.join(dataset_path, genre)
    if os.path.isdir(genre_path):
        for file in os.listdir(genre_path):
            if file.endswith('.wav'):
                file_path = os.path.join(genre_path, file)
                features = extract_features(file_path)
                data.append(features)
                labels.append(genre)

df = pd.DataFrame(data)
df['label'] = labels

le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])

X = df.drop(columns='label')
Y = df['label']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

Y_train_encoded = to_categorical(Y_train)
Y_test_encoded = to_categorical(Y_test)

model = Sequential([

    Dense(512, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    BatchNormalization(),
    Dropout(0.5),

    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),

    Dense(128, activation='relu'),
    BatchNormalization(),
    Dropout(0.4),

    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),

    Dense(32, activation='relu'),
    BatchNormalization(),
    Dropout(0.3),

    Dense(len(genres), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train_scaled, Y_train_encoded, epochs=200, validation_data=(X_test_scaled, Y_test_encoded))

test_loss, test_accuracy = model.evaluate(X_test_scaled, Y_test_encoded)
print("Test accuracy:", test_accuracy)

model.save('genre_classifier_nn.h5')

with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
