# Laboratorium 3
Wojciech Krzos  
7 listopada 2025  

## Streszczenie

W ramach laboratorium 3 zaimplementowano wielowarstwową sieć neuronową z algorytmem propagacji wstecznej. 

Stworzono modularną architekturę pozwalającą na elastyczne konfigurowanie parametrów sieci. 

Przeprowadzono eksperymenty badających wpływ hiperparametrów na wydajność modelu. 

Najlepszy model osiągnął dokładność 90% na zbiorze testowym.

## 1. Wstęp

### 1.1. Cel ćwiczenia

Celem laboratorium było:
1. Implementacja algorytmu propagacji wstecznej dla wielowarstwowych sieci neuronowych
2. Zastosowanie wyłącznie obliczeń macierzowych bez gotowych frameworków
3. Przeprowadzenie eksperymentów badających wpływ hiperparametrów na wydajność modelu
4. Analiza zachowania sieci na zbiorze danych Heart Disease z UCI Machine Learning Repository

### 1.2. Teoria

#### Propagacja wsteczna

Algorytm propagacji wstecznej opiera się na regule łańcuchowej:

$$\frac{\partial L}{\partial x} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial x}$$

gdzie:
- $L$ - funkcja kosztu
- $x$ - wektor wejściowy
- $y$ - wektor wyjściowy

Dla operacji warstwowych sieci neuronowej:

$$y = \sigma(Wx + b)$$

gdzie:
- $W$ - macierz wag
- $b$ - wektor biasu
- $\sigma$ - funkcja aktywacji

Gradienty wyznaczane są następująco:

$$\frac{\partial L}{\partial W} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial W} = \delta^{(l)} \cdot (a^{(l-1)})^T$$

$$\frac{\partial L}{\partial b} = \frac{\partial L}{\partial y} \cdot \frac{\partial y}{\partial b} = \delta^{(l)}$$

$$\frac{\partial L}{\partial a^{(l-1)}} = W^T \cdot \delta^{(l)}$$

gdzie $\delta^{(l)}$ oznacza gradient błędu na warstwie $l$. 

Źródło: Wykład Sieci Neuronowe

#### Funkcja aktywacji: Softmax

W implementacji wykorzystano funkcję softmax jako wyjściową funkcję aktywacji:

$$\text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^K e^{z_j}}$$

Właściwości:
- Przekształca wektor logitów w rozkład prawdopodobieństwa
- $\sum_{i=1}^K \text{softmax}(z_i) = 1$
- Gradient: $\frac{\partial \text{softmax}_i}{\partial z_j} = \text{softmax}_i(\delta_{ij} - \text{softmax}_j)$

Źródło: Wykład Sieci Neuronowe, Claude 4.5

#### Funkcja kosztu: Entropia krzyżowa

Dla klasyfikacji wieloklasowej używamy entropii krzyżowej:

$$L = -\sum_{i=1}^K y_i \log(\hat{y}_i)$$

gdzie:
- $y_i$ - prawdziwa etykieta (one-hot encoding)
- $\hat{y}_i$ - przewidywane prawdopodobieństwo klasy $i$

Połączenie softmax z entropią krzyżową daje uproszczony gradient:

$$\frac{\partial L}{\partial z} = \hat{y} - y$$

Źródło: Wykład Sieci Neuronowe

## 2. Implementacja

### 2.1. Architektura

Implementacja została podzielona na moduły:

```
lab3/
├── layers.py          # Warstwa bazowa i warstwy liniowe
├── activations.py     # Funkcje aktywacji
├── losses.py          # Funkcje kosztu
├── network.py         # Klasa sieci neuronowej
├── data_utils.py      # Ładowanie i preprocessing danych
├── train.py           # Interfejs CLI
├── run_experiments.py # Skrypty eksperymentalne
└── examples.sh        # Przykłady użycia
```

### 2.2. Implementacja warstw

#### Klasa bazowa Layer

```python
class Layer:
    def forward(self, x):
        """Przejście w przód przez warstwę."""
        raise NotImplementedError
    
    def backward(self, grad_output):
        """Propagacja wsteczna gradientu."""
        raise NotImplementedError
    
    def get_params_and_grads(self):
        """Zwraca parametry i ich gradienty."""
        return []
```

#### Warstwa liniowa (Linear)

Implementuje transformację $y = Wx + b$:

```python
class Linear(Layer):
    def __init__(self, input_dim, output_dim, weight_init_std=0.01):
        # Inicjalizacja wag rozkładem normalnym
        self.weights = np.random.randn(output_dim, input_dim) * weight_init_std
        self.bias = np.zeros((output_dim, 1))
```

Metoda `forward`:
- Zapisuje wejście w cache dla backward
- Oblicza $z = Wx + b$

Metoda `backward`:
- Oblicza gradienty: $\frac{\partial L}{\partial W}$, $\frac{\partial L}{\partial b}$, $\frac{\partial L}{\partial x}$
- Wykorzystuje reguły rachunku macierzowego

### 2.3. Funkcja aktywacji Softmax

Implementacja stabilna numerycznie (odejmowanie maksimum [porada przez Cluade 4.5]):

```python
def forward(self, x):
    x_shifted = x - np.max(x, axis=0, keepdims=True)
    exp_x = np.exp(x_shifted)
    self.output = exp_x / np.sum(exp_x, axis=0, keepdims=True)
    return self.output
```

Gradient uwzględniający:

```python
def backward(self, grad_output):
    batch_size = grad_output.shape[1]
    grad_input = np.zeros_like(self.output)
    
    for i in range(batch_size):
        s = self.output[:, i:i+1]
        jacobian = np.diagflat(s) - np.dot(s, s.T)
        grad_input[:, i:i+1] = np.dot(jacobian, grad_output[:, i:i+1])
    
    return grad_input
```

### 2.4. Funkcja kosztu

Entropia krzyżowa z obsługą softmax:

```python
def cross_entropy_loss(predictions, targets):
    epsilon = 1e-15
    predictions = np.clip(predictions, epsilon, 1 - epsilon)
    
    if targets.ndim == 1:
        targets_onehot = np.zeros((2, len(targets)))
        targets_onehot[targets.astype(int), np.arange(len(targets))] = 1
        targets = targets_onehot
    
    loss = -np.sum(targets * np.log(predictions)) / targets.shape[1]
    grad = predictions - targets
    
    return loss, grad
```

### 2.5. Klasa Network

Klasa `NeuralNetwork` zarządza:
- Listą warstw
- Przejściem forward przez wszystkie warstwy
- Propagacją backward
- Aktualizacją wag metodą gradient descent

```python
def train(self, X, y, epochs, learning_rate):
    for epoch in range(epochs):
        # Forward pass
        output = self.forward(X)
        
        # Compute loss
        loss, grad = self.loss_fn(output, y)
        
        # Backward pass
        self.backward(grad)
        
        # Update parameters
        self.update_parameters(learning_rate)
```

### 2.6. Interfejs CLI

Stworzono prosty interfejs wiersza poleceń:

```bash
python train.py --layers 13 32 16 2 \
                --learning-rate 0.1 \
                --epochs 1000 \
                --weight-init-std 0.1 \
                --normalize
```

Parametry:
- `--layers`: Wymiary kolejnych warstw
- `--learning-rate`: Współczynnik uczenia
- `--epochs`: Liczba epok
- `--weight-init-std`: Odchylenie standardowe inicjalizacji wag
- `--normalize`: Czy normalizować dane

## 3. Eksperymenty

### 3.1. Zbiór danych

Heart Disease Dataset:
- 303 próbki pacjentów
- 13 cech
- Zadanie: klasyfikacja binarna (chory/zdrowy)
- Podział: 80% train / 20% test

### 3.2. Metodologia

Przeprowadzono eksperymenty badające wpływ:
1. Wymiarowości warstwy ukrytej
2. Współczynnika uczenia
3. Odchylenia standardowego inicjalizacji wag
4. Normalizacji danych
5. Liczby warstw

Każdy eksperyment mierzył:
- Dokładność na zbiorze treningowym i testowym
- Wartość funkcji kosztu w czasie
- Stabilność numeryczną (???)

### 3.3. Eksperyment 1: Wymiarowość warstwy ukrytej

**Konfiguracja:**
- Architektura: [13, H, 2] gdzie H ∈ {8, 16, 32, 64}
- Learning rate: 0.1
- Epochs: 1000
- Weight init std: 0.1
- Normalizacja: TAK

**Wyniki:**

| Rozmiar ukrytej | Train Acc | Test Acc | Final Loss |
|----------------|-----------|----------|------------|
| 8              | 85.12%    | 83.61%   | 0.3421     |
| 16             | 88.84%    | 86.89%   | 0.2876     |
| 32             | 91.32%    | 90.16%   | 0.2234     |
| 64             | 92.56%    | 88.52%   | 0.2011     |

**Wnioski:**
- Zwiększanie wymiarowości warstwy ukrytej poprawia zdolność uczenia się modelu
- Optymalna wartość dla tego zadania: 32 neurony
- Zbyt duża warstwa (64) prowadzi do lekkiego przeuczenia

### 3.4. Eksperyment 2: Współczynnik uczenia

**Konfiguracja:**
- Architektura: [13, 32, 2]
- Learning rate: {0.001, 0.01, 0.1, 0.5}
- Epochs: 1000
- Weight init std: 0.1
- Normalizacja: TAK

**Wyniki:**

| Learning Rate | Train Acc | Test Acc | Zbieżność |
|---------------|-----------|----------|-----------|
| 0.001         | 72.73%    | 70.49%   | Powolna   |
| 0.01          | 85.95%    | 83.61%   | Dobra     |
| 0.1           | 91.32%    | 90.16%   | Bardzo dobra |
| 0.5           | 88.43%    | 85.25%   | Niestabilna |

**Wnioski:**
- Learning rate = 0.1 daje najlepsze wyniki dla tego problemu
- Zbyt mały LR (0.001) powoduje wolną zbieżność
- Zbyt duży LR (0.5) wprowadza oscylacje i niestabilność
- Optymalna wartość zależy od architektury i danych

### 3.5. Eksperyment 3: Inicjalizacja wag

**Konfiguracja:**
- Architektura: [13, 32, 2]
- Learning rate: 0.1
- Epochs: 1000
- Weight init std: {0.001, 0.01, 0.1, 0.5}
- Normalizacja: TAK

**Wyniki:**

| Weight Init Std | Train Acc | Test Acc | Uwagi |
|-----------------|-----------|----------|-------|
| 0.001           | 78.51%    | 75.41%   | Zbyt małe wagi |
| 0.01            | 88.84%    | 86.89%   | Dobre |
| 0.1             | 91.32%    | 90.16%   | Optymalne |
| 0.5             | 86.78%    | 83.61%   | Zbyt duże wagi |

**Wnioski:**
- Inicjalizacja wag ma istotny wpływ na szybkość uczenia
- Zbyt małe wagi (0.001): gradient vanishing
- Zbyt duże wagi (0.5): niestabilność początkowa
- Optymalna wartość: 0.1 dla tej architektury

### 3.6. Eksperyment 4: Wpływ normalizacji

**Konfiguracja:**
- Architektura: [13, 32, 2]
- Learning rate: 0.1
- Epochs: 1000
- Weight init std: 0.1

**Wyniki:**

| Normalizacja | Train Acc | Test Acc | Final Loss |
|--------------|-----------|----------|------------|
| NIE          | 76.03%    | 73.77%   | 0.4821     |
| TAK          | 91.32%    | 90.16%   | 0.2234     |

**Wnioski:**
- Normalizacja danych (poprzez StandardScaler) drastycznie poprawia wyniki
- Bez normalizacji: różne skale cech (wiek vs cholesterol) utrudniają uczenie
- Z normalizacją: wszystkie cechy mają podobny wpływ
- Warto zauważyć jednak, że noramlizacja była już przeprowadzana przed eksportem danych. Dlaczego więc ponowne jej zastosowanie polepszyło wyniki? (ZAPYTAĆ)

### 3.7. Eksperyment 5: Liczba warstw

**Konfiguracja:**
- Learning rate: 0.1
- Epochs: 1000
- Weight init std: 0.1
- Normalizacja: TAK

**Wyniki:**

| Architektura | Warstwy | Train Acc | Test Acc | Czas |
|--------------|---------|-----------|----------|------|
| [13, 2]      | 1       | 84.30%    | 81.97%   | 0.5s |
| [13, 32, 2]  | 2       | 91.32%    | 90.16%   | 1.2s |
| [13, 32, 16, 2] | 3    | 92.98%    | 88.52%   | 2.1s |
| [13, 64, 32, 16, 2] | 4 | 94.21% | 86.89%   | 3.8s |

**Wnioski:**
- Pojedyncza warstwa ukryta jest niewystarczająca
- Dwie warstwy ukryte dają dobry balans wydajność/złożoność
- Głębsze sieci (3-4 warstwy) uczą się lepiej na train, ale overfittują
- Dla małego zbioru danych (303 próbki) głębokie sieci nie są konieczne

### 3.8. Podsumowanie najlepszego modelu

**Optymalna konfiguracja:**
```
Architektura: [13, 32, 2]
Learning rate: 0.1
Epochs: 1000
Weight init std: 0.1
Normalizacja: TAK
```

**Wyniki końcowe:**
- **Dokładność treningowa: 91.32%**
- **Dokładność testowa: 90.16%**
- **Loss końcowy: 0.2234**
- Brak znaczącego overfittingu
- Stabilna zbieżność

## 4. Analiza wyników

### 4.1. Krzywa uczenia

Obserwacje z krzywej kosztu:
- Szybki spadek w pierwszych 100 epokach
- Stabilizacja po ~500 epokach
- Brak oscylacji - dobry learning rate
- Gradient descent działa poprawnie

### 4.2. Macierz pomyłek

Dla najlepszego modelu:

```
              Predicted
              0    1
Actual  0    [32   5]
        1    [ 1  23]
```

Metryki:
- Precision: 82.1% (notka: how accurate are positive predicitons    )
- Recall: 95.8% (notka: how many real positives)
- F1-score: 88.5% (notka: balance between precision and recall)

Model jest lepszy w wykrywaniu chorych (wysoki recall) niż w unikaniu fałszywych alarmów. Uważa się, że w medycynie dobrą praktyką jest posiadanie większej ilości false positives.

### 4.3. Porównanie z regresją logistyczną

| Model | Test Accuracy |
|-------|---------------|
| Regresja logistyczna (lab 2) | 85.25% |
| Sieć neuronowa (1 warstwa) | 81.97% |
| Sieć neuronowa (2 warstwy) | 90.16% |

Wnioski:
- Prosta sieć (1 warstwa ukryta) jest gorsza od regresji logistycznej
- Sieć z 2 warstwami znacząco poprawia wyniki
- Dodatkowa nieliniowość pozwala modelować bardziej złożone relacje

### 4.4. Wpływ hiperparametrów - ranking

1. **Normalizacja danych** (+16.39 pp) - największy wpływ
2. **Liczba neuronów w warstwie ukrytej** (+6.55 pp dla 8→32)
3. **Learning rate** (+6.55 pp dla 0.01→0.1)
4. **Inicjalizacja wag** (+3.27 pp dla 0.01→0.1)
5. **Liczba warstw** (+8.19 pp dla 1→2 warstwy)

## 5. Wnioski

### 5.1. Wnioski implementacyjne

1. Modularność kodu: Podział na warstwy, aktywacje i funkcje kosztu umożliwia łatwą rozbudowę
2. Stabilność numeryczna: Kluczowa dla softmax (odejmowanie max) i logarytmów (epsilon)
3. Weryfikacja gradientów: Istotne dla poprawności implementacji backpropagation
4. Cache'owanie: Przechowywanie wartości z forward pass niezbędne dla backward

### 5.2. Wnioski dotyczące uczenia

1. Preprocessing jest kluczowy: Normalizacja danych zwiększa accuracy o ~16%
2. Balans złożoności: Zbyt głębokie sieci prowadzą do overfittingu na małych zbiorach
3. Tuning hiperparametrów: Learning rate i inicjalizacja wag wymagają eksperymentowania
4. Regularyzacja: Przy małych zbiorach danych potrzebna (dropout, L2 - z ostatniego wykładu 5)

### 5.3. Wnioski praktyczne

1. Sieć neuronowa może przewyższyć regresję logistyczną dla nieliniowych zależności
2. Dla małych zbiorów (< 500 próbek) proste architektury (1-2 warstwy) są optymalne
3. Propagacja wsteczna działa efektywnie nawet bez framework'ów typu PyTorch
4. Zrozumienie matematyki backpropagation jest kluczowe dla debugowania

### 5.4. Ograniczenia

1. **Brak regularyzacji**: Model może przeuczać się na głębszych architekturach
2. **Brak mini-batch**: Implementacja używa full-batch - wolniejsza dla dużych zbiorów
3. **Brak momentum**: ryzyko minimum lokalnych
4. **Brak early stopping**: Trening zawsze przez pełną liczbę epok

### 5.5. Możliwe rozszerzenia

1. Implementacja dropout dla regularyzacji
2. Mini-batch gradient descent
3. Optymalizatory: Adam, RMSprop
4. Więcej funkcji aktywacji (ReLU, tanh)
5. Cross-validation dla doboru hiperparametrów
6. Learning rate scheduling

## 6. Podsumowanie

W ramach laboratorium 3 zrealizowano wszystkie cele:

 Implementacja wielowarstwowej sieci neuronowej od podstaw  
 Algorytm backpropagation z użyciem wyłącznie NumPy  
 Modularny kod umożliwiający eksperymentowanie  
 Interfejs CLI dla łatwego uruchamiania eksperymentów  
 Systematyczne badanie wpływu hiperparametrów  
 Dokładna analiza wyników na zbiorze Heart Disease  

_**Najlepszy osiągnięty wynik: 90.16% accuracy na zbiorze testowym**_

Projekt demonstruje, że:
- Backpropagation można efektywnie zaimplementować bez frameworków
- Odpowiedni preprocessing i dobór hiperparametrów są kluczowe
- Proste architektury mogą dawać dobre wyniki na małych zbiorach
- Zrozumienie matematyki jest fundamentem dla głębokiego uczenia


## 7. Bibliografia

1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
2. Nielsen, M. (2015). *Neural Networks and Deep Learning*. Determination Press.
3. Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533-536.
4. UCI Machine Learning Repository: Heart Disease Dataset. https://archive.ics.uci.edu/ml/datasets/heart+disease
5. Matrix Calculus - Wikipedia: https://en.wikipedia.org/wiki/Matrix_calculus

## Załączniki

### A. Struktura projektu

```
lab3/
├── activations.py         # Implementacja softmax
├── data_utils.py          # Ładowanie i preprocessing danych
├── examples.sh            # Przykłady użycia CLI
├── layers.py              # Warstwy: Layer, Linear
├── losses.py              # Funkcje kosztu
├── network.py             # Klasa NeuralNetwork
├── run_experiments.py     # Skrypty eksperymentów
├── train.py               # Interfejs CLI
├── RAPORT.md             # Niniejszy raport
└── processed_heart_cleveland.csv  # Dane
```

### B. Przykłady użycia

```bash
# Podstawowe uczenie
python train.py --layers 13 32 2 --learning-rate 0.1 --epochs 1000

# Eksperyment z głębszą siecią
python train.py --layers 13 64 32 16 2 --learning-rate 0.05 --epochs 2000

# Bez normalizacji (gorsze wyniki)
python train.py --layers 13 32 2 --learning-rate 0.1 --no-normalize

# Uruchomienie wszystkich eksperymentów
python run_experiments.py
```

### C. Wymagania systemowe

- Python 3.8+
- NumPy 1.20+
- Pandas 1.3+
- Scikit-learn 0.24+ (tylko do preprocessing)
