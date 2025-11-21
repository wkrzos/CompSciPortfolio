# Ćwiczenie 5 – Klasyfikacja obrazów FashionMNIST

## Podsumowanie

Cel: Zbadanie wpływu architektury (jedno- vs dwuwarstwowa sieć w pełni połączona) oraz hiperparametrów (liczba neuronów, rozmiar batcha, liczba przykładów uczących, szum gaussowski) na jakość klasyfikacji obrazów FashionMNIST.

Status danych: Na moment przygotowania raportu pełny zestaw wyników nie został jeszcze wygenerowany (brak plików JSON w `lab5/results/`). Raport opisuje metodologię, oczekiwane zachowania oraz plan analizy – z miejscami na wstawienie konkretnych liczb po uruchomieniu eksperymentów.

## Dataset

FashionMNIST: 70 000 obrazów 28×28 (grayscale) w 10 klasach:
- 60 000 – trening
- 10 000 – test
- Klasy: T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot

Transformacje:
- `ToTensor()` – konwersja do tensora float32 (wartości w [0,1])
- Normalizacja: średnia 0.5, odchylenie 0.5 → zakres przeskalowany w przybliżeniu do [-1,1]
- Spłaszczenie w modelu przez `nn.Flatten()` przed warstwami liniowymi

## Architektury modeli

### SingleLayerNet
- Wejście: 784 (28×28)
- Ukryta: H (ReLU)
- Wyjście: 10 klas (logity → `CrossEntropyLoss`)

### TwoLayerNet
- Wejście: 784
- Ukryta 1: H1 (ReLU)
- Ukryta 2: H2 (ReLU)
- Wyjście: 10 klas

Parametry są tworzone fabryką `create_model(model_type, hidden_size, hidden_size2)`.

## Hiperparametry i zakres eksperymentów

| Kategoria | Wartości | Cel analizy |
|-----------|----------|-------------|
| Architektura | single, two | Czy dodatkowa warstwa poprawia jakość / stabilność |
| Hidden size | 64, 128, 256, 512 (dla two-layer: H2 = H/2) | Trade-off złożoność vs generalizacja |
| Batch size | 16, 32, 64, 128 | Wpływ na wariancję gradientu i szybkość uczenia |
| Data fraction | 1%, 10%, 100% | Jak zachowują się modele przy ograniczonych danych |
| Noise σ (test-only) | 0.1, 0.3, 0.5 | Odporność na degradację wejścia |
| Noise σ (train+test) | 0.1, 0.3, 0.5 | Czy uczenie na zaburzonych danych poprawia robustność |
| Epochs | 20 | Skrócone względem lab4 (tam 100) z uwagi na większą liczbę kombinacji |
| Learning rate | 0.001 (Adam) | Stabilna wartość bazowa dla klasyfikacji obrazów |
| Optimizer | Adam | Szybka konwergencja – skupienie na architekturze i danych |

## Metodyka eksperymentów

1. Generacja konfiguracji w `run_experiments.py` (funkcja `generate_experiment_configs`).
2. Dla każdej konfiguracji:
   - Inicjalizacja modelu.
   - Przygotowanie loaderów (`get_data_loaders`) z opcjonalnym subsettingiem i szumem.
   - Trening 20 epok: zapis loss i accuracy (train/test) per epoka.
   - Ewaluacja końcowa + obliczenie best test accuracy.
   - Zapis wyniku do JSON: `<nazwa>_results.json`.
3. Po serii eksperymentów: zapis zbiorczego pliku `experiments_summary_<timestamp>.json`.
4. Wizualizacje (`visualization.py`):
   - Krzywe tren./test loss i accuracy.
   - Porównania w formie overlay (architektury vs wartość hiperparametru).
5. Analiza (`compare_results.py`):
   - Tabele summary (parametry, final acc, best acc, overfit gap).
   - Ranking konfiguracji.

## Oczekiwane zachowania (hipotezy przed uruchomieniem)

### Architektura
- Two-layer może osiągać wyższą accuracy przy większych hidden size (256, 512) dzięki dodatkowej reprezentacji.
- Single-layer może generalizować lepiej przy małych danych (1%, 10%) z uwagi na mniejszą liczbę parametrów.

### Hidden size
- H=64: szybka konwergencja, potencjalnie ograniczona reprezentacja.
- H=128 / 256: dobry kompromis.
- H=512: ryzyko overfittingu przy 1% i 10% danych.

### Batch size
- Małe batch (16) → większa wariancja gradientu, możliwa lepsza generalizacja kosztem stabilności.
- Duże batch (128) → stabilne uczenie, ryzyko utknięcia w płaskich minimach / słabsza generalizacja.

### Data fraction
- 1% danych (~600 próbek): wyraźny overfitting dla większych modeli.
- 10% danych: modele średniej wielkości powinny już uzyskiwać rozsądną accuracy (>80%).
- 100% danych: pełna konwergencja – przewaga większych modeli.

### Noise – test-only
- Spadek accuracy wraz z rosnącym σ – modele bez treningu na zaburzonych danych są mniej odporne.
- Większe modele mogą być bardziej wrażliwe (nadmierne dopasowanie do czystych wzorców).

### Noise – train+test
- Umiarkowany szum (σ=0.1–0.3) może poprawić robustność (mniejsze różnice względem czystych danych).
- Zbyt duży szum (σ=0.5) utrudnia naukę → spadek accuracy.

## Plan analizy wyników (po uruchomieniu)

Sekcje do uzupełnienia danymi:

### 1. Porównanie architektur
| Konfiguracja | Parametry | Final Test Acc | Best Test Acc | Overfit Gap |
|--------------|-----------|----------------|---------------|-------------|
| single_h128 (PLACEHOLDER) | X | Y% | Z% | D% |
| two_h128_h64 (PLACEHOLDER) | X | Y% | Z% | D% |

### 2. Hidden size scaling
Krzywe accuracy vs epoka dla H ∈ {64,128,256,512} (single i two). Wstawienie wykresów z `hidden_size_comparison.png`.

### 3. Batch size
Tabela + wykres test accuracy vs batch size.

### 4. Data fraction
Krzywa: test accuracy vs % danych (dla architektur i wybranych H=128,256).

### 5. Noise robustness
Porównanie test-only vs train+test dla σ ∈ {0.1,0.3,0.5}.

### 6. Overfitting analysis
Zestawienie (train acc – test acc) dla konfiguracji skrajnych:
- Duży model + mało danych (H=512, 1%)
- Mały model + pełne dane (H=64, 100%)

## Przykładowe fragmenty kodu (dla dokumentacji)

### Definicja modelu (skrócona)
```python
class SingleLayerNet(nn.Module):
    def __init__(self, input_size=784, hidden_size=128, num_classes=10):
        super().__init__()
        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    def forward(self, x):
        x = self.flatten(x)
        return self.fc2(self.relu(self.fc1(x)))
```

### Pętla treningowa (skrót)
```python
for images, labels in train_loader:
    images, labels = images.to(device), labels.to(device)
    if noise_train: images = add_gaussian_noise(images, noise_std)
    optimizer.zero_grad()
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()
```

## Możliwe problemy i rozwiązania

| Problem | Przyczyna | Rozwiązanie |
|---------|-----------|-------------|
| Wolne uczenie | CPU only | Użyć GPU (`torch.cuda.is_available()`) |
| Overfitting małych subsetów | Za duży model | Zmniejszyć hidden size / dodać regularyzację |
| Niestabilna accuracy przy batch=16 | Wysoka wariancja | Zwiększyć batch / dodać normalizację danych |
| Słaba odporność na szum | Brak augmentacji | Trenować z szumem (train+test) |
| Zbyt długi czas eksperymentów | Dużo konfiguracji | Uruchamiać kategorie osobno (parametr `--experiment`) |

## Wnioski (po oczekiwanym uzupełnieniu wynikami)

1. Dodanie drugiej warstwy zwiększa zdolność do reprezentacji, ale nie zawsze poprawia generalizację przy małych danych.
2. Hidden size powyżej 256 może dawać malejące korzyści przy standardowym LR=0.001 i Adam.
3. Batch size 32/64 prawdopodobnie będzie kompromisem stabilność/szybkość; 16 może lekko poprawić generalizację kosztem fluktuacji.
4. Przy 1% danych – preferencja mniejszych modeli; przy pełnych danych – większe modele wykorzystują więcej wzorców.
5. Trenowanie z umiarkowanym szumem (σ≈0.1–0.3) może zwiększyć odporność na zaburzenia.

## Dalsze prace

- Dodanie regularizacji L2 / Dropout.
- Test alternatywnych aktywacji (LeakyReLU, GELU).
- Zwiększenie epok do 50 dla obserwacji późniejszego overfittingu.
- Włączenie Early Stopping.
- Porównanie z prostą CNN (konwolucje zamiast MLP) – spodziewana poprawa.
- Analiza czasu uczenia vs liczba parametrów.

## Checklist do uzupełnienia po uruchomieniu eksperymentów

- [ ] Uzupełnić tabele wyników architektur.
- [ ] Dodać konkretne wartości final/best test accuracy.
- [ ] Wstawić wygenerowane wykresy do raportu (ścieżki).
- [ ] Zweryfikować hipotezy vs wyniki (potwierdzone / odrzucone).
- [ ] Dodać sekcję ranking konfiguracji.

## Uruchomienie

```bash
cd lab5
pip install -r requirements.txt
./run_experiments.sh hidden_size
./run_experiments.sh batch_size
./run_experiments.sh data_size
./run_experiments.sh noise
python visualization.py --results-dir results --output-dir results/plots
python compare_results.py --results-dir results --output-file results/analysis_summary.txt
```

## Pliki

- `model.py` – architektury MLP
- `train.py` – pętle treningowe, noise injection
- `run_experiments.py` – generacja i uruchamianie konfiguracji
- `visualization.py` – wykresy
- `compare_results.py` – analiza wyników
- `quick_test.py` – szybka weryfikacja środowiska
- `EXAMPLES.md` – przykłady użycia
- `raport.md` – niniejszy raport

---
Raport wygenerowany automatycznie – sekcje wynikowe wymagają uzupełnienia po wykonaniu eksperymentów.
