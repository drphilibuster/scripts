import wave
import numpy as np
import os

def split_channels(input_wav, output_directory):
    # Open the input WAV file
    with wave.open(input_wav, 'rb') as wav_file:
        # Check the number of channels
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        print(f"Number of channels: {num_channels}")
        print(f"Sample width: {sample_width} bytes")
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Number of frames: {num_frames}")

        # Ensure we have 16 channels
        if num_channels != 16:
            raise ValueError(f"Expected 16 channels, but got {num_channels} channels.")

        # Read the audio frames
        frames = wav_file.readframes(num_frames)

        # Convert the frames to a numpy array
        audio_data = np.frombuffer(frames, dtype=np.int16)

        # Reshape the array based on the number of channels
        audio_data = audio_data.reshape(-1, num_channels)

        # Create output directory if it does not exist
        os.makedirs(output_directory, exist_ok=True)

        # Split each channel and save as a separate mono WAV file
        for i in range(num_channels):
            output_file = os.path.join(output_directory, f'channel_{i+1}.wav')
            # Extract data for the channel
            channel_data = audio_data[:, i]
            # Write the channel data to a new WAV file
            with wave.open(output_file, 'wb') as channel_wav:
                channel_wav.setnchannels(1)
                channel_wav.setsampwidth(sample_width)
                channel_wav.setframerate(sample_rate)
                channel_wav.writeframes(channel_data.tobytes())
            print(f"Saved channel {i+1} to {output_file}")

# Example usage
input_wav="/Users/jamesfrontz/Library/Application Support/Rack2/recordings/restacker/restacker_202406102252_zS.16chan.000.wav"
output_directory="/Users/jamesfrontz/Library/Application Support/Rack2/recordings/restacker/split"

split_channels(input_wav, output_directory)
