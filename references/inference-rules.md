# 추론 규칙 카드 — 자연연역

문장논리·술어논리 표준 자연연역 규칙. canonical 한국어 + 영어 + 기호.
한말(이고 없애기, 차근차근 이끌기 등)은 응답에서 사용하지 않는다.

## 문장논리 도입·제거 규칙

| ID | canonical_ko | English | 기호 | schema |
|---|---|---|---|---|
| PROP.CONJ_INTRO | 연언 도입 | conjunction introduction | ∧I | A, B ⊢ A ∧ B |
| PROP.CONJ_ELIM | 연언 제거 | conjunction elimination | ∧E | A ∧ B ⊢ A; A ∧ B ⊢ B |
| PROP.DISJ_INTRO | 선언 도입 | disjunction introduction (addition) | ∨I | A ⊢ A ∨ B |
| PROP.DISJ_ELIM | 선언 제거 | disjunction elimination, disjunctive syllogism | ∨E | A ∨ B, ¬A ⊢ B; A ∨ B, A → C, B → C ⊢ C |
| PROP.IMP_INTRO | 조건문 도입 | conditional proof | →I | [A] ⋯ B ⊢ A → B |
| PROP.MODUS_PONENS | 전건긍정, 조건문 제거 | modus ponens | MP, →E | A, A → B ⊢ B |
| PROP.MODUS_TOLLENS | 후건부정 | modus tollens | MT | A → B, ¬B ⊢ ¬A |
| PROP.HYPOTHETICAL_SYLLOGISM | 가언 삼단논법 | hypothetical syllogism | HS | A → B, B → C ⊢ A → C |
| PROP.RAA | 귀류법, 간접증명 | reductio ad absurdum | RAA, ¬I | [¬A] ⋯ ⊥ ⊢ A |
| PROP.DN_ELIM | 이중부정 제거 | double negation elimination | DNE | ¬¬A ⊢ A |
| PROP.ARGUMENT_BY_CASES | 경우에 의한 증명, 양도논법 | argument by cases | — | A ∨ B, A → C, B → C ⊢ C |

## 술어논리 양화 규칙

| ID | canonical_ko | English | 기호 | schema |
|---|---|---|---|---|
| PRED.FORALL_INTRO | 보편 일반화 | universal generalization | ∀I, UG | P(a) ⊢ ∀x P(x)  (a arbitrary) |
| PRED.FORALL_ELIM | 보편 예화 | universal instantiation | ∀E, UI | ∀x P(x) ⊢ P(a) |
| PRED.EXISTS_INTRO | 존재 일반화 | existential generalization | ∃I, EG | P(a) ⊢ ∃x P(x) |
| PRED.EXISTS_ELIM | 존재 예화 | existential instantiation | ∃E, EI | ∃x P(x), [P(a)] ⋯ C ⊢ C  (a fresh) |
| PRED.QUANTIFIER_EXCHANGE_UNIV | 보편양화사 교환규칙 | universal quantifier exchange | — | ¬∀x P(x) ≡ ∃x ¬P(x) |
| PRED.QUANTIFIER_EXCHANGE_EXIST | 존재양화사 교환규칙 | existential quantifier exchange | — | ¬∃x P(x) ≡ ∀x ¬P(x) |

## 치환 규칙 (equivalence rules)

치환 규칙은 sequent 양방향으로 적용 가능하며, 부분식에도 적용된다.

| ID | canonical_ko | schema |
|---|---|---|
| RULE.DEMORGAN_CONJ | 연언 드 모르간 규칙 | ¬(A ∧ B) ≡ ¬A ∨ ¬B |
| RULE.DEMORGAN_DISJ | 선언 드 모르간 규칙 | ¬(A ∨ B) ≡ ¬A ∧ ¬B |
| RULE.COMM_CONJ | 연언 교환규칙 | A ∧ B ≡ B ∧ A |
| RULE.COMM_DISJ | 선언 교환규칙 | A ∨ B ≡ B ∨ A |
| RULE.ASSOC_CONJ | 연언 결합규칙 | (A ∧ B) ∧ C ≡ A ∧ (B ∧ C) |
| RULE.ASSOC_DISJ | 선언 결합규칙 | (A ∨ B) ∨ C ≡ A ∨ (B ∨ C) |
| RULE.DIST_CONJ | 연언 배분규칙 | A ∧ (B ∨ C) ≡ (A ∧ B) ∨ (A ∧ C) |
| RULE.DIST_DISJ | 선언 배분규칙 | A ∨ (B ∧ C) ≡ (A ∨ B) ∧ (A ∨ C) |
| RULE.TRANSPOSITION | 대우 | A → B ≡ ¬B → ¬A |
| RULE.EXPORTATION | 추출규칙 | (A ∧ B) → C ≡ A → (B → C) |
| RULE.CONDITIONAL_EXCHANGE | 조건규칙 | A → B ≡ ¬A ∨ B |
| RULE.CONJ_TAUT | 연언 동어반복 | A ∧ A ≡ A |
| RULE.DISJ_TAUT | 선언 동어반복 | A ∨ A ≡ A |

## 잘 혼동되는 항목

- **modus ponens vs affirming the consequent**: MP는 `A → B, A ⊢ B` (타당). 후건긍정은 `A → B, B ⊢ A` (부당). 후건에서 전건을 끌어내면 오류다.
- **modus tollens vs denying the antecedent**: MT는 `A → B, ¬B ⊢ ¬A` (타당). 전건부정은 `A → B, ¬A ⊢ ¬B` (부당).
- **귀류법 vs 이중부정 제거**: 직관주의 논리에서는 RAA의 강한 형태(¬¬A ⊢ A)가 일반적으로 인정되지 않는다. 고전 논리에서는 둘 다 인정된다.
- **함축(implication)의 두 표기**: 대상언어의 `→` (조건문)과 메타언어의 `⊨` / `⊢` (논리적 함축, 증명가능성)은 다른 것이다.
