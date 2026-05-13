---
name: logickocli
description: "Korean structured-reasoning prelude. Loads a shared logic coordinate system (standard Korean / English / symbolic) so the agent and the user reason in the same vocabulary. Use when the user makes a logical claim, argues, asks to check validity, asks about inference rules, formal/informal fallacies, modal/quantifier logic, or wants Korean-natural-language reasoning translated into structured logical analysis."
---

# logickocli — 한국어 구조화 추론 프렐류드

이 스킬은 논리학 교과서가 아니다. **에이전트와 인간이 같은 논리 좌표계에서 대화하도록 어휘·기호·분석 포맷을 로딩하는 모드 컨버터**다.

에이전트는 이미 자연연역·양화논리·양상논리·확률·게임이론을 안다. 부족한 것은 같은 개념을 한국어와 영어와 기호 중 어느 표현으로 들어오든 같은 노드로 잡는 좌표계다. 이 스킬은 그 좌표계를 로딩한다.

## 언제 발동하는가

다음 신호가 하나 이상 있으면 이 스킬의 frame으로 응답한다.

- 사용자가 자연어로 **논증**을 펼침: "X이면 Y이고, X니까 Y다", "왜냐하면", "그러므로", "이므로", "...에 따라" 등.
- **논리 어휘**가 등장: 전제·결론·타당·건전·모순·일관·필연·가능·증명·반례·오류·논증·추론.
- 한말 어휘로 들어옴: "이고 없애기", "차근차근 이끌기", "마땅하다", "튼튼하다" 등. 매핑은 인식하되 응답은 표준어로.
- **양상** 주장: 반드시, 어쩌면, 가능, 필연, 증명할 수 있다, 반증할 수 없다.
- **오류** 검토 요청: "이게 성급한 일반화 아니야?", "후건긍정 아니야?".
- **형식 검증** 요청: "Lean으로 어떻게 쓰지?", "Coq에서는?".

발동 신호가 약하면 한 줄 요약 + "구조화 분석 원하면 알려 주세요" 식 옵트인.

## 핵심 정책

### 1. 응답 언어 — 표준 학술용어로 통일

- **canonical**: 표준 한국어 학술용어(한자말) + 기호. 영어는 필요 시 병기.
- **native_aliases**: 김명석 『두뇌보완계획100』 계열의 한말 어휘 (이고 없애기, 모든씨, 받침말 등). 한국어 논리 어휘를 토착화하려는 의도적인 작업의 결과물이며, 가든 옛 노트와의 검색 호환을 위해 vocab에 보존한다. 다만 이 도구는 LLM 사전훈련 분포에서 충분히 학습된 한자말·영어·기호로 응답해 통신 안정성을 높이는 쪽을 선택했다. 사용자가 한말로 입력하면 매핑을 인식해 표준어로 정규화한 결과를 돌려준다.

### 2. 항상 구조화

자연어 논증을 받으면 다음을 분리해서 출력한다.

1. **주장**, **전제(P1, P2, ...)**, **결론(C)** 을 분리.
2. **형식화** — 변수 할당과 함께 기호 표기. 예: `A = "비가 온다", B = "길이 젖는다"`, `P1: A → B, P2: A, C: B`.
3. **사용 규칙** — vocab/core.yaml의 ID로 식별 (예: `PROP.MODUS_PONENS`).
4. **숨은 가정** — 결론이 따라 나오기 위해 필요한, 명시되지 않은 명제.
5. **평가** — 형식적 타당성, 건전성, 비형식 오류 후보.

세부 frame은 `references/argument-frame.md` 참조.

### 3. 정규화는 ID 기반

사용자가 어떤 표현으로 들어오든 같은 ID에 묶는다.

| 입력 | 매핑되는 ID | canonical 응답 |
|---|---|---|
| "이고 없애기" | PROP.CONJ_ELIM | 연언 제거 (∧E) |
| "conjunction elimination" | PROP.CONJ_ELIM | 연언 제거 (∧E) |
| "∧E" | PROP.CONJ_ELIM | 연언 제거 (∧E) |
| "and-elim" | PROP.CONJ_ELIM | 연언 제거 (∧E) |
| "단순화 논법" | PROP.CONJ_ELIM | 연언 제거 / 단순화논법 (∧E) |

### 4. 형식 타당성 ≠ 사실 참

응답에서 두 가지를 항상 분리해서 다룬다.

- **형식 타당성**: 전제가 모두 참이라면 결론도 반드시 참인지. 이건 형식만 본다.
- **건전성**: 전제가 실제로 참인지. 이건 사실 검토가 필요. 사실 검토를 하지 않았다면 "평가 불가"로 명시.

### 5. 검증 커널과 대화 도구를 구분

Lean / Coq는 **검증 커널**이다. 이 스킬은:

- 자연어 → 형식 표기 **번역 후보**를 제시한다.
- 그러나 실제 Lean/Coq 호출 없이 "Lean에서 증명됨"이라고 말하지 않는다.
- `bridges/lean.md`·`bridges/coq.md`가 생기기 전까지는 cheat sheet 수준 매핑만 제공.

## 데이터

| 경로 | 내용 |
|---|---|
| `vocab/core.yaml` | 명제논리·술어논리·메타논리·구문·통사 어휘. ID, canonical_ko, en, symbol, aliases, native_aliases. |
| `vocab/fallacies.yaml` | 형식 오류 + 비형식 오류 카탈로그 (성급한 일반화, 결론 선취 등). |
| `references/inference-rules.md` | 자연연역 규칙 카드 (문장논리 + 술어논리 + 치환규칙). |
| `references/modal-systems.md` | K/T/S4/S5/GL cheat sheet. |
| `references/argument-frame.md` | default / proof_mode / debate_mode / modal_mode / probability_mode 출력 포맷. |
| `vocab/raw.json` | 20230617T120300 org-table에서 추출한 원자료 (audit용). |
| `scripts/extract_org_table.py` | 원자료 재추출 스크립트. |

## 사용 흐름

```
1. 입력 발화에서 논증/주장 식별
2. 표현을 vocab을 통해 canonical ID로 정규화
3. argument-frame 적용해 구조화 출력
4. 형식 타당성·비형식 오류 후보 검토
5. 양상·확률·게임이론·증명 등 모드가 필요하면 변형 frame
6. 검증 커널 필요 시 번역 후보만 제시 (검증 안 했다고 명시)
```

## 출처

- vocab 원천: `~/sync/org/notes/20230617T120300--용어-말꼴-배움낱말-테이블__dictionary_glossary_logic_orgtable.org` (142행, 3열: 영어/한자말/한말). 가든 공개본은 `notes.junghanacs.com`에 있음.
- 142행 중 중복·역방향·오탈자를 정규화해 한자말 columns을 canonical로, 한말을 native_aliases로 분리.
- fallacies는 표준 분석철학 교재 (Hurley, Bergmann, 이병덕) 기반.
- 한말 어휘 (이고/이거나/이면/...) 는 김명석 『두뇌보완계획100』 계열의 한국어 토착화 작업에서 온 것. 이 도구는 LLM 호환을 위해 한자말 + 기호로 응답하지만, 매핑은 보존해 입력 인식과 가든 옛 노트 검색 호환을 살린다.

## 한계 — 알면서 안 하는 것들

- **Lean/Coq 실제 호출**: 안 함. 번역 cheat sheet만. Phase 2에서 실제 검증 bridge 작성 예정.
- **확률·게임이론 vocab**: vocab/core.yaml에 포함하지 않음. 모드 frame은 references/argument-frame.md에 있음.
- **DSL 추론 엔진**: 형식 증명 자동화 안 함. 분석·평가만.
- **자체 기호 체계 어댑터**: 이 도구의 초점은 **표준 논리** 어휘의 한국어 호환이다. 개별 저자가 만든 자체 기호 체계 검산은 범위 밖이며, 이는 그 작업이 가치가 없어서가 아니라 이 도구의 범용성 목표와 결이 다르기 때문이다.

이 한계들은 의도된 것이고, Phase 2 이후로 미뤄둔다.
