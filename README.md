# A* Pathfinding Visualizer

Projekt realizowany w ramach przedmiotu **„Grafy i ich zastosowania”**.

## Temat

**Algorytm A* i jego zastosowania**

Projekt towarzyszy referatowi trwającemu 25 minut, po którym przewidziane jest 5 minut na pytania i dyskusję.

## Zakres

Projekt obejmuje:

- wyszukiwanie najkrótszej ścieżki z wykorzystaniem funkcji heurystycznej,
- algorytm A*,
- porównanie algorytmu A* z algorytmem Dijkstry,
- wpływ jakości heurystyki na działanie algorytmu,
- warunki gwarantujące znalezienie najkrótszej drogi,
- zastosowania algorytmu A* w:
    - nawigacji,
    - planowaniu tras,
    - robotyce,
    - grach komputerowych.

## Część praktyczna

Repozytorium zawiera interaktywną wizualizację pokazującą:

- działanie algorytmu A*,
- działanie algorytmu Dijkstry jako punkt odniesienia,
- odwiedzane wierzchołki,
- końcową najkrótszą ścieżkę,
- różnice w liczbie odwiedzonych wierzchołków,
- działanie różnych funkcji heurystycznych.

## Heurystyki

Wizualizacja zawiera:

- odległość Manhattan – `|Δx| + |Δy|`, na planszy bez przeszkód równa rzeczywistej długości drogi przy ruchu w 4 kierunkach,
- odległość euklidesową – `√(Δx² + Δy²)`, słabiej poinformowana (zaniża koszt bardziej niż Manhattan).

Żadna z nich nie przeszacowuje odległości do celu, dlatego A* z każdą z nich znajduje ścieżkę tej samej, minimalnej długości co Dijkstra.

## Technologie

- Python
- Pygame

---

## Instalacja

Wymagany jest Python 3.10 lub nowszy (projekt testowano na Pythonie 3.13).

```bash
git clone https://github.com/marcin-o/astar-pathfinding-visualizer.git
cd astar-pathfinding-visualizer

python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS

pip install -r requirements.txt
```

## Uruchomienie

Z katalogu głównego repozytorium:

```bash
python src/main.py
```

Okno ma rozdzielczość 1280×720. Klawisz **F** przełącza tryb pełnoekranowy – obraz jest wtedy skalowany do rozdzielczości ekranu/projektora.

## Sterowanie

| Klawisz / mysz | Działanie |
|---|---|
| **LPM** (przeciąganie) | rysowanie przeszkód |
| **LPM** na polu **S** / **C** + przeciąganie | przesunięcie startu / celu |
| **PPM** (przeciąganie) | usuwanie przeszkód |
| **Spacja** | uruchomienie algorytmu / pauza / wznowienie |
| **Enter** | pominięcie animacji i pokazanie wyniku od razu |
| **A** / **D** | wybór algorytmu: A* / Dijkstra |
| **H** | zmiana heurystyki A* (Manhattan ↔ euklidesowa); gdy wybrana jest Dijkstra – przejście do A* |
| **+** / **−** (lub **↑** / **↓**) | prędkość animacji |
| **P** | porównanie wariantów na bieżącej planszy (bez animacji): Dijkstra, A* euklidesowa, A* Manhattan |
| **C** | wyczyszczenie wyniku (przeszkody zostają) |
| **R** | wyczyszczenie całej planszy |
| **L** | losowe przeszkody |
| **M** | labirynt |
| **F** / **F11** | pełny ekran |
| **Esc** | wyjście z pełnego ekranu / zamknięcie programu |

Skrót sterowania jest zawsze widoczny na dole okna.

## Jak działa program

- **Plansza to graf.** Każde pole jest wierzchołkiem, a krawędzie łączą pola sąsiadujące w górę, w dół, w lewo i w prawo (bez ruchu po skosie). Koszt każdego ruchu wynosi 1, a przeszkody są wierzchołkami usuniętymi z grafu.
- **A*** wybiera z kolejki priorytetowej wierzchołek o najmniejszym `f(n) = g(n) + h(n)`, gdzie `g(n)` to koszt dojścia od startu, a `h(n)` to oszacowanie odległości do celu. Przy równym `f(n)` wybierany jest wierzchołek z mniejszym `h(n)`, czyli bliższy celowi.
- **Dijkstra** wybiera wierzchołek o najmniejszym `g(n)` – jest to A* z `h(n) = 0`, dlatego rozchodzi się równomiernie we wszystkich kierunkach.
- Algorytm wykonuje się w całości, zapisując kolejne kroki: który wierzchołek został zdjęty z kolejki i które wierzchołki trafiły do zbioru kandydatów. Animacja odtwarza te kroki z wybraną prędkością, a na końcu rysuje znalezioną ścieżkę.
- **Odwiedzone wierzchołki** to wierzchołki zdjęte z kolejki i przeanalizowane (łącznie ze startem i celem). **Długość ścieżki** to liczba ruchów od startu do celu.
- Tabela **Porównanie** zbiera wyniki uruchomień na tej samej planszy w kolejności: Dijkstra, A* z heurystyką euklidesową, A* z heurystyką Manhattan – od braku heurystyki do coraz lepszego oszacowania. Długość ścieżki jest we wszystkich wariantach taka sama, różni się liczba odwiedzonych wierzchołków. Każda zmiana planszy czyści tabelę.
- Jeżeli wynik jest widoczny, edycja planszy (przeszkody, przesunięcie startu lub celu) od razu przelicza i pokazuje nowy wynik.
- Jeżeli cel jest nieosiągalny, na planszy pojawia się komunikat **BRAK ŚCIEŻKI**.

### Oznaczenia na planszy

| Kolor | Znaczenie |
|---|---|
| zielony z literą **S** | punkt startowy |
| czerwony z literą **C** | punkt docelowy |
| ciemnoszary | przeszkoda |
| biały | puste pole |
| pomarańczowy | wierzchołek aktualnie analizowany |
| niebieski (ciemniejszy = przed chwilą) | wierzchołek odwiedzony |
| jasnozielony | kandydat – wierzchołek w kolejce priorytetowej |
| żółty | znaleziona ścieżka |

### Przykładowy przebieg demonstracji

1. Na pustej planszy narysuj ścianę między startem a celem i uruchom A* (**Spacja**).
2. Przełącz na Dijkstrę (**D**) i uruchom ponownie – porównaj obszar i liczbę odwiedzonych wierzchołków.
3. Wróć do A* (**A**), przełącz heurystykę na euklidesową (**H**), uruchom ponownie i porównaj kształt przeszukanego obszaru.
4. Naciśnij **P** – tabela pokaże Dijkstrę, A* z heurystyką euklidesową i A* z heurystyką Manhattan: ścieżka ma tę samą długość, a liczba odwiedzonych wierzchołków zwykle maleje.
5. Zamknij przejście do celu przeszkodami – program pokaże brak ścieżki.

## Testy

Testy logiki (algorytmy, heurystyki, plansza, animacja) nie wymagają otwierania okna Pygame:

```bash
python -m pytest
```

## Struktura projektu

```
src/
  main.py                    # punkt wejścia
  algorithms/
    grid_graph.py            # graf siatki: sąsiedzi w 4 kierunkach, koszt ruchu
    astar.py                 # algorytm A*
    dijkstra.py              # algorytm Dijkstry
    heuristics.py            # heurystyki
    search_result.py         # wynik wyszukiwania i zapis kroków
  visualization/
    app.py                   # pętla programu i obsługa wejścia
    board.py                 # stan planszy: start, cel, przeszkody, generatory
    animation.py             # odtwarzanie kroków algorytmu
    search_settings.py       # wybór algorytmu i heurystyki
    grid.py                  # rysowanie planszy
    ui.py                    # panel boczny, legenda, sterowanie
    theme.py                 # kolory, czcionki, wymiary
tests/                       # testy pytest
```
