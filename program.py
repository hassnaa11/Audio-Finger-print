import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
import os
# Load ui
Ui_MainWindow, QtBaseClass = uic.loadUiType("ui5.ui")
from finger_print import AudioFingerprint 


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.open_button.clicked.connect(self.open_file)
        self.open_folder.clicked.connect(self.select_folder)
        self.current_file = None
        self.database_folder = None
        
        self.songs_labels = [self.first_song_label, self.second_song_label, self.third_song_label, self.fourth_song_label, self.fifth_song_label]
        self.songs_progress_bars = [self.first_progressBar, self.second_progressBar, self.third_progressBar, self.fourth_progressBar, self.fifth_progressBar]
        
        
        self.fingerprinter = AudioFingerprint()
        
    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Query Audio", "", "Audio Files (*.mp3 *.wav)")
        files = [files]  # Wrap the single file in a list for consistency

        if files and all(files):  # Check if at least one file is selected
            if len(files) == 1:
                self.current_file = files[0]
                if self.database_folder:
                    self.find_similar_songs()
            elif len(files) == 2:
                self.current_file_1 = files[0]
                self.current_file_2 = files[1]
                self.compare_files()

    
    def select_folder(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Database Directory")
        if dir_path:
            self.database_folder = dir_path
            if self.current_file:
                self.find_similar_songs() 
                
                
    def find_similar_songs(self):
        """Find similar songs to the query audio"""
        if not self.current_file or not self.database_folder:
            return
        
        query_fingerprint = self.fingerprinter.generate_fingerprint(self.current_file)
        if not query_fingerprint:
            return
        
        # Get list of songs in database
        songs = [f for f in os.listdir(self.database_folder) 
                if f.lower().endswith(('.mp3', '.wav'))]
        
        similarities = []
        for i, song in enumerate(songs):
            song_path = os.path.join(self.database_folder, song)
            song_fingerprint = self.fingerprinter.generate_fingerprint(song_path)
            if song_fingerprint:
                similarity = self.fingerprinter.compute_similarity(
                    query_fingerprint, song_fingerprint)
                similarities.append((song, similarity))
        
        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        print("similarities: ", similarities)
        
        for i, (song, similarity) in enumerate(similarities):
            print("i = ", i, "song: ", song, "similarity: ", similarity)
            self.songs_labels[i].setText(song) 
            self.songs_progress_bars[i].setValue(int(similarity * 100))
            if i == 4:
                break
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())