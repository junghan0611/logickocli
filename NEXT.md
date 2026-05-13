# NEXT — logickocli

> 휘발성. 다음에 할 일을 잡아두는 닻. 영속할 사실은 AGENTS.md / docs / commit
> history로 옮긴다.

## 지금 상태 (2026-05-13)

- Phase 1 어휘·계약·테스트·자가 검증 러너까지 정비됨.
- 어휘 147개 unique ID, 9개 도메인 (`scripts/check_vocab.py` 로 항상 검증 가능).
- alias 충돌: 의도된 5건 (`vocab/SCHEMA.md` 화이트리스트), 정리된 2건.
- CLI 바이너리 없음. 에이전트 스킬로만 작동.
- 첫 외부 공개 직전 (GitHub 리포 생성 + 초기 커밋 + 본 정비 commit).

## 다음 한 걸음

### 1. 모드 계약 한 turn 실사용 검증

- 호스트 SKILL.md (예: agent-config/skills/logickocli/SKILL.md) 가 이 리포의
  `references/skill-contract.md` 를 참조해 로드된 세션에서 실제 한국어 논증
  대화를 한 turn 돌려보고, frame 이 자연스럽게 적용되는지 본다.
- `tests/argument-analysis.yaml` 의 케이스 한두 개를 자연어 입력으로 던져
  `expect_must_identify` 항목이 실제 응답에 등장하는지 손으로 확인.
- 어색하면 `references/argument-frame.md` 를 조정.

### 2. normalize() 프로토타입 — 정규화의 실제 코드화

`scripts/check_vocab.py` 는 무결성 검사이고, 입력 표현 → ID 정규화는 아직
없다. Phase 2 CLI 진입 전 닻으로 다음 형태의 작은 함수 하나가 필요하다:

```python
def normalize(expr: str) -> list[CandidateMatch]:
    """입력 표현 → 후보 ID 리스트 (우선순위 정렬).
    SCHEMA.md '입력 인식 우선순위' 정책에 따른다.
    의도된 alias 충돌(예: '가정')은 후보 다중 반환 + disambiguation hint.
    """
```

이게 들어가면 `tests/normalization.yaml` 의 `inputs` → `expect_id` 매핑이
자동 회귀가 된다. 언어는 Python (vocab 로더와 같은 자리).

### 3. CLI 인터페이스 spec 초안

다음 명령 후보를 spec 문서로 정리:

```
logickocli normalize <expression>
logickocli analyze <argument-text>
logickocli formalize <korean-sentence> --target propositional|predicate|modal
logickocli vocab list [--domain <name>]
logickocli rule lookup <id-or-symbol>
logickocli verify <argument> --lean4   # Phase 2
```

남은 결정 (현재 단계에서는 결정하지 않고 데이터 패턴 더 보고 결정):

- 구현 언어: Python (어휘 YAML 다루기 쉬움, 자가 검증 러너와 같은 자리) vs
  Rust (배포·속도) vs Clojure (abductcli와 결 맞음) vs TypeScript.
- 데이터 인덱싱: YAML 직접 로드 vs SQLite.
- 출력 포맷: human(컬러) / json / yaml.

### 4. Lean4 bridge 프로토타입

- 단순 예제 5개로 시작: `A → B, A ⊢ B` 등을 Lean4 코드로 변환 + lean
  binary 호출 + 결과 파싱.
- mathlib4 dependency 처리 방식 결정.
- 검증 안 된 자연어 응답과 검증된 결과를 출력에서 명확히 구분하는 표시.

## 이번 정비에서 처리한 것

(다음 turn에 다시 들지 않도록 기록)

- vocab 항목 수 정합 — README 표에 epistemology 누락분 추가, 합계 147 검증.
- canonical_ko 필드의 string/list 타입 가변성 → `vocab/SCHEMA.md` 에 명시.
- alias 충돌 — 의도된 5건 화이트리스트화, 정리할 2건(`LEX.TERM`의 '명사',
  `META.CONCLUSION_INDICATOR` 의 단독 '따름말') 수정.
- `scripts/extract_org_table.py` 경로 fallback (`~/sync/org/` / `~/org/`).
- README 예시 두 개에 Phase 1 mock 임을 명시.
- `scripts/check_vocab.py` 신설 — 항목 수 / 도메인 / 충돌 / 스키마 / dangling
  test ID 자동 검사. `--json` 출력 지원.

## 보류 중인 결정

- **데이터 형식**: YAML 유지 vs SQLite 마이그레이션 (CLI 검색 성능 따라).
- **다국어 (i18n)**: 영어 사용자도 쓸 수 있게 하면 abductcli·denotecli 톤과
  맞고 GitHub 노출에 유리. 한국어 전용으로 가면 포지셔닝이 명확.
- **패키징**: nix flake (개인 환경 우선) / PyPI (외부 접근성) / Homebrew.
- **license**: LICENSE 파일 추가됨 (MIT). README 표현 정합 점검만 남음.
- **양상논리 vocab 확장**: 가든에 자료가 없어 새로 짜야 함. Phase 2와
  bundle 할지 별도로 할지.

## Phase 2에서 손대지 말 것

- 외부 저자의 자체 기호 체계 어댑터 (의도적으로 범위 밖).
- 한말 어휘 응답 표면화 (canonical 한자말 + 기호 정책 유지).
- 형식 증명 자동화 엔진 (검증은 Lean/Coq 커널이 한다 — 우리는 다리만).

## 관련 노트

- 설계 논의: 가든 botlog `20260513T103033` —
  "structured-reasoning-ko 스킬 설계와 CLI 공개 로드맵"
- 어휘 원천: 가든 노트 `20230617T120300`
- agent-config 원본: `~/repos/gh/agent-config/skills/structured-reasoning-ko/`
  (현재는 logickocli로 이관, agent-config 쪽 처리 방식은 별도 결정)
