# Lab 7 – IMDB, ulepszona wersja (100% danych, BiLSTM)

## Cel

Sprawdzić, jak zestaw usprawnień (BiLSTM, mocniejsza regularyzacja, scheduler, pełne dane) wpływa na wyniki klasyfikacji sentymentu IMDB.

## Kluczowe zmiany względem bazowej wersji

- Architektura: BiLSTM (1 warstwa), dropout=0.7, FC dostosowane do kierunków; embedding 128.
- Trening: Adam lr=0.001 z weight_decay=1e-4, grad clipping=1.0, ReduceLROnPlateau (patience=2, factor=0.5), early stopping patience=7.
- Dane: 100% zbioru (25k/25k), słownik 10k, padding token=0, max_len ∈ {50, 100, 200}.
- Grid: hidden_dim ∈ {64, 128, 256}; wszystkie konfiguracje dwukierunkowe LSTM; 30 epok max, batch=64.

## Wyniki (test accuracy)

| Konfiguracja | Test | Val best | Epoki |
|--------------|------|----------|-------|
| BiLSTM h=256, len=200 | 0.8457 | 0.8624 | 21 |
| BiLSTM h=64, len=200  | 0.8444 | 0.8576 | 22 |
| BiLSTM h=128, len=200 | 0.8428 | 0.8688 | 20 |
| BiLSTM h=256, len=100 | 0.7992 | 0.8146 | 18 |
| BiLSTM h=128, len=100 | 0.7970 | 0.8242 | 16 |
| BiLSTM h=64,  len=100 | 0.7954 | 0.8136 | 14 |
| BiLSTM h=256, len=50  | 0.7440 | 0.7620 | 12 |
| BiLSTM h=64,  len=50  | 0.7393 | 0.7726 | 13 |
| BiLSTM h=128, len=50  | 0.7364 | 0.7646 | 13 |

Plik zbiorczy: `results/experiments_summary.json` (9 eksperymentów), tabela CSV: `results/summary.csv`.

## Wnioski

1. **Dłuższe sekwencje pomagają** w biLSTM (len=200 daje +4–10pp vs 50). Dwukierunkowość i większy dropout pozwalają wykorzystać dłuższy kontekst bez utraty stabilności.
2. **Hidden_dim 64/128/256 podobne** na test (~0.79–0.85). Przy len=200 różnice są marginalne (maks +0.3pp), więc można wybrać 64/128 dla oszczędności parametrów (1.38–1.54M vs 2.07M).
3. **Regularyzacja działa**: mimo wysokiej accuracy treningowej (~0.97–0.99) walidacja utrzymuje 0.81–0.87; early stopping zatrzymuje w 12–22 epokach.
4. **Scheduler + grad clipping** stabilizują dłuższe sekwencje: brak eksplozji gradientu, krzywe walidacji gładkie; lr redukowany, gdy val loss plateau.

## Rekomendacje dalsze

1. Spróbować embeddings pretrained (GloVe/fastText) zamiast losowych 128-d, utrzymując len=200.
2. Zmniejszyć dropout do 0.5 przy hidden=64/128 (możliwy +1–2pp) lub włączyć layer_norm LSTM.
3. Testować mniejszy batch (32) dla potencjalnie lepszej generalizacji przy dłuższych sekwencjach.

## Pliki

- Wyniki: `results/*.json`, `results/experiments_summary.json`, `results/summary.csv`.
- Analiza: `compare_results.py` (uruchomione), log: `experiment_log.txt`.
- Trening/eksperymenty: `run_experiments.py`, `train.py`, `model.py` (BiLSTM). `quick_test.py` do sanity check.
