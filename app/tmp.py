import sys
import os

# import whisper_processor 
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.normpath(os.path.join(BASE_DIR, "../externals/whisper_cpp/models/ggml-base.bin"))
audio_path = os.path.normpath(os.path.join(BASE_DIR, "../externals/whisper_cpp/samples/jfk.wav"))

print("MODEL FILE EXIST?: ", os.path.exists(model_path))
print("AUDIO FILE EXIST?: ", os.path.isfile("../externals/whisper_cpp/samples/jfk.wav"))

def process_audio(wav_file, model_name="base.en"):
    # 1. 모델 경로 절대 경로로 확정
    model_path = os.path.join(BASE_DIR, f"../externals/whisper_cpp/models/ggml-{model_name}.bin")
    model_path = os.path.abspath(model_path)

    # 2. 실행 파일(whisper-cli) 절대 경로로 확정
    executable = os.path.join(BASE_DIR, "../externals/whisper_cpp/build/bin/whisper-cli")
    executable = os.path.abspath(executable)

    # 3. 입력 오디오 파일 절대 경로로 확정
    wav_file_abs = os.path.abspath(wav_file)

    print(f"!! EXECUTABLE: {executable}")
    print(f"!! MODEL FILE EXIST?: {os.path.exists(model_path)}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    if not os.path.exists(wav_file_abs):
        raise FileNotFoundError(f"WAV file not found: {wav_file_abs}")

    # 4. 명령어 구성 (모두 절대 경로 사용)
    # f-string에서 경로에 공백이 있을 수 있으므로 따옴표로 감싸주는 것이 안전합니다.
    full_command = f'"{executable}" -m "{model_path}" -f "{wav_file_abs}" -nt'

    # Execute
    process = subprocess.Popen(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    # whisper.cpp는 일반적인 로그 정보도 stderr로 보낼 때가 있습니다.
    # 진짜 에러인지 확인하려면 returncode를 체크하는 것이 더 정확합니다.
    if process.returncode != 0:
        raise Exception(f"Error processing audio: {error.decode('utf-8')}")

    return output.decode('utf-8').strip().replace('[BLANK_AUDIO]', '').strip()



try:
    result = process_audio("../externals/whisper_cpp/samples/jfk.wav", "base")
    print("RESULT:", result)

except Exception as e:
    print(f"Error: {e}")