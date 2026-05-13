# vocab schema

`core.yaml` 과 `fallacies.yaml` 항목의 필드 명세. 새 어휘를 추가하거나
정규화 로더를 작성할 때 이 문서를 기준으로 한다.

## 항목 골격

```yaml
- id: DOMAIN.NAME            # 필수
  domain: propositional_logic # 필수 (core.yaml만)
  kind: inference_rule       # 필수 (core.yaml만)
  canonical_ko: ...          # 필수
  en: [...]                  # 권장
  symbol: [...]              # 선택
  aliases_ko: [...]          # 선택
  native_aliases: [...]      # 선택
  schema: [...]              # 선택 — 추론/치환 규칙의 형식 표기
  parts: {...}               # 선택 — 부분 개념 (예: 조건문의 전건/후건)
  note: "..."                # 선택 — 출처·주의·맥락
  explanation_ko: "..."      # fallacies.yaml 전용
  subtype: relevance         # fallacies.yaml 전용
```

## 필드별 규약

### `id` (필수, 문자열)

`DOMAIN.SHORTNAME` 형태. 대문자 + 언더스코어. ID는 가든 노트들과 ID 기반으로
연결되므로 변경에 신중해야 한다.

- `PROP.*` — 명제논리 (propositional logic)
- `PRED.*` — 술어/양화 논리
- `META.*` — 메타논리 (논증·타당성·건전성 등)
- `SEM.*` — 문장·구문·의미론 범주
- `LEX.*` — 어휘 범주 (단어·명사·정의 등 — 논리 도구 범위를 넘는 부분도 포함)
- `RULE.*` — 도출된 치환·동치 규칙
- `FALLACY.*` — 오류 카탈로그 (`fallacies.yaml`)

### `canonical_ko` (필수, string 또는 list)

표준 한자말 학술용어. **두 가지 타입을 모두 허용한다.**

- string: 단일 canonical (예: `canonical_ko: 부정`)
- list: 동의어 묶음, 첫 항목이 primary (예: `canonical_ko: [연언 제거, 단순화논법]`)

로더는 항상 list로 normalize 한다:

```python
def as_list(v): return [v] if isinstance(v, str) else (v or [])
```

응답 표면에는 list의 첫 항목을 기본으로 쓰되, 사용자가 다른 항목으로 입력했으면 그 항목을 우선해도 된다.

### `en` (권장, list)

영어 표준어. 첫 항목이 primary. 약어나 별칭은 뒤에 둔다.

### `symbol` (선택, list)

표준 기호. 유니코드 우선 (`→`, `∧`, `∀`, `□`). ASCII 대체(`->`, `&`)는 입력 인식용이지 응답 표면용이 아니다.

### `aliases_ko` (선택, list)

같은 한자말 계열의 별칭/유의어. 예: `META.PREMISE.aliases_ko: [근거, 논거, 가정]`.

### `native_aliases` (선택, list)

한말 어휘 — 김명석 『두뇌보완계획100』 계열의 한국어 학문어휘 토착화 작업에서 온 어휘를 주로 보존한다. **인식 입력으로만 다루며 응답에 등장하지 않는다** — 이건 어휘 가치 평가가 아니라 도구의 호환성 선택이다.

### `schema` (선택, list of strings)

추론·치환 규칙의 형식 표기. 시퀀트 표기 사용:

- `A, B ⊢ A ∧ B` — 추론
- `¬(A ∧ B) ≡ ¬A ∨ ¬B` — 등가
- `[A] ⋯ B ⊢ A → B` — 가정 도입 (대괄호 = discharge)

### `parts` (선택, dict)

복합 개념의 부분. 각 부분도 `canonical_ko` / `en` / `native_aliases` 를 가질 수 있다. 예: `PROP.CONDITIONAL.parts.antecedent`.

### `note` (선택, 문자열)

출처 표시, 표준 정의 인용, 또는 주의사항. 평가적 표현 없이 사실 진술로.

## 정규화 정책

### Alias 충돌 — 의도된 것과 정리할 것

같은 문자열이 여러 ID에 잡히는 경우가 있다. 두 부류로 나눈다.

**의도된 충돌** (`scripts/check_vocab.py` 가 화이트리스트로 인정). ID 쌍 4개, surface 문자열 5건 — 한 ID 쌍에서 한자말·한말 두 표면이 겹칠 수 있다:

- `PROP.CONDITIONAL ⇄ SEM.CONDITIONAL_SENTENCE` — connective (≡ 추상 연산자) 와 sentence (≡ 그 연산자로 이루어진 문장) 가 같은 한국어를 공유.
- `PROP.BICONDITIONAL ⇄ SEM.BICONDITIONAL_SENTENCE` — 동일 사유.
- `PROP.BICONDITIONAL ⇄ META.LOGICAL_EQUIVALENCE` — 기호 `≡` 가 대상언어(쌍조건)와 메타언어(논리적 동치) 양쪽에서 쓰임. `references/inference-rules.md` 의 "잘 혼동되는 항목" 단락에 이미 주의가 있다.
- `META.PREMISE ⇄ META.ASSUMPTION` — `'가정'` 이 둘 모두에 해당. 입력이 `'가정'` 일 때 **기본 META.ASSUMPTION** 으로 가되, 명백한 논증 맥락이면 META.PREMISE.

**정리할 충돌** — 발견 시 vocab을 손본다. 화이트리스트에 넣지 않는다.

### 입력 인식 우선순위

1. 정확 일치 (`symbol`, `en`, `canonical_ko`, `aliases_ko`, `native_aliases` 순)
2. 대소문자 무시 (영어만)
3. 공백 정규화 (`연언제거` → `연언 제거`)

## 새 항목 추가 절차

1. 적절한 도메인 / ID 네임스페이스 선택.
2. `vocab/core.yaml` 또는 `vocab/fallacies.yaml` 의 해당 도메인 섹션에 추가.
3. `tests/normalization.yaml` 또는 `tests/argument-analysis.yaml` 에 테스트 케이스 추가.
4. `python3 scripts/check_vocab.py` 로 충돌·통계 확인.
5. 필요시 `references/*.md` cheat sheet 동기화.

ID 자체의 변경(rename)은 가능한 한 피한다. 가든 노트들이 ID로 참조한다.
