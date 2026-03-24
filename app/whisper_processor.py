import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def process_audio(wav_file, model_name="base.en"):
    """
    Processes an audio file using a specified model and returns the processed string.

    :param wav_file: Path to the WAV file
    :param model_name: Name of the model to use
    :return: Processed string output from the audio processing
    :raises: Exception if an error occurs during processing

    ex: ../externals/whisper_cpp/build/bin/whisper-cli -m ../externals/whisper_cpp/models/ggml-base.bin -f ../externals/whisper_cpp/samples/jfk.wav 
    """

    model = f"/models/ggml-{model_name}.bin"
    model = os.path.normpath(os.path.join(BASE_DIR, f"../externals/whisper_cpp/{model}"))

    print("!! MODEL FILE EXIST?: ", os.path.exists(model))

    # Check if the file exists
    if not os.path.exists(model):
        raise FileNotFoundError(f"Model file not found: {model} \n\nDownload a model with this command:\n\n> bash ./models/download-ggml-model.sh {model_name}\n\n")

    if not os.path.exists(wav_file):
        raise FileNotFoundError(f"WAV file not found: {wav_file}")

    full_command = f"../externals/whisper_cpp/build/bin/whisper-cli -m {model} -f {wav_file} -nt"

    # Execute the command
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the output and error (if any)
    output, error = process.communicate()

    if error:
        raise Exception(f"Error processing audio: {error.decode('utf-8')}")

    # Process and return the output string
    decoded_str = output.decode('utf-8').strip()
    processed_str = decoded_str.replace('[BLANK_AUDIO]', '').strip()

    return processed_str

def main():
    if len(sys.argv) >= 2:
        wav_file = sys.argv[1]
        model_name = sys.argv[2] if len(sys.argv) == 3 else "base.en"
        try:
            result = process_audio(wav_file, model_name)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Usage: python whisper_processor.py <wav_file> [<model_name>]")

if __name__ == "__main__":
    main()
