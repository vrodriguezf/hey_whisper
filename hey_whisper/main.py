#!/usr/bin/env python3
import os
import numpy as np
import sounddevice as sd
import wavio
import pyperclip
import threading
import time
from openai import OpenAI

def run_transcription():
    # Initialize the OpenAI client
    client = OpenAI()
    client.api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
    
    # Recording parameters
    FS = 16000  # Sampling rate (16kHz recommended for Whisper)
    CHANNELS = 1  # Mono recording
    
    # Shared variables for recording
    recording_data = []
    is_recording = True
    
    def audio_callback(indata, frames, time_info, status):
        """Callback function to collect audio data."""
        if status:
            print(f"Recording Status: {status}", flush=True)
        recording_data.append(indata.copy())
    
    def start_recording():
        """Starts the audio recording."""
        with sd.InputStream(samplerate=FS, channels=CHANNELS, callback=audio_callback):
            while is_recording:
                sd.sleep(100)  # Sleep briefly to keep the stream active
    
    def show_loading(stop_event):
        """Displays a loading indicator while waiting for the API response."""
        print("Transcribing audio... Please wait", end='', flush=True)
        while not stop_event.is_set():
            for char in ['|', '/', '-', '\\']:
                print(f'\rTranscribing audio... Please wait {char}', end='', flush=True)
                if stop_event.is_set():
                    break
                time.sleep(0.2)
        print('\rTranscription complete!             ')
    
    print("Recording started... Speak now.")
    
    # Start the recording in a separate thread
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()
    
    # Wait for the user to press Enter to stop recording
    input("Press Enter to stop recording.\n")
    is_recording = False
    recording_thread.join()
    print("Recording stopped.")
    
    # Combine all recorded chunks into a single NumPy array
    audio_array = np.concatenate(recording_data, axis=0)
    
    # Save the recorded audio to a temporary WAV file
    temp_filename = "temp_recording.wav"
    wavio.write(temp_filename, audio_array, FS, sampwidth=2)
    
    # Prepare to show loading indicator during API call
    stop_loading = threading.Event()
    loading_thread = threading.Thread(target=show_loading, args=(stop_loading,))
    loading_thread.start()
    
    # Call the Whisper API to transcribe the audio
    try:
        with open(temp_filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
    except Exception as e:
        stop_loading.set()
        loading_thread.join()
        print(f"\nAn error occurred during transcription: {e}")
        return
    stop_loading.set()
    loading_thread.join()
    
    # Print the transcription
    print("\nTranscription:")
    print(transcription.text)
    
    # Copy the transcription to the clipboard
    try:
        pyperclip.copy(transcription.text)
        print("The transcription has been copied to your clipboard!")
    except pyperclip.PyperclipException:
        print("Failed to copy to clipboard. Please ensure clipboard functionality is supported on your system.")
    
    # Clean up the temporary audio file
    try:
        os.remove(temp_filename)
    except OSError:
        print(f"Warning: Temporary file {temp_filename} could not be deleted.")
