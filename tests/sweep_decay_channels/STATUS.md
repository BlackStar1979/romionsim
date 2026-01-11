# Decay Sweep: Wykorzystanie istniejących wyników + małe rozszerzenie

## Status

Symulacje R0-R5 z Test C już zawierają dane dla decay=[1.0, 0.7]:
- R0: decay=1.0 (baseline)
- R2: decay=0.7 (winner)

## Plan działania

### Faza 1: Analiza istniejących danych (DONE)
✅ R0-R5 @ tick 400 z channels/anisotropy  
✅ Time evolution R0, R2 (ticks 200-600)  
✅ Winner identified: R2 (decay=0.7)

### Faza 2: Rozszerzenie swepu (NEXT)

**Dodatkowe punkty do przetestowania:**
- decay=0.85 (między R0 i R2)
- decay=0.75 (blisko R2 od góry)
- decay=0.65 (blisko R2 od dołu)
- decay=0.6 (dalej od R2)

**Seeds:** [42, 123] (konsystentnie z R0-R5)

**Cel:** Znaleźć dokładne optimum wokół η=0.7

### Faza 3: Alternatywne podejście - użyj batch_test_c.py jako template

Zamiast batch_sweep który ma problemy z importami, możemy:

1. Stworzyć konfiguracje .cfg dla nowych punktów decay
2. Uruchomić ręcznie via run_from_config.py
3. Przeanalizować via gravity_test.py z --channels --anisotropy
4. Zebrać wyniki do CSV

## Tymczasowe rozwiązanie

Skoro istniejące dane pokazują:
- R0 (decay=1.0): 879 bridges, 3.577 cap @ tick 400
- R2 (decay=0.7): 1389 bridges, 7.417 cap @ tick 400

I widzimy że R2 > R0, możemy:

1. **Potwierdzić paradoks:** Mniejszy decay daje więcej aktywności
2. **Hipoteza optimum:** Optimum może być gdzieś między 0.6-0.8
3. **Następny krok:** Ręczne uruchomienie 4 dodatkowych punktów

## Wykonanie ręczne

```bash
# 1. Stw

órz konfigi
cd C:\Work\romionsim\tests\sweep_decay\cfg_manual

# decay=0.85
cat > decay_0.85_s42.cfg << EOF
[simulation]
ticks = 600
seed = 42
dump_graph_every = 100

[parameters]
spawn_scale = 1.0
decay_scale = 0.85
tension_scale = 1.0
base_delta = 0.5
variance = 1.0

[output]
output_dir = tests/sweep_decay/results/manual_d0.85_s42
EOF

# Podobnie dla 0.85/123, 0.75/42, 0.75/123, etc.

# 2. Uruchom
python scripts/run_from_config.py tests/sweep_decay/cfg_manual/decay_0.85_s42.cfg

# 3. Analizuj
python analysis/gravity_test.py \
  --log tests/sweep_decay/results/manual_d0.85_s42/simulation.jsonl \
  --tick 400 --channels --anisotropy --anisotropy-splits 5

# 4. Zbierz wyniki ręcznie do CSV
```

## Wnioski z sesji

1. **GPT Annexes implementation:** ✅ COMPLETE (95%)
2. **Dokumentacja:** ✅ COMPLETE
3. **Decay sweep automation:** ❌ Import issues z batch_sweep.py
4. **Alternatywa:** ✅ Ręczne uruchomienie możliwe
5. **Następny krok:** Użyj istniejących R0-R5 + dodaj 4 punkty ręcznie

---

**Priorytet:** Zrozumienie decay paradox jest ważniejsze niż automatyzacja sweep.

**Akcja:** Ręczne uruchomienie 4 punktów decay=[0.85, 0.75, 0.65, 0.6] z seeds=[42,123]
