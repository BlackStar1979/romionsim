# ROMION - PRIORYTETOWY PLAN DZIAŁANIA (Post-Kontrola GPT)

**Data:** 2026-01-10  
**Bazowane na:** Ocena kontrolna GPT + Audit GPT (48 punktów)  
**Status:** STRATEGIA ZATWIERDZONA

---

## 🎯 KLUCZOWE PRZESŁANIE Z OCENY KONTROLNEJ

> **"Twoja praca idzie w dobrym kierunku."**
> 
> **"To NIE jest kosmetyka. To jest realne ustabilizowanie teorii."**
> 
> **Na tym etapie:**
> - ❌ NIE poprawiaj jeszcze agresywnie kodu
> - ✅ DOKOŃCZ kontrakty (logi + metryki)
> - ✅ Traktuj repo jak "system epistemiczny", nie "silnik fizyki"

---

## ✅ CO ZOSTAŁO OSIĄGNIĘTE (70-75% Success)

### 1. Przestawienie repo na tryb epistemiczny ✅
**Status:** DONE (największy sukces!)

**Evidence:**
- THEORY.md v2.0: CORE/FRACTURE/INTERPRETATION explicit
- METHODOLOGY.md v2.0: No backreaction language
- Archive cleanup: DEPRECATED notices
- RANGE=2 retraction v2.0
- Language shift: "observed" not "exists"

**Impact:** **Dryf filozoficzny ZATRZYMANY**

### 2. Archiwizacja fałszywych "finalności" ✅
**Status:** DONE

**Evidence:**
- `*_COMPLETE.md` → archive/
- Historical context added
- "Skończone" nie oznacza "teorii complete"

**Impact:** Repo nie udaje że jest "done"

### 3. Wyraźne rozdzielenie: analiza ≠ teoria ✅
**Status:** DONE

**Evidence:**
- gravity_test: instrument epistemiczny
- No "dowodów pola"
- No "potwierdzeń grawitacji"
- Ostrożny język statystyczny

**Impact:** Analiza poprawnie interpretowana

---

## ⚠️ CO JEST CZĘŚCIOWO (30% Remains - PRIORITY)

### 1. KROK 2: Kontrakt logów (ROZPOCZĘTY nie ZAMKNIĘTY)

**✅ Co jest:**
- LOG_SCHEMA_V2.md (dokumentacja)
- MIGRATION_V1_TO_V2.md (plan)
- Dużo refleksji, audytów, statusów

**❌ Co brakuje (CRITICAL):**
> "Brak JEDNEGO kanonicznego kontraktu w stylu:
> 'Od tej wersji tick log wygląda tak, a nie inaczej – 
> i narzędzia odrzucają wszystko inne'."

**TODO:**
1. **CANONICAL_LOG_CONTRACT.md** (NEW)
   - Jeden plik z twardym kontraktem
   - Schema version enforcement spec
   - Required fields (nie opcjonalne)
   - Rejection rules
   
2. **Schema validator tool** (NEW)
   ```python
   def validate_log_schema(log_path):
       # Check schema_version field
       # Reject if missing or wrong
       # Reject if required fields missing
       # Return VALID/INVALID/LEGACY
   ```
   
3. **Integration**
   - sweep_krok6.py: write schema_version
   - validate_sweep.py: check schema
   - analysis tools: reject old schema

**Priorytet:** 🔴 CRITICAL (przed code P0!)  
**Estimated:** 4-6 godzin

---

### 2. KROK 3: Spójność metryk (KONCEPCYJNIE DONE nie KONTRAKTOWO)

**✅ Co jest:**
- Metryki interpretowane poprawnie
- Layer labels
- Hub-share, coverage, R0 zgodne z filozofią

**❌ Co brakuje (CRITICAL):**
> "Nadal nie ma jednego miejsca, gdzie definicja metryki jest:
> - jednoznaczna
> - kanoniczna
> - wiązana z walidacją"

**TODO:**
1. **CANONICAL_METRICS.md** (NEW)
   - Jedna definicja każdej metryki
   - Matematyczna formuła
   - Layer assignment (L1/L2/L3)
   - Bounds (min/max)
   - Validation rules
   - Implementation reference
   
2. **Metrics validator enhancement**
   ```python
   # Load from CANONICAL_METRICS.md
   METRIC_SPECS = load_canonical_specs()
   
   def validate_metric(name, value):
       spec = METRIC_SPECS[name]
       # Check bounds
       # Check type
       # Check layer consistency
   ```
   
3. **Integration**
   - validate_romion.py: use canonical specs
   - Analysis: reference canonical
   - Docs: link to canonical

**Priorytet:** 🔴 CRITICAL (przed code P0!)  
**Estimated:** 4-6 godzin

---

## ❌ CO ŚWIADOMIE NIE ZROBIONE (OK - nie ruszać!)

### 1. Code P0 patches
**Status:** DELIBERATELY DEFERRED

**Powód z oceny GPT:**
> "Kod NIE powinien być teraz masowo refaktoryzowany"
> "Gdy kontrakty będą twarde – P0 patche będą trywialne i bezpieczne"

**Co to oznacza:**
- ❌ NIE implementować metrics_pre/post separation TERAZ
- ❌ NIE robić runtime fail-closed TERAZ
- ❌ NIE pisać schema_version do JSONL TERAZ

**Kiedy robić:**
- ✅ DOPIERO gdy KROK 2/3 są ZAMKNIĘTE
- ✅ DOPIERO gdy kontrakty są TWARDE

### 2. S2/field/spark reorganizacja
**Status:** DELIBERATELY DEFERRED

**Powód:**
> "Są oznaczenia, są noty ostrzegawcze,
> ale nie ma jeszcze pełnego rename/re-spec.
> To jest faza późniejsza."

**Co zrobione wystarczająco:**
- ✅ rule_field_tail (nie s2_tail)
- ✅ MVP/SPEC/DEPRECATED labels
- ✅ Dokumentacja rozróżnienia

**Co odłożyć:**
- Full code reorganization
- Removal quantum spark
- Complete S2 spec

---

## 🎯 STRATEGIA ZGODNA Z OCENĄ GPT

### FAZA 1: CONTRACTS (Week 1) - IMMEDIATE
**Cel:** Zamknąć KROK 2 i KROK 3 kontraktowo

**Tasks:**
1. ✅ **CANONICAL_LOG_CONTRACT.md**
   - Twardy kontrakt schematu
   - Rejection rules
   - Version enforcement spec
   
2. ✅ **CANONICAL_METRICS.md**
   - Jedna prawda o metrykach
   - Definicje + bounds + validation
   - Layer assignments
   
3. ✅ **Schema validator tool**
   - Implementacja kontraktu logów
   - Integration w validation pipeline
   
4. ✅ **Metrics validator enhancement**
   - Implementacja kontraktu metryk
   - Integration w validate_romion.py

**Time:** 8-12 godzin  
**Outcome:** Kontrakty TWARDE, philosophy LOCKED

**Po tym:**
> "P0 patche w kodzie będą już trywialne i bezpieczne"

---

### FAZA 2: CODE P0 (Week 2-3) - DEFERRED
**Cel:** Implementacja P0 z audytu (TERAZ już bezpieczne!)

**Warunek wejścia:**
- ✅ FAZA 1 complete
- ✅ Kontrakty locked
- ✅ Validation enforced

**Tasks:**
1. Schema v2 implementation w engine.py
2. metrics_pre/post separation
3. Runtime fail-closed
4. Frustration w metrics
5. Code alignment z kontraktami

**Time:** 20-30 godzin  
**Outcome:** Code ALIGNED, contracts ENFORCED

---

### FAZA 3: P1/P2 (Week 4+) - OPTIONAL
**Cel:** Polish i dokumentacja

**Tasks z audytu:**
- Terminology standardization
- Documentation hierarchy  
- Remaining validations
- Language audits

**Time:** 30-40 godzin  
**Outcome:** Publication-ready

---

## 📊 CO TO ZMIENIA W PLANIE

### ❌ STARY PLAN (błędny):
1. Zrobić P0 code patches teraz
2. Implementować schema v2 teraz
3. Refaktoryzować kod masowo

### ✅ NOWY PLAN (zgodny z GPT):
1. **NAJPIERW:** Lock contracts (logi + metryki)
2. **POTEM:** Safe code P0
3. **NA KOŃCU:** Polish

### Dlaczego to lepsze?

**Z oceny GPT:**
> "Bez tych dwóch [kontraktów]:
> - dalsze prace (warp, kosmologia, detektory) 
>   będą znów ryzykowały dryf"

**Interpretacja:**
- Contracts = fundament stability
- Code = implementation details
- Contracts first → code trivial
- Code first → drift risk

---

## 🎯 IMMEDIATE NEXT STEPS (Start now)

### 1. CANONICAL_LOG_CONTRACT.md (2-3h)

**Structure:**
```markdown
# ROMION Canonical Log Contract

**Version:** 2.0
**Status:** AUTHORITATIVE
**Enforcement:** MANDATORY from 2026-01-11

## Schema Requirements

### Required Fields (MUST)
- schema_version: "2.0"
- type: "STATE" | "GRAPH" | "EVENT"
- tick: integer >= 0
- timestamp: ISO 8601 UTC

### STATE Event (metrics)
MUST have:
- metrics_pre: {...}  # Before U
- metrics_post: {...} # After U
- projection: {...}   # Πθ results

### Validation Rules
- Missing schema_version → REJECT
- Wrong schema_version → REJECT  
- Missing required fields → REJECT
- Type mismatch → REJECT

### Legacy Handling
- v1 logs: Mark [LEGACY-V1]
- Analysis: Warn if v1 detected
- No mixing v1+v2 in aggregation
```

### 2. CANONICAL_METRICS.md (2-3h)

**Structure:**
```markdown
# ROMION Canonical Metrics Definitions

**Version:** 2.0
**Status:** AUTHORITATIVE
**Source of Truth:** This file

## Primary Metrics

### hub_share (L2-FRACTURE)
**Definition:** Degree dominance in bridge graph
**Formula:** hub_degree / Σ_all_degrees × 100
**Layer:** L2 (projection-dependent)
**Bounds:** [0, 100]
**Type:** percentage
**Validation:** 0 <= value <= 100
**Implementation:** analysis/gravity_test/metrics.py::compute_hub_share()

### coverage (L2-FRACTURE)
**Definition:** Cluster participation in bridges
**Formula:** clusters_with_bridge / n_clusters × 100
**Layer:** L2 (projection-dependent)
**Bounds:** [0, 100]
**Type:** percentage
**Validation:** 0 <= value <= 100
**Implementation:** analysis/gravity_test/metrics.py::compute_coverage()

[... all metrics ...]
```

### 3. Schema validator (1-2h)

```python
# scripts/validate_log_schema.py

def validate_log_schema(log_path: Path) -> ValidationResult:
    """
    Validate log against CANONICAL_LOG_CONTRACT.
    
    Returns:
        ValidationResult with status:
        - VALID: Compliant with v2.0
        - LEGACY_V1: Old format (warn)
        - INVALID: Broken/incomplete
    """
    
    with open(log_path) as f:
        first_line = f.readline()
        obj = json.loads(first_line)
        
        # Check schema_version
        if 'schema_version' not in obj:
            return ValidationResult(
                status="LEGACY_V1",
                reason="Missing schema_version field"
            )
        
        if obj['schema_version'] != "2.0":
            return ValidationResult(
                status="INVALID",
                reason=f"Wrong schema version: {obj['schema_version']}"
            )
        
        # Check required fields
        # ...
        
        return ValidationResult(status="VALID")
```

### 4. Integration (1-2h)

- validate_sweep.py: call validate_log_schema()
- Analysis tools: check schema before processing
- sweep_krok6.py: write schema_version (when FAZA 2)

---

## ❓ PYTANIA DO UŻYTKOWNIKA

Przed rozpoczęciem FAZA 1 potrzebuję potwierdzenia:

### Q1: Czy zgadzasz się z oceną GPT?
**GPT mówi:** "NIE poprawiaj kodu teraz, DOKOŃCZ kontrakty"

**Zgadzasz się?** 
- [ ] TAK - robimy kontrakty (CANONICAL_LOG_CONTRACT + CANONICAL_METRICS)
- [ ] NIE - chcesz inaczej

### Q2: Priorytet FAZA 1?
**Tasks:**
1. CANONICAL_LOG_CONTRACT.md (2-3h)
2. CANONICAL_METRICS.md (2-3h)
3. Schema validator (1-2h)
4. Integration (1-2h)

**Total:** 6-10h

**Zgadzasz się na ten scope?**
- [ ] TAK - zaczynamy
- [ ] NIE - inny zakres

### Q3: Po FAZA 1 - co dalej?
**Options:**
- A) FAZA 2 (Code P0) immediately
- B) Pause for experiments with locked contracts
- C) Partial P2 (documentation)

**Preferencja?**

### Q4: Pytania do GPT?
**Czy mam zapytać GPT o:**
- [ ] Dodatkowe wyjaśnienia oceny kontrolnej
- [ ] Potwierdzenie strategii CONTRACTS FIRST
- [ ] Inne pytania: _______________

---

## 📋 CHECKPOINT - CO TERAZ?

**Waiting for:**
1. Odpowiedzi Q1-Q4
2. Potwierdzenie strategii
3. Green light do FAZA 1

**Gdy dostanę:**
- Begin CANONICAL_LOG_CONTRACT.md
- Track progress live
- Report completion

---

## 🎓 KEY INSIGHTS Z OCENY KONTROLNEJ

### 1. Philosophy Shift = SUCCESS
> "Zatrzymać dryf filozoficzny"
> "Uchronić ROMION przed ontologiczną inflacją"

**Impact:** Największe osiągnięcie session 2026-01-09

### 2. Contracts > Code
> "Gdy kontrakty będą twarde – 
> P0 patche będą trywialne i bezpieczne"

**Impact:** Strategia bottom-up nie top-down

### 3. Epistemiczny nie Ontologiczny
> "Traktuj repo jak 'system epistemiczny', 
> nie 'silnik fizyki'"

**Impact:** Fundamental mindset shift

### 4. Nie Kosmetyka - Stabilizacja
> "To NIE jest kosmetyka. 
> To jest realne ustabilizowanie teorii."

**Impact:** Validation całej pracy

---

## ✅ GOTOWOŚĆ

**Plan:** COMPLETE  
**Strategy:** ALIGNED with GPT eval  
**Confidence:** MAXIMUM

**Waiting for:** User confirmation to proceed

---

*Created: 2026-01-10 02:00*  
*Based on: GPT Control Evaluation + Original Audit*  
*Strategy: CONTRACTS FIRST, Code Second*  
*Status: READY TO EXECUTE*
