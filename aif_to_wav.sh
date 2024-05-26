#!/bin/bash

# Directory containing the AIFF files
INPUT_DIR="/path/to/aif_files"

# Change to the input directory
cd "$INPUT_DIR" || exit

# Loop through all AIFF files in the directory
for file in *.aif; do
  # Check if there are no .aiff files
  if [ "$file" = "*.aif" ]; then
    echo "No AIF files found in the directory."
    exit 0
  fi

  # Extract the filename without extension
  base_name="${file%.aif}"

  # Convert AIFF to 16-bit WAV
  ffmpeg -i "$file" -acodec pcm_s16le "${base_name}.wav"

  # Check if the conversion was successful
  if [ $? -eq 0 ]; then
    # Delete the original AIF file
    rm "$file"
  else
    echo "Conversion failed for file: $file"
  fi
done
