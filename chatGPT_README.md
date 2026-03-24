# Voice Reflection Coach

말이 막히는 순간을 감지하고, 질문으로 생각을 끌어내 복기와 다음 행동까지 연결하는 음성 인터랙션 AI입니다.

## 1. Overview

### 프로젝트 한 줄 소개

면접이나 중요한 대화 후, 사용자가 말로 복기하면  
AI가 끊긴 지점을 감지하고 적절한 질문을 던져  
생각을 더 끌어낸 뒤 요약과 액션 아이템까지 정리해주는 시스템입니다.

### 왜 만들었는가

면접이나 중요한 대화 후 복기가 중요하지만,  
텍스트로 정리하려면 귀찮고 생각이 잘 안 이어지는 문제가 있습니다.  
실제로는 혼잣말이나 전화처럼 “말하면서” 복기하는 경우가 많고,  
이때 누군가 질문해주면 더 많은 기억과 생각이 나옵니다.

이 프로젝트는 이 지점을 해결하기 위해 시작했습니다.

### 핵심 문제 정의

- 복기는 중요하지만 잘 기록되지 않음
- 혼자 말하면 금방 막힘
- 텍스트보다 음성이 더 자연스럽게 생각을 끌어냄
- 단순 기록이 아니라 “생각을 확장시키는 질문”이 필요함

## 2. Demo

### 예시 시나리오

1. 사용자가 면접 후 복기를 시작한다
2. 시스템이 발화를 텍스트로 변환한다
3. 사용자가 멈추는 순간, AI가 질문을 던진다
4. 대화가 끝나면 전체 복기를 요약한다
5. 다음 액션 아이템을 생성한다

### 예시 대화

- 사용자: "오늘 면접에서 프로젝트 질문이 나왔는데..."
- AI: "어떤 프로젝트 질문이었어요?"
- 사용자: "내가 했던 역할을 설명하라고 했는데 좀 꼬였어"
- AI: "어느 부분에서 가장 꼬였다고 느꼈어요?"
- ...
- 최종 결과:
  - 잘한 점
  - 아쉬운 점
  - 다음 연습 포인트

> 여기에 GIF / 스크린샷 / 데모 영상 링크 넣기

## 3. Features

### MVP 기능

- 음성 입력 기반 복기 시작
- STT 기반 발화 텍스트 변환
- 침묵/끊김 감지
- 질문 기반 대화 이어가기
- 복기 요약 및 액션 아이템 생성

### 이후 확장 가능 기능

- 면접 유형별 질문 모드
- 세션별 비교 분석
- 반복 실수 패턴 탐지
- 캐릭터별 질문 스타일 변경
- 루틴 앱/노트 앱 연동

## 4. System Architecture

```text
[User Voice Input]
   ↓
[STT Module]
   ↓
[Conversation Manager]
   ├─ 세션 관리
   ├─ 침묵 감지
   └─ 대화 상태 판단
   ↓
[Question Engine]
   ├─ Rule-based Question
   └─ LLM-based Question Refinement
   ↓
[Response Output (Text / TTS)]
   ↓
[Reflection Analyzer]
   ├─ 요약
   ├─ 잘한 점 / 아쉬운 점
   └─ 액션 아이템 생성
   ↓
[Session Storage]
```

설계 포인트

- 단순 챗봇이 아니라 대화 흐름 제어를 목표로 설계
- 사용자의 발화 내용뿐 아니라 침묵도 신호로 사용
- 질문은 “정답 제시”보다 “생각 확장”에 초점
- 복기 결과를 다음 행동으로 이어지게 설계

## 5. Tech Stack

Backend: FastAPI
STT: Whisper / Whisper API
LLM: OpenAI API (or Claude)
TTS: Optional
Storage: SQLite / JSON
Frontend: 간단한 Web UI or CLI

## 6. Core Logic

1. 침묵 감지
   사용자가 일정 시간 이상 말하지 않으면 끊김으로 판단
   끊김 상태에서 후속 질문 생성

2. 질문 생성
   Rule 기반 템플릿으로 기본 흐름 유지
   LLM으로 직전 발화 맥락을 반영해 질문 보정

3. 복기 요약
   전체 대화를 기반으로
   잘한 점
   아쉬운 점
   액션 아이템
   생성

## 7. Project Structure

```text
project/
├── app/
│   ├── main.py
│   ├── api/
│   ├── services/
│   │   ├── stt_service.py
│   │   ├── question_service.py
│   │   ├── reflection_service.py
│   │   └── tts_service.py
│   ├── core/
│   │   ├── silence_detector.py
│   │   └── session_manager.py
│   ├── prompts/
│   └── models/
├── data/
│   ├── audio/
│   └── sessions/
├── frontend/
└── README.md
```

## 8. Getting Started

Installation

````bash
git clone <repo-url>
cd <project-name>
pip install -r requirements.txt


Environment Variables
```bash
OPENAI_API_KEY=...
````

Run

```bash
uvicorn app.main:app --reload
```

## 9. API / Main Flow

주요 흐름
POST /session/start
POST /session/{id}/voice
POST /session/{id}/analyze
GET /session/{id}

실제 구현 후 엔드포인트 추가

## 10. What I Focused On

이 프로젝트에서 특히 집중한 부분은 아래와 같습니다.

음성이 필수인 문제 정의
사용자의 “막힘”을 감지하는 대화 흐름 설계
질문을 통해 생각을 끌어내는 인터랙션 설계
대화를 복기 요약과 다음 행동으로 연결하는 구조

## 11. Limitations

침묵만으로는 실제 “생각 막힘”을 완벽히 판단하기 어려움
질문 품질이 발화 맥락에 크게 의존함
STT 품질에 따라 후속 분석 정확도가 달라질 수 있음

## 12. Future Work

면접 외 대화/회고 상황으로 확장
질문 스타일 개인화
세션 간 성장 추적
음성 감정 신호 반영
실시간 스트리밍 대화로 개선

## 13. Why This Project Matters

이 프로젝트는 단순히 음성 입력을 붙인 챗봇이 아니라,
말이 막히는 순간을 감지하고 질문으로 사고를 확장하는 인터랙션 시스템을 목표로 합니다.

특히 실제 면접 복기처럼
텍스트보다 음성이 더 자연스러운 문제를 대상으로 했다는 점에서
“음성이 핵심인 AI 경험”을 설계하고 구현하는 데 의미가 있습니다.

# 작성 팁

README 첫 화면에서 바로 보여야 하는 건 3개야.

1. **무슨 문제를 푸는 프로젝트인지**
2. **왜 음성이 핵심인지**
3. **내가 뭘 설계했는지**

그리고 네 프로젝트는 예쁜 UI보다  
**대화 흐름 설계 / 질문 생성 / 복기 구조화**가 강점이라,  
`Features`보다 `Why`와 `Core Logic`를 더 잘 써야 해.

원하면 내가 다음 답변에서  
이 틀을 바탕으로 **네 프로젝트용 README 초안**을 바로 써줄게.
