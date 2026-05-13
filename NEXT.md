# NEXT — logickocli

> 휘발성. 다음에 할 일을 잡아두는 닻. 영속할 사실은 AGENTS.md / docs / commit
> history로 옮긴다.

## 지금 상태 (2026-05-13)

- Phase 1 끝. 어휘 데이터 + 정규화 정책 + 분석 frame + 테스트 케이스만 있음.
- 어휘 147개 unique ID, 8개 도메인.
- CLI 바이너리 없음. 에이전트 스킬로만 작동.
- 첫 외부 공개 직전 (GitHub 리포 생성 + 초기 커밋).

## 다음 한 걸음

### 1. 한 turn 실사용 검증

- agent-config 또는 logickocli SKILL.md를 로드한 세션에서 실제 한국어 논증
  대화를 한 turn 돌려보고, frame이 자연스럽게 적용되는지 본다.
- 안 맞는 부분이 있으면 references/argument-frame.md 를 조정한다.

### 2. CLI 인터페이스 spec 초안

다음 명령 후보를 spec 문서로 정리:

```
logickocli normalize <expression>
logickocli analyze <argument-text>
logickocli formalize <korean-sentence> --target propositional|predicate|modal
logickocli vocab list [--domain <name>]
logickocli rule lookup <id-or-symbol>
logickocli verify <argument> --lean4   # Phase 2
```

남은 결정:

- 구현 언어: Python (어휘 YAML 다루기 쉬움) vs Rust (배포·속도) vs Clojure
  (abductcli와 결 맞음, EDN/JSON 친화) vs TypeScript (Node 생태계)
- 데이터 인덱싱: YAML 직접 로드 (단순) vs SQLite (검색 빠름, 인덱스 가능)
- 출력 포맷: human(컬러) / json / yaml
- subcommand 라이브러리 선택

### 3. Lean4 bridge 프로토타입

- 단순 예제 5개로 시작: `A → B, A ⊢ B` 등을 Lean4 코드로 변환 + lean
  binary 호출 + 결과 파싱.
- mathlib4 dependency 처리 방식 결정.
- 검증 안 된 자연어 응답과 검증된 결과를 출력에서 명확히 구분하는 표시.

### 4. 자가 검증 강화

- tests/normalization.yaml 케이스를 자동 실행하는 작은 러너 스크립트
  (script로 작성, 일단 Python).
- vocab 변경 시 native_aliases가 중복되거나 충돌하는지 검사.

## 보류 중인 결정

- **데이터 형식**: YAML 유지 vs SQLite 마이그레이션 (CLI 검색 성능 따라).
- **다국어 (i18n)**: 영어 사용자도 쓸 수 있게 하면 abductcli·denotecli 톤과
  맞고 GitHub 노출에 유리. 한국어 전용으로 가면 포지셔닝이 명확.
- **패키징**: nix flake (개인 환경 우선) / PyPI (외부 접근성) / Homebrew.
- **license**: MIT 추정이지만 LICENSE 파일 추가 시 확정.
- **양상논리 vocab 확장**: 가든에 자료가 없어 새로 짜야 함. Phase 2와
  bundle 할지 별도로 할지.

## Phase 2에서 손대지 말 것

- 김명석 사적 양상 체계 어댑터 (의도적으로 범위 밖).
- 한말 어휘 응답 표면화 (canonical 한자말 + 기호 정책 유지).
- 형식 증명 자동화 엔진 (검증은 Lean/Coq 커널이 한다 — 우리는 다리만).

## 관련 노트

- 설계 논의: 가든 botlog `20260513T103033` —
  "structured-reasoning-ko 스킬 설계와 CLI 공개 로드맵"
- 어휘 원천: 가든 노트 `20230617T120300`
- agent-config 원본: `~/repos/gh/agent-config/skills/structured-reasoning-ko/`
  (현재는 logickocli로 이관, agent-config 쪽 처리 방식은 별도 결정)
