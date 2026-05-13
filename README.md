# logickocli

> 한국어 자연어 추론 ↔ 표준 논리 좌표계 변환 도구.
> Korean ↔ standard-logic coordinate-system tool for human-agent collaboration.

`logic` + `ko` + `cli`.

## 무엇을 하는 도구인가

한국어로 논리적 사고를 할 때, 사람과 LLM 에이전트가 같은 좌표계에서
대화할 수 있어야 한다. 같은 개념을

- `이고 없애기`
- `연언 제거`
- `conjunction elimination`
- `∧E`
- `and-elim`

어느 표현으로 입력하든, 모두 같은 노드 `PROP.CONJ_ELIM` 으로 정규화한 뒤
표준 한국어 학술용어 + 기호로 응답한다.

자연어 논증을 받으면 다음 frame으로 구조화한다:

```
[주장]   사용자가 결론으로 내세우는 명제
[전제]   P1, P2, ...
[결론]   C
[형식화] 변수 할당 + 기호 표기 (A → B, A ⊢ B 등)
[사용 규칙] PROP.MODUS_PONENS / 전건긍정 / modus ponens / MP
[숨은 가정] 결론이 따라 나오기 위해 필요한, 명시되지 않은 명제
[평가]   형식적 타당성 + 건전성 + 비형식 오류 후보
```

## 예시

> 아래 두 예시는 Phase 2에서 CLI가 들어왔을 때의 입출력 모습을 미리 보여주는
> mock 이다. Phase 1 현재는 같은 분석을 `references/skill-contract.md` 가 로딩된 에이전트가 수행한다.

### 정규화

```
입력:  이고 없애기
       ↓
정규화: PROP.CONJ_ELIM
응답:  연언 제거 (∧E / conjunction elimination)
       schema: A ∧ B ⊢ A;  A ∧ B ⊢ B
```

### 자연어 논증 분석

```
입력: "비가 오면 길이 젖는다. 길이 젖었다. 그러므로 비가 왔다."

[전제]
  P1. 비가 오면 길이 젖는다
  P2. 길이 젖었다
[결론]
  C. 비가 왔다
[형식화]
  A = "비가 온다", B = "길이 젖는다"
  P1: A → B
  P2: B
  C:  A
[평가]
  형식적으로 부당.
  FALLACY.AFFIRMING_CONSEQUENT (후건긍정의 오류 / affirming the consequent)
  반례: B의 원인이 A 외에도 있을 수 있다 (스프링클러, 누수, 청소 등).
```

## 어휘 범위 (Phase 1)

| 도메인 | 항목 수 | 예시 |
|---|---|---|
| 명제논리 | 33 | 연언/선언/조건문, 자연연역 규칙, 치환규칙 |
| 술어논리 | 15 | 보편/존재 양화사, 양화 규칙, 술어/변항/상항 |
| 메타논리 | 35 | 전제·결론·논증, 타당성·건전성·일관성, 함축·동치 |
| 통사/의미 | 27 | 문장/명제/항진/항위, 진리표, 진리값 |
| 정언논리 | 5 | A/E/I/O 명제 |
| 어휘 | 6 | 단어/명사/정의/의미 |
| 인식론 | 2 | 의견·신념, 사상 |
| 형식 오류 | 3 | 후건긍정, 전건부정, 매개념 부주연 |
| 비형식 오류 | 21 | 성급한 일반화, 결론 선취, 거짓 양도논법 등 |

**총 147개 unique ID**. 수치는 `python3 scripts/check_vocab.py` 로 검증된다.

## 데이터 출처와 정책

- 어휘 원천: 디지털 가든의 Denote 노트 `20230617T120300` (142행, 영어/한자말/한말 3열).
- 한자말(`canonical`): 한국 학계 통용 학술용어. 응답 언어로 사용.
- 한말(`native_aliases`): 김명석 『두뇌보완계획100』 계열의 한국어 토착화
  작업에서 온 어휘. 한국어로 논리 개념을 의도적으로 재구성한 시도다. 이
  도구는 LLM 호환을 위해 한자말 + 기호로 응답하지만, 한말 매핑을 보존해
  입력 인식과 옛 한국어 노트 검색 호환을 살린다.
- 오류 카탈로그: 표준 분석철학 교재 (Hurley, Bergmann, 이병덕 등) 기반.

## 관련 작업에 대한 인정

한국어 논리 어휘를 둘러싼 시도는 여러 갈래로 진행되어 왔다.

- 학계 표준 한자말 학술용어 (선우환·이병덕·최훈·박병철 등)
- 김명석 『두뇌보완계획100』 의 한말 토착화 어휘 (이고/이거나/이면/...)
- Coq 한국어 자료 (박성우, 정주희)
- 디지털 가든의 누적된 어휘 실험

이 도구는 그중 어느 하나를 평가하거나 대체하지 않는다. *범용 LLM 에이전트와
한국어 사용자가 같은 논리 좌표계에서 대화한다*는 좁은 목표를 위해 한자말 +
영어 + 기호 표준에 정렬했을 뿐이다. 한말 토착화 작업의 의도(한국어 학문어휘
재구성)와 가치는 그것대로 별도의 의의가 있다.

## 상태 — Phase 1

현재는 데이터 + 어휘 정규화 정책 + 분석 frame 명세 + 테스트 케이스만
정비되어 있다. CLI 바이너리는 Phase 2에서 구현 예정.

### Phase 2 예정

- Lean4 bridge — 자연어 → Lean4 형식화 + mathlib4 호출 + 검증 결과 자연어 설명
- Coq bridge (선택)
- CLI 구현 — `logickocli normalize`, `logickocli analyze`, `logickocli verify` 등
- 양상논리 vocab 확장

### Phase 3 예정

- philosophy_glossary 통합
- 다국어 (영어 사용자)
- 패키징 (nix flake 등)

## 파일 구조

```
AGENTS.md                  # 담당자(분신) 호출용
README.md                  # 이 파일
NEXT.md                    # 다음 작업 닻

vocab/
  core.yaml                # 표준 논리 어휘
  fallacies.yaml           # 오류 카탈로그
  SCHEMA.md                # 필드 명세 + alias 충돌 정책
  raw.json                 # 원자료 audit

references/
  skill-contract.md        # 에이전트 모드 계약 본문 (호스트 SKILL.md가 참조)
  inference-rules.md       # 자연연역 + 술어 + 치환규칙
  modal-systems.md         # K/T/S4/S5/GL cheat sheet
  argument-frame.md        # 분석 출력 frame 명세

scripts/
  extract_org_table.py     # 원자료 재추출
  check_vocab.py           # vocab 자가 검증

tests/
  normalization.yaml       # 입력 → ID 매핑 케이스
  argument-analysis.yaml   # 자연어 논증 분석 케이스
```

## 사용 (현재)

CLI 미구현. 어휘 데이터를 직접 읽거나 에이전트 스킬로 호출.

### 어휘 조회

```bash
python3 -c "
import yaml
core = yaml.safe_load(open('vocab/core.yaml'))
for e in core['entries']:
    if 'CONJ_ELIM' in e['id']:
        print(e)
"
```

### 자가 검증

```bash
python3 scripts/check_vocab.py
# 항목 수, 도메인 분포, alias 충돌(의도된 것/정리할 것) 보고
# 미해결 충돌·스키마 누락·dangling test ID 있으면 exit 1
```

### 원자료 재추출

```bash
python3 scripts/extract_org_table.py
# → vocab/raw.json 생성
# 원본은 ~/sync/org/notes/20230617T120300--... 또는 ~/org/notes/... 둘 다 탐색.
```

### 에이전트 스킬 (Claude Code / pi-shell-acp / Codex)

호스트 환경의 스킬 디렉터리에 짧은 `SKILL.md` 를 두고 본문을 이 리포의
`references/skill-contract.md` 로 참조시키면 모드 계약이 로딩되어 한국어
자연어 추론 대화가 구조화된다. logickocli 리포 자체에는 호스트별 SKILL.md
를 두지 않는다 — 모드 계약 본문(`references/skill-contract.md`) 과 데이터만
SSOT 로 유지한다.

## License

MIT (예정 — LICENSE 파일 추가 시 확정).

## 기여

Phase 1 어휘 정비 + Phase 2 bridge 설계 단계. 이슈 / PR 환영하나, 어휘
canonical 변경은 사용 중인 노트·도구와의 호환성 검토 후 신중히 진행한다.
