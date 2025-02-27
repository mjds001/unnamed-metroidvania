"""
A script for trimming the empty sound at the beginning and end of a .wav file
"""
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

base_path = "assets/sounds"
sound = AudioSegment.from_wav(f"{base_path}/jump.wav")

nonsilent_ranges = detect_nonsilent(sound, min_silence_len = 50, silence_thresh = -40)

if nonsilent_ranges:
    start_trim = nonsilent_ranges[0][0]
    trimmed_sound = sound[start_trim:]
    trimmed_sound.export(f"{base_path}/trimmed_jump.wav", format = 'wav')
else:
    print('no nonsilent range found')