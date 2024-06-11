import os
import librosa
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle

# Funkcja do ekstrakcji cech z plików audio
def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=30)  # Wczytaj plik audio, ograniczając długość do 30 sekund
    features = []
    features.append(np.mean(librosa.feature.chroma_stft(y=y, sr=sr)))  # chroma_stft
    features.append(np.mean(librosa.feature.rms(y=y)))  # rms
    features.append(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))  # spectral_centroid
    features.append(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))  # spectral_bandwidth
    features.append(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))  # spectral_rolloff
    features.append(np.mean(librosa.feature.zero_crossing_rate(y)))  # zero_crossing_rate
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features.extend(np.mean(mfccs.T, axis=0))  # MFCCs
    print(features)
    return features

# Ścieżka do katalogu z plikami audio
dataset_path = 'X:/BIAI/Data/genres_original'

# Przygotowanie danych
data = []
labels = []
genres = os.listdir(dataset_path)

for genre in genres:
    genre_path = os.path.join(dataset_path, genre)
    if os.path.isdir(genre_path):
        for file in os.listdir(genre_path):
            if file.endswith('.wav'):
                file_path = os.path.join(genre_path, file)
                print(file_path)
                features = extract_features(file_path)
                data.append(features)
                labels.append(genre)

# Konwersja danych do DataFrame
df = pd.DataFrame(data)
df['label'] = labels

# Enkoding etykiet
le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])

# Przygotowanie danych do treningu
X = df.drop(columns='label')
Y = df['label']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.25, random_state=42)

# Skalowanie danych
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Trening modelu
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, Y_train)

# Predykcja i ewaluacja
Y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy:", accuracy)

# Zapis modelu, enkodera i skalera
with open('genre_classifier.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('label_encoder.pkl', 'wb') as f:
    pickle.dump(le, f)
with open('scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
