"""Simple music generator for Love Maze"""

import pygame.mixer
import numpy as np
import wave
import struct

def generate_note(frequency, duration, sample_rate=22050, volume=0.3):
    """Generate a single note"""
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, False)
    
    # Generate square wave for 8-bit sound
    wave_data = volume * np.sign(np.sin(2 * np.pi * frequency * t))
    
    return wave_data

def generate_peppy_love_theme(filename, sample_rate=22050):
    """Generate a peppy love-themed chiptune melody inspired by 'Lava'"""
    
    # Note frequencies (in Hz) - Major scale
    notes = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23,
        'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
        'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46,
        'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
        'REST': 0
    }
    
    # Gentle, romantic melody inspired by "Lava" - slow, warm, and flowing
    melody = [
        # "I have a dream I hope will come true"
        ('C5', 0.4), ('D5', 0.4), ('E5', 0.6), ('REST', 0.2),
        ('E5', 0.4), ('D5', 0.4), ('C5', 0.4), ('D5', 0.4),
        ('E5', 0.8), ('REST', 0.4),
        
        # "That you're here with me, and I'm here with you"
        ('G5', 0.4), ('F5', 0.4), ('E5', 0.6), ('REST', 0.2),
        ('D5', 0.4), ('E5', 0.4), ('F5', 0.4), ('E5', 0.4),
        ('D5', 0.8), ('REST', 0.4),
        
        # "I wish that the earth, sea, and the sky up above"
        ('C5', 0.4), ('D5', 0.4), ('E5', 0.6), ('REST', 0.2),
        ('E5', 0.4), ('F5', 0.4), ('G5', 0.6), ('REST', 0.2),
        ('A5', 0.8), ('REST', 0.4),
        
        # "Will send me someone to lava"
        ('G5', 0.4), ('F5', 0.4), ('E5', 0.6), ('REST', 0.2),
        ('D5', 0.4), ('C5', 0.4), ('D5', 0.6), ('REST', 0.2),
        ('C5', 1.2), ('REST', 0.4),
    ]
    
    # Generate melody
    audio_data = np.array([])
    
    for note_name, duration in melody:
        if note_name == 'REST':
            # Silence
            num_samples = int(duration * sample_rate)
            audio_data = np.concatenate([audio_data, np.zeros(num_samples)])
        else:
            frequency = notes[note_name]
            note_data = generate_note(frequency, duration, sample_rate)
            audio_data = np.concatenate([audio_data, note_data])
    
    # Normalize and convert to 16-bit PCM
    audio_data = np.int16(audio_data * 32767)
    
    # Save as WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"Generated music file: {filename}")

def generate_all_music():
    """Generate all music files for the game"""
    import os
    
    music_dir = "assets/music"
    os.makedirs(music_dir, exist_ok=True)
    
    # Generate main theme
    generate_peppy_love_theme(f"{music_dir}/peppy_love_theme.ogg")
    
    print("All music files generated successfully!")

if __name__ == "__main__":
    generate_all_music()
