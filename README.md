# ReInterviewer

면접 복기를 도와주는 작은 친구. 친구에게 면접 썰을 풀어주듯이 이야기하면서 면접 복기와 정리를 도와주는 AI입니다.

## 1. Overview
### 프로젝트 간단 소개
면접 후 사용자가 말로 복기하면 AI가 끊긴 지점을 감지하고, 적절한 질문을 던져 생각을 더 끌어내는 걸 도와줍니다.   
복기 후에는 요약과 액션 아이템까지 정리해줍니다.

### 왜 만들었는가
면접 후 복기가 중요하지만, 글로 정리하려면 귀찮고 쓰다보면 면접 질문이 기억나지 않는 문제가 종종 생깁니다.   
하지만 가족이나 친구들에게 전화로 “말하면서” 복기하게 되면 면접 흐름과 답변을 자연스럽게 말하게 됩니다.    
이때 질문까지 받으면 면접 복기가 더 생생해집니다.  

이 프로젝트는 "말하면서 면접 복기하고 편리하게 복기하기" 위해 시작했습니다.

### 핵심 문제 정의
- 복기는 중요하지만 기록을 잘 안하게 됨
- 혼자 생각하면 잘 생각나지 않음
- 글로 쓰는 것보다 말할 때 생각이 더 자연스럽게 남
- 기억이 안 날 떄, 누군가가 질문해주면 더 많은 기억이 떠오르게 됨
- 단순 기록에서 멈추지 않고, 정리와 요약까지 편리하게 하고자 함

## 2. Getting Started
1. 가상환경 설정
```bash
git clone https://github.com/ParkSomin23/ReInterviewer.git

cd ReInterviewer

pip install uv
uv sync
```

## 3. Demo

## 4. Features

## 5. 시스템 구조

## 6. 사용한 기술
- STT: [Whisper.cpp](https://github.com/ggml-org/whisper.cpp)
- LLM: OpenAI API (or Claude)
- TTS: Optional
- Backend: FastAPI
- Storage: SQLite / JSON
- Frontend: 간단한 Web UI or CLI

## 7. Core Logic

## 8. API / Main Flow

## 9. Limitations

## 10. Future Work