# Audio-Finger-print

## Overview

This project implements a Shazam-like application for signal fingerprinting and identification. The system is designed to identify signals, such as songs or other audio files, based on their intrinsic features. 

## Features

### Song Repository
- A shared repository of songs with separated tracks: full song, music, and vocals.
  
### Spectrogram Generation
- Generates spectrograms for:
  - Full song
  - Music-only track
  - Vocals-only track

### Feature Extraction
- Extracts main features from each spectrogram.
- Features are hashed using perceptual hashing for compact representation.

### Fingerprint Matching
- Compares a given audio file against the repository to find the closest matches.
- Outputs a sorted similarity list with similarity scores in a clean GUI.

### File Blending
- Takes two audio files, applies a weighted average of their features (controlled via a slider), and treats the blend as a new file.
- Searches for the closest songs to the blended file.

## Usage

1. **Install requirements**:
   ```bash
   pip install -r requirements.txt
2. **Clone the repository**:
   ```bash
   git clone https://github.com/hassnaa11/Audio-Finger-print.git
2. **Run the program**:
   ```bash
   python program.py


## Contributors

<table align="center" width="100%">
  <tr>
    <td align="center" width="20%">
      <a href="https://github.com/yasmine-msg79">
        <img src="https://github.com/yasmine-msg79.png?size=100" style="width:80%;" alt="yasmine-msg79"/>
      </a>
      <br />
      <a href="https://github.com/yasmine-msg79">yasmine Mahmoud</a>
    </td>
    <td align="center" width="20%">
      <a href="https://github.com/hassnaa11">
        <img src="https://github.com/hassnaa11.png?size=100" style="width:80%;" alt="hassnaa11"/>
      </a>
      <br />
      <a href="https://github.com/hassnaa11">Hassnaa Hossam</a>
    </td>
    <td align="center" width="20%">
      <a href="https://github.com/shahdragab89">
        <img src="https://github.com/shahdragab89.png?size=100" style="width:80%;" alt="shahdragab89"/>
      </a>
      <br />
      <a href="https://github.com/shahdragab89">Shahd Ragab</a>
    </td>
   <td align="center" width="20%">
      <a href="https://github.com/Emaaanabdelazeemm">
        <img src="https://github.com/Emaaanabdelazeemm.png?size=100" style="width:80%;" alt="Emaaanabdelazeemm"/>
      </a>
      <br />
      <a href="https://github.com/Emaaanabdelazeemm">Eman Abdelazeem</a>
    </td>
   <td align="center" width="20%">
      <a href="https://github.com/Ayat-Tarek">
        <img src="https://github.com/Ayat-Tarek.png?size=100" style="width:80%;" alt="Ayat-Tarek"/>
      </a>
      <br />
      <a href="https://github.com/Ayat-Tarek">Ayat Tarek</a>
    </td>
  </tr>
</table>
