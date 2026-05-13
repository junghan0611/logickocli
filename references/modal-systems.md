# 양상논리 cheat sheet — K · T · S4 · S5 · GL

문장논리에 양상 연산자 □(필연), ◇(가능)를 더한 체계. 이 스킬은 표준 양상논리
어휘를 응답에서 직접 쓸 수 있도록 cheat sheet 형태로 둔다. 별도 vocab CSV는
만들지 않는다.

## 기본 연산자

| 기호 | canonical_ko | English | 정의 |
|---|---|---|---|
| □A | 필연적으로 A | necessarily A | A is necessary |
| ◇A | 가능하게 A | possibly A | ¬□¬A |

자연어 매핑:

- "반드시 A다" → □A
- "A일 수 있다" / "가능하다" → ◇A
- "A가 반증되지 않는다" → ◇A (≡ ¬□¬A)

## 체계 비교

| 체계 | 공리 (K 위에 더해지는 것) | frame condition | 비고 |
|---|---|---|---|
| K | □(A → B) → (□A → □B) | — | 모든 normal modal logic의 기저 |
| T | □A → A | reflexive | "필연이면 실제로 그러하다" |
| S4 | □A → □□A | reflexive + transitive | T를 확장. 인식논리 후보 |
| S5 | ◇A → □◇A | equivalence | S4를 확장. 형이상학적 필연성 |
| GL | □(□A → A) → □A | converse well-founded, transitive | 증명가능성 논리 (provability logic) |

## 추론 규칙

모든 normal modal logic의 공통 규칙:

- **Modus Ponens (MP)**: `A, A → B ⊢ B`
- **Necessitation (Nec)**: `⊢ A   ⇒   ⊢ □A`
  (정리로서 도출된 A에 □를 붙일 수 있다. 가정에서 도출된 A는 안 됨.)
- **Uniform substitution**: 명제변수 치환은 닫힌 정리에서 가능.

## 자주 마주치는 등가

- ◇A ≡ ¬□¬A
- □A ≡ ¬◇¬A
- □(A ∧ B) ≡ □A ∧ □B
- ◇(A ∨ B) ≡ ◇A ∨ ◇B
- □A → ◇A   (T 이상에서)
- □A → A    (T 이상에서)
- □A → □□A  (S4 이상에서)

## 주의 — 증명가능성과 양상의 구분

**T의 □A → A**는 강한 반성 원리(strong reflection)다. 자연어로는 "증명 가능하면 참이다"처럼 들리지만, 산술에서의 *증명가능성 술어* Prov_T(⌜A⌝)에 그대로 적용하면 위험하다.

- 임의의 충분히 강한 T에 대해 □A → A를 T 내부에서 보편적으로 받아들이면 일관성을 잃기 쉽다 (Löb's theorem).
- 산술의 증명가능성 논리는 보통 **GL** (Gödel–Löb): `□(□A → A) → □A`.
- 따라서 "X는 증명할 수 있다"를 S4 또는 T 안에서 □로 다루는 것과, "X는 산술체계 T에서 증명할 수 있다"를 Prov_T로 다루는 것은 다른 일이다.

## Lean / Coq에서의 양상

mathlib4 등 주류 증명보조기에는 GL, S4, S5 등의 양상논리 형식화가 일부 존재하지만, 사용자 자연어 양상 주장을 그대로 mathlib 정리로 번역하기는 어렵다. 일반적으로:

- 사용자 양상 주장 → 표준 □/◇ 식으로 정규화
- 체계 식별 (K? T? S4? S5? GL?)
- 그 체계의 알려진 정리/반례를 reference
- mathlib 형식화는 옵션, 보통은 자연어 검토 + 표준 양상 의미론(Kripke frames)에서 검증
