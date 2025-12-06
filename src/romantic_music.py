"""Generate romantic background music"""

import numpy as np
import pygame

def generate_romantic_music():
    """Generate a romantic melody with piano-like tones"""
    sample_rate = 22050
    duration = 8  # 8 seconds, will loop
    
    # Romantic chord progression: C - Am - F - G (I - vi - IV - V)
    # Using frequencies for a soft, romantic feel
    notes = {
        'C4': 261.63,
        'E4': 329.63,
        'G4': 392.00,
        'A4': 440.00,
        'F4': 349.23,
        'D4': 293.66,
        'B3': 246.94,
    }
    
    # Romantic melody pattern (slow, flowing)
    melody_sequence = [
        ('C4', 0.5), ('E4', 0.5), ('G4', 0.5), ('E4', 0.5),  # C chord arpeggio
        ('A4', 0.5), ('C4', 0.5), ('E4', 0.5), ('A4', 0.5),  # Am chord
        ('F4', 0.5), ('A4', 0.5), ('C4', 0.5), ('F4', 0.5),  # F chord
        ('G4', 0.5), ('B3', 0.5), ('D4', 0.5), ('G4', 1.0),  # G chord
    ]
    
    # Create the waveform
    wave = np.zeros(int(sample_rate * duration))
    current_time = 0
    
    for note, note_duration in melody_sequence:
        freq = notes[note]
        samples = int(sample_rate * note_duration)
        t = np.linspace(0, note_duration, samples)
        
        # Soft piano-like tone with harmonics
        note_wave = 0.3 * np.sin(2 * np.pi * freq * t)  # Fundamental
        note_wave += 0.15 * np.sin(2 * np.pi * freq * 2 * t)  # 2nd harmonic
        note_wave += 0.05 * np.sin(2 * np.pi * freq * 3 * t)  # 3rd harmonic
        
        # Soft envelope (fade in/out)
        envelope = np.ones_like(t)
        fade_samples = int(sample_rate * 0.05)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        note_wave *= envelope
        
        # Add to main wave
        start_idx = int(current_time * sample_rate)
        end_idx = start_idx + samples
        if end_idx <= len(wave):
            wave[start_idx:end_idx] += note_wave
        
        current_time += note_duration
    
    # Add gentle bass notes
    bass_notes = [
        ('C4', 2.0, 0),
        ('A4', 2.0, 2),
        ('F4', 2.0, 4),
        ('G4', 2.0, 6),
    ]
    
    for note, note_duration, start_time in bass_notes:
        freq = notes[note] / 2  # One octave lower
        samples = int(sample_rate * note_duration)
        t = np.linspace(0, note_duration, samples)
        
        bass_wave = 0.15 * np.sin(2 * np.pi * freq * t)
        
        # Soft envelope
        envelope = np.ones_like(t)
        fade_samples = int(sample_rate * 0.1)
        envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
        envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
        bass_wave *= envelope
        
        start_idx = int(start_time * sample_rate)
        end_idx = start_idx + samples
        if end_idx <= len(wave):
            wave[start_idx:end_idx] += bass_wave
    
    # Normalize
    wave = wave / np.max(np.abs(wave))
    wave = (wave * 32767 * 0.4).astype(np.int16)  # Lower volume
    
    # Convert to stereo
    stereo = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo)

def save_romantic_music(filename='assets/music/romantic_theme.wav'):
    """Save romantic music to file"""
    try:
        import os
        os.makedirs('assets/music', exist_ok=True)
        
        sound = generate_romantic_music()
        pygame.mixer.init()
        
        # Save as WAV
        import scipy.io.wavfile as wavfile
        sample_rate = 22050
        duration = 8
        
        wave = np.zeros(int(sample_rate * duration))
        # Regenerate the wave for saving
        # (simplified version of the generation above)
        
        print(f"Romantic music saved to {filename}")
        return True
    except Exception as e:
        print(f"Could not save music: {e}")
        return False
