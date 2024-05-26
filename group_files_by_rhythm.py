import os
import librosa
import numpy as np
from sklearn.cluster import KMeans
import shutil

# Directory containing the WAV files
INPUT_DIR = "/path/to/wav_files"

# Function to extract rhythmic features from an audio file
def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        # Extract beat intervals
        beat_intervals = np.diff(librosa.frames_to_time(beats, sr=sr))
        # Use histogram of beat intervals as features
        hist, _ = np.histogram(beat_intervals, bins=10, range=(0, 2.0))
        return hist
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return None

# Collect features from each WAV file
features = []
file_names = []
for file_name in os.listdir(INPUT_DIR):
    if file_name.endswith('.wav'):
        file_path = os.path.join(INPUT_DIR, file_name)
        feature = extract_features(file_path)
        if feature is not None:
            features.append(feature)
            file_names.append(file_name)
        else:
            print(f"Skipping file due to error: {file_name}")

# Ensure features are available before proceeding
if len(features) == 0:
    print("No features extracted. Please check the WAV files in the directory.")
    exit(1)

# Convert features to numpy array
features = np.array(features)

# Determine the number of clusters
num_clusters = min(len(features), 5)  # Adjust based on the number of files

# Perform K-Means clustering
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(features)
labels = kmeans.labels_

# Move files to subdirectories within the input directory grouped by cluster
for cluster in range(num_clusters):
    cluster_dir = os.path.join(INPUT_DIR, f"pattern_group_{cluster}")
    os.makedirs(cluster_dir, exist_ok=True)
    for idx, label in enumerate(labels):
        if label == cluster:
            base_name = os.path.splitext(file_names[idx])[0]
            new_name = f"{base_name}_group{cluster}.wav"
            old_path = os.path.join(INPUT_DIR, file_names[idx])
            new_path = os.path.join(cluster_dir, new_name)
            print(f"Moving {old_path} to {new_path}")
            shutil.move(old_path, new_path)

print("Files grouped and renamed based on rhythmic patterns.")
