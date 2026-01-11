# Pytania do ChatGPT - założenia teorii ROMION wymagające uzasadnienia

Data utworzenia: 2026-01-08
Status: ODPOWIEDZIANE

---

## Q1: Trzy osobne progi (wcluster / wdist / wbridge)

**Założenie w teorii:**
W ROMION O'LOGIC istnieją trzy semantycznie różne progi wagowe:
- `wcluster` = próg dla klastrów (materia/obiekty)
- `wdist` = próg dla geometrii tła (dystanse między klastrami)  
- `wbridge` = próg dla mostów (pole/interakcje)

**Pytanie:**
Skąd wynika to rozróżnienie? Jakie jest teoretyczne uzasadnienie dla trzech osobnych progów zamiast jednego?

**ODPOWIEDŹ ChatGPT (2026-01-08):**

Trzy progi to nie parametry tuningowe, tylko definicje trzech różnych bytów:

1. **wcluster (obiekty/materia)** - relacja wystarczająco trwała/gęsta żeby tworzyć strukturę lokalną
2. **wdist (geometria)** - relacja wystarczająco stabilna żeby budować metrykę tła i dystanse
3. **wbridge (pole)** - relacja rzadka, selektywna, "kanałowa", wykrywana jako anomalia/most ponad tłem

Zlewanie ich w jeden próg wprowadza błędne koło - to samo odcięcie jednocześnie definiuje obiekty, metrykę i pole. Wtedy "most" nie jest mostem względem tła.

Typowe relacje:
- `wcluster` > `wdist` (obiekty są "twardsze" niż tło)
- `wbridge` > `wdist` (mosty mają być selektywne, nie częste)

**Status:** ✅ POTWIERDZONE - implementować rozdzielenie progów

---

## Q2: Dystanse na background graph vs bridge graph

**Założenie w teorii:**
Dystanse między klastrami powinny być liczone na "background graph" (zbudowanym wg `wdist`), a NIE na grafie mostów (zbudowanym wg `wbridge`).

**Pytanie:**
Dlaczego dystans ma być liczony na innym grafie niż mosty?

**ODPOWIEDŹ ChatGPT (2026-01-08):**

Dystans ma być niezależny od pola. Jeśli liczysz dystans na grafie mostów:
- Most z definicji daje dystans 1 (tautologia)
- Pary bez mostów mają często dystans ∞ (graf rzadki)
- Metryka jest "pocięta" przez to co próbujesz wykrywać

Pytanie które ma odpowiadać dystans:
> "Jak daleko są od siebie obiekty w sensie TŁA, zanim dodamy pole?"

Pytanie które ma odpowiadać most:
> "Czy istnieje dodatkowe, selektywne sprzężenie ponad tłem?"

Jeśli dystans na bridge graph, to detekcja mostu jest tautologią.

**Błąd który to powoduje:**
- "range=1 zawsze" bo mosty z definicji robią dystans 1
- Fałszywe rankingi i artefakty

**Status:** ✅ POTWIERDZONE - implementować osobny background graph dla dystansów

---

## Specyfikacja implementacyjna (z odpowiedzi)

### (I) Klasteryzacja: wcluster
1. Graf G_cluster z krawędzi >= wcluster
2. Znajdź klastry (CC)
3. Przypisz cluster_id

### (II) Geometria tła: wdist  
1. Graf G_bg z krawędzi >= wdist
2. Meta-graf M_bg (klastrów)
3. D_bg(A,B) = shortest_path na M_bg

### (III) Mosty/pole: wbridge
1. Graf G_bridge z krawędzi >= wbridge
2. Meta-graf M_bridge
3. Licz mosty między klastrami

**Kluczowe:** meta_bg_edges ≠ meta_bridge_edges

---

## Obecne błędy w kodzie (do naprawy)

1. ❌ Klastruje na `wdist` zamiast `wcluster`
2. ❌ Dystans liczony na krawędziach `wbridge` zamiast `wdist`
3. ❌ `meta_edges` używane jednocześnie do dystansu i mostów

