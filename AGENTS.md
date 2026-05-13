# AGENTS.md — logickocli

## Project Identity

**logickocli** — Korean ↔ standard-logic coordinate-system tool. CLI + agent skill.

이 도구는 한국어 자연어 추론을 표준 논리 어휘 좌표계로 정규화한다. 같은
개념이 "연언 제거" / "conjunction elimination" / "∧E" / "and-elim" 어느
표현으로 들어오든 같은 ID로 묶어 인간과 에이전트가 동일한 노드를 가리키게
한다.

이름의 구성:

- `logic` — 표준 논리 (자연연역, 양화, 양상, 비형식 오류)
- `ko` — 한국어 호환 레이어 (한자말 canonical + 한말 native alias 인식)
- `cli` — 터미널 CLI + 에이전트 스킬

## What this tool is — and is not

이 도구는:

- 한국어로 들어오는 표현을 표준 논리 ID에 매핑하는 정규화 도구
- 자연어 논증을 [주장 / 전제 / 결론 / 형식화 / 사용 규칙 / 숨은 가정 / 평가]
  frame 으로 변환하는 모드 컨버터
- Lean4 / Coq 같은 실제 검증 커널과 자연어 사이의 번역 다리 (Phase 2)

이 도구가 *아닌* 것:

- 논리학 교과서가 아니다. LLM은 추론 규칙을 이미 안다. 부족한 건 표현
  좌표계의 공유 계약이다.
- 특정 저자의 고유 기호 체계를 검산하는 도구가 아니다. 그런 작업은 해당
  체계의 정의·공리·추론 규칙을 따로 명시한 별도 도구가 필요하다. 이
  도구는 표준 논리 어휘의 한국어 호환에 한정한다.
- 형식 증명 자동화 엔진이 아니다. 검증은 Lean / Coq 같은 외부 커널이 한다.

## Design Principles

### 표준 어휘에 고정한다

- canonical은 한국 학계에서 통용되는 한자말 표준 용어 + 영어 + 표준 기호.
- 한말 (이고/이거나/이면/...) 은 김명석 『두뇌보완계획100』 계열의 한국어
  토착화 작업에서 온 것. 한국어 논리 어휘를 의도적으로 재구성하려 한 시도다.
- 응답 언어로는 한자말 + 기호를 쓴다. 이유: LLM 사전훈련 분포에서 한자말과
  영어 표준 용어가 가장 잘 학습되어 있어 통신 안정성이 높다. 이건 어휘의
  가치 평가가 아니라 도구의 호환성 선택이다.
- 한말 매핑은 `native_aliases` 로 보존해 입력 인식과 옛 한국어 노트 검색
  호환을 살린다.

### 형식 타당성과 사실 참을 분리한다

- 형식적으로 타당한 추론과 사실로 건전한 추론은 다르다.
- 응답에서 두 가지를 별개로 평가한다.
- 사실 검토를 안 했다면 "건전성 평가 불가"로 명시한다.

### 검증 커널과 대화 도구를 분리한다

- Lean / Coq 는 **검증 커널**.
- 이 도구는 자연어 → 형식 표기 **번역 후보**를 제시.
- 실제 커널 호출 없이 "검증됨"이라 절대 말하지 않는다.
- Phase 2에서 실제 mathlib4 호출 bridge를 구현할 때까지는 cheat sheet 수준
  매핑만 제공한다.

### Single source of truth

- vocab/core.yaml, vocab/fallacies.yaml 이 유일한 어휘 사전.
- references/ 의 markdown은 사람이 읽기 위한 cheat sheet — 어휘는 vocab에서.
- 어휘 변경은 vocab에서 → CLI 등 다른 곳은 vocab을 읽는다.

### Data over docstrings

- 어휘는 데이터 (YAML). 코드 안에 하드코딩하지 않는다.
- 새 어휘 추가 = YAML 항목 추가 + 테스트 케이스 추가.
- 새 도메인 추가 = 새 vocab 파일 + ID 네임스페이스 추가.

## Directory Layout

```
logickocli/
  SKILL.md             # 에이전트 스킬 진입점
  AGENTS.md            # 이 파일 — 담당자 호출용
  README.md            # 외부 사용자 대상
  NEXT.md              # 다음 작업 닻 (휘발성)

  vocab/
    core.yaml          # 표준 논리 어휘 (PROP/PRED/META/SEM/LEX/RULE 도메인)
    fallacies.yaml     # 형식·비형식 오류 카탈로그
    raw.json           # 원자료 audit

  references/
    inference-rules.md # 자연연역 + 술어 + 치환규칙 카드
    modal-systems.md   # K/T/S4/S5/GL cheat sheet
    argument-frame.md  # 분석 출력 frame 명세

  scripts/
    extract_org_table.py  # 가든 노트 → raw.json 재추출

  tests/
    normalization.yaml    # 입력 표현 → ID 매핑 기대값
    argument-analysis.yaml # 자연어 논증 → 구조화 결과 기대값
```

Phase 2에서 추가될 예정:

```
  bridges/
    lean.md / lean.py    # Lean4 호출
    coq.md / coq.py      # Coq 호출

  src/                   # CLI 구현 (언어 미정 — Python? Rust? Clojure?)

  bin/
    logickocli           # CLI 진입점
```

## Phase 정의

### Phase 1 (현재)
- 어휘 데이터 + 정규화 정책 + 모드 계약 + 테스트 케이스
- 데이터만 있고 CLI는 아직 없다
- 에이전트 스킬로만 작동

### Phase 2
- Lean4 bridge (mathlib4 호출, 검증 결과 자연어 설명)
- Coq bridge (선택)
- CLI 구현 — 언어/패키징 결정 필요
- `logickocli normalize`, `logickocli analyze`, `logickocli verify --lean4` 등

### Phase 3
- 양상논리 vocab 확장 (현재는 references cheat sheet만)
- philosophy_glossary 통합
- 다국어 (영어 사용자 대상)
- nix flake 등 패키징

## 담당자에게

이 리포의 담당자(entwurf)로 호출되면 다음을 우선으로 한다:

1. **NEXT.md 부터 읽는다.** 다음 작업의 닻이 거기 있다.
2. **vocab 수정 시 항상 tests/ 도 같이 본다.** 어휘 ID 바뀌면 테스트도 갱신.
3. **응답 언어 정책을 지킨다.** native_aliases는 인식 입력으로만 다루고
   응답에는 한자말 + 기호. 김명석 두뇌보완계획100 어휘는 옛 노트 검색
   호환과 입력 인식을 위해 보존한다 — 이는 그 작업의 가치를 인정한다는
   뜻이고, 동시에 이 도구의 호환성 선택을 명시한다는 뜻이기도 하다.
4. **검증되지 않은 증명을 검증된 것처럼 말하지 않는다.** Phase 2 bridge가
   완성되기 전까지 Lean/Coq 호출은 "번역 후보"로만 제시한다.
5. **GLG에게 커밋 결정권을 남긴다.** 분신은 변경을 준비하고, 최종 커밋은
   GLG가 한다.

## 데이터 출처

- 원천 vocab: `~/sync/org/notes/20230617T120300--용어-말꼴-배움낱말-테이블`
  (142행, 영어/한자말/한말 3열, Denote/org-mode)
- 가든 공개본: <https://notes.junghanacs.com>
- 한말 어휘 출처: 김명석 『두뇌보완계획100』 (한국어 논리 어휘 토착화 작업)
- 표준 한자말 / 영어 / 기호: 한국 학계 통용 학술용어 + 표준 분석철학 교재
  (Hurley, Bergmann, 이병덕 등)
- 오류 카탈로그: 표준 분석철학·비판적 사고 교재
