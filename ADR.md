# Architectural Decision Records

- 아키텍처 변경에 대한 의사 결정을 내리기 위한 혹은 결정난 사항을 기록하는 파일
- 개인 프로젴트로 프로젝트가 크지 않기에 하나의 파일에 정리 진행
- 템플릿: [Documenting architecture decisions - Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) ([한국어 번역](https://github.com/joelparkerhenderson/architecture-decision-record/tree/main/locales/ko/템플릿/의사%20결정%20기록%20템플릿-by-michael-nygard))을 기반으로 개인 프로젝트에 맞게 변경
    ```text
    ### 상태
    > - 제안됨 (Proposed): 아이디어 단계.
    > - 승인됨 (Accepted): 실제 코드에 적용하기로 함.
    > - 대체됨 (Superseded): 나중에 결정이 바뀌어 다른 ADR로 넘어갔을 때
    > - 거부됨 (Rejected): 검토해봤으나 도입하지 않기로 함

    ### 문맥
    > - 어떤 상황인가?
    > - 어떤 기술적 문제가 있는가?

    ### 결정
    > - 무엇을 하기로 했는가?
    > - 왜 이 방법인가? (비교했던 다른 후보가 있다면 간단히 언급)

    ### 결과
    > - 장점: (예: 코드 가독성 향상, 빌드 속도 개선)
    > - 단점/주의점: (예: 학습 곡선 있음, 라이브러리 의존성 추가)
    ```

## ADR-001: 아키텍처를 레이어드에서 도메인으로 변경
### 상태
- 승인됨

### 문맥
- 프로젝트를 시작하기 전, 더 나은 아키텍처가 있을지에 대한 의문이 들었음    
- 이전 프로젝트와 달리, 여러 API를 호출이 필요함

### 결정
- 레이어드 구조 $\rightarrow$ 도메인 구조:   
    도메인 기반으로 폴더를 나누기로 함   
    레이어드 구조에서는 각 기능을 수정하기 불편함이 예상됨   

### 결과

## ADR-002:
### 상태
- 승인됨

### 문맥
- 오디오 전처리 과정이 길어질 때를 대비하여,   
이를 stt 과정과 분리하는게 좋을지 아니면 함께 가져가는게 좋을지 고민됨

### 결정 
- `domain/transcript` → `domain/audio + domain/transcript` 로 분리:    
    오디오의 노이즈가 많을 경우 등 오디오 전처리 과정이 많아질 것으로 예상   
	VAD, 화자 분리, 문장별 분리 등 다양한 경우를 실험의 편리성을 위해 분리가 더 낫다는 판단 

### 결과

