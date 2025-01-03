import librosa
import numpy as np
from scipy.signal import find_peaks
import imagehash
from PIL import Image
import json
import os
from sklearn.metrics.pairwise import cosine_similarity

class AudioFingerprint:
    def __init__(self):
        self.features = {}
        self.database_path = "database.json"
        
    def extract_features(self, audio_data, sr):
        features = {}
        
        # 1. Compute mel-spectrogram: Converts the waveform into a time-frequency representation
        mel_spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr, 
                                                n_mels=128, fmax=8000)
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)
        
        # 2. Extract spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
        features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
            
        # 3. Extract spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
        features['spectral_rolloff_mean'] = float(np.mean(spectral_rolloff))
        
        # 4. Extract MFCCs
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        features['mfccs_mean'] = np.mean(mfccs, axis=1).tolist()
        
        # 5. Extract chroma features
        chromagram = librosa.feature.chroma_stft(y=audio_data, sr=sr)
        features['chroma_mean'] = np.mean(chromagram, axis=1).tolist()
        
        # 7. Extract harmonic and percussive components
        y_harmonic, y_percussive = librosa.effects.hpss(audio_data)
        features['harmonic_ratio'] = float(np.mean(np.abs(y_harmonic)) / np.mean(np.abs(audio_data)))
        features['percussive_ratio'] = float(np.mean(np.abs(y_percussive)) / np.mean(np.abs(audio_data)))
        
        # 6. Find peaks in mel spectrogram
        peaks = []
        for i in range(mel_spectrogram_db.shape[0]):
            peak_indices, _ = find_peaks(mel_spectrogram_db[i, :])
            if len(peak_indices) > 0:
                peaks.extend([(int(i), int(j)) for j in peak_indices])
        features['peak_positions'] = peaks[:100]
        
        return features
    
    def compute_perceptual_hash(self, mel_spectrogram_db):
        img_data = ((mel_spectrogram_db - mel_spectrogram_db.min()) * 255 / 
                   (mel_spectrogram_db.max() - mel_spectrogram_db.min())).astype(np.uint8)
        img = Image.fromarray(img_data)
        
        return {
            'average_hash': str(imagehash.average_hash(img)),
            'phash': str(imagehash.phash(img)),
            'dhash': str(imagehash.dhash(img)),
            'whash': str(imagehash.whash(img))
        }
    
    def generate_fingerprint(self, audio_path):
        try:
            audio_data, sr = librosa.load(audio_path)
            
            # Extract features
            features = self.extract_features(audio_data, sr)
            
            # Compute mel spectrogram for hashing
            mel_spec = librosa.feature.melspectrogram(y=audio_data, sr=sr)
            mel_spectrogram_db = librosa.power_to_db(mel_spec, ref=np.max)
            
            # Compute perceptual hashes
            hashes = self.compute_perceptual_hash(mel_spectrogram_db)
            
            self.save_fingerprint(audio_path, features)
            
            return {
                'features': features,
                'hashes': hashes
            }
        except Exception as e:
            print(f"Error generating fingerprint for {audio_path}: {str(e)}")
            return None
    
    def save_fingerprint(self, audio_path, fingerprint):
        try:
            with open(self.database_path, 'r') as f:
                database = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            database = {}
        
        database[os.path.basename(audio_path)] = fingerprint
        
        with open(self.database_path, 'w') as f:
            json.dump(database, f)
    
    def compute_similarity(self, fingerprint1, fingerprint2):
        try:
            # Compare MFCCs
            mfcc_sim = cosine_similarity(
                [fingerprint1['features']['mfccs_mean']], 
                [fingerprint2['features']['mfccs_mean']]
            )[0][0]
            
            # Compare chroma features
            chroma_sim = cosine_similarity(
                [fingerprint1['features']['chroma_mean']], 
                [fingerprint2['features']['chroma_mean']]
            )[0][0]
            
            # Compare spectral features
            centroid_diff = abs(fingerprint1['features']['spectral_centroid_mean'] - 
                              fingerprint2['features']['spectral_centroid_mean'])
            rolloff_diff = abs(fingerprint1['features']['spectral_rolloff_mean'] - 
                              fingerprint2['features']['spectral_rolloff_mean'])
            
            # Normalize differences
            max_centroid = max(fingerprint1['features']['spectral_centroid_mean'],
                             fingerprint2['features']['spectral_centroid_mean'])
            max_rolloff = max(fingerprint1['features']['spectral_rolloff_mean'],
                            fingerprint2['features']['spectral_rolloff_mean'])
            
            centroid_sim = 1 - (centroid_diff / max_centroid if max_centroid > 0 else 0)
            rolloff_sim = 1 - (rolloff_diff / max_rolloff if max_rolloff > 0 else 0)
            
            # 6. Harmonic/Percussive similarity
            harmonic_sim = 1 - abs(
                fingerprint1['features']['harmonic_ratio'] - fingerprint2['features']['harmonic_ratio']
            )
            percussive_sim = 1 - abs(
                fingerprint1['features']['percussive_ratio'] - fingerprint2['features']['percussive_ratio']
            )
            harmonic_percussive_sim = (harmonic_sim + percussive_sim) / 2
        
            # Compare perceptual hashes
            hash_sim = sum(h1 == h2 for h1, h2 in zip(
                fingerprint1['hashes'].values(), 
                fingerprint2['hashes'].values()
            )) / len(fingerprint1['hashes'])
            
            # Weighted combination
            similarity_score = (0.3 * mfcc_sim + 
                              0.2 * chroma_sim + 
                              0.2 * centroid_sim +
                              0.1 * rolloff_sim +
                              0.1 * harmonic_percussive_sim +
                              0.2 * hash_sim)
            
            return max(0, min(1, similarity_score))  # Ensure score is between 0 and 1
            
        except Exception as e:
            print(f"Error computing similarity: {str(e)}")
            return 0