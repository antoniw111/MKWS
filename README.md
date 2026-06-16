# MKWS — walidacja prędkości detonacji (CFD vs Cantera)

Walidacja termochemiczna symulacji CFD detonacji **ubogiej mieszaniny
wodorowo-powietrznej** (15% mol. H₂, φ ≈ 0,42) w rurze uderzeniowej z klinem.
Prędkości fal zmierzone z sond CFD (metoda czasu dotarcia, TOA) porównano
z przewidywaniami klasycznej teorii detonacji obliczonymi w **Canterze**.

> Praca powstała w ramach przedmiotu **Metody Komputerowe w Spalaniu** na
> Wydziale **Mechanicznym Energetyki i Lotnictwa (MEiL) Politechniki
> Warszawskiej**.

## Powiązanie z symulacją CFD

Dane wejściowe (przebiegi ciśnienia w sondach) pochodzą z symulacji CFD
prowadzonej solverem **ddtFoam** (OpenFOAM 2.1.1) w osobnym repozytorium ze
środowiskiem Docker:

👉 **https://github.com/antoniw111/docker_project**

Skrypt walidacyjny uruchamia się w zdefiniowanym tam kontenerze `cantera`
(`python:3.14-slim` + Cantera 3.2.0). Wyniki CFD trafiają do analizy przez
współdzielony wolumin `docker_root/`.

## Zawartość

| plik | opis |
|------|------|
| `detonation_validation.py` | TOA z sond + obliczenia Cantery (szok zamrożony, CJ) |
| `raport_detonacja.tex` | raport (LaTeX, `pdflatex`) |
| `raport_detonacja.pdf` | skompilowany raport |
| `fig_pt.pdf`, `fig_xt.pdf` | wykresy ciśnienia i diagram x–t |
| `przed_zapl_*.png`, `po_zapl_*.png` | pole temperatury przy klinie (przed/po zapłonie) |
| `video_5fps.avi` | animacja przebiegu symulacji z ParaView (5 fps) |

### Animacja

`video_5fps.avi` to animacja (5 kl./s, eksport z ParaView) pokazująca ewolucję
pola w czasie: nadbieg fali padającej, jej ogniskowanie na wierzchołku klina
(refleksja Macha) oraz inicjację i propagację detonacji. Stanowi materiał
poglądowy uzupełniający statyczne klatki z raportu (`przed_zapl_*` / `po_zapl_*`).

## Co liczy skrypt

- `W`   — prędkość fali padającej z sond (TOA, pierwsze narastanie, kierunek +x)
- `D`   — prędkość detonacji z sond (czas piku, kierunek −x od klina)
- `u_p` — prędkość gazu za falą padającą (Cantera, szok zamrożony)
- `D_CJ`— prędkość detonacji Chapmana–Jougueta (równowagowy Hugoniot)
- `D_lab = D_CJ − u_p` — prędkość detonacji w układzie laboratorium (do porównania z CFD)

## Uruchomienie

W kontenerze `cantera` z repo `docker_project`, w katalogu zawierającym skrypt
i plik z sondami `p_combined_probes.csv` (eksport z ParaView):

```bash
python detonation_validation.py
```

Zależności: `cantera`, `numpy`, `scipy` (SDToolbox **nie** jest potrzebny).
Konfiguracja (ścieżka CSV, mechanizm, skład `X`, `T0`, `P0`, współrzędne sond)
znajduje się na początku [`detonation_validation.py`](detonation_validation.py).
Skrypt wypisuje wyniki na konsolę i zapisuje `walidacja_wyniki.csv`.

> **Cantera 3.x** używa mechanizmów `.yaml` (np. `gri30.yaml`) — format `.cti`
> został usunięty.

## Wyniki (przypadek 15% H₂, T₀ = 300 K)

- Fala padająca: `W = 564 m/s`, `M = 1,50`, `P₂ = 2,54 bar` (≈ plateau CFD ~2,5 bar), `u_p = 263 m/s`
- Detonacja: `D_CJ = 1516 m/s`, **`D_lab = 1261 m/s`** vs CFD `1194–1319 m/s`

Pełen opis metodyki i dyskusja — w [`raport_detonacja.pdf`](raport_detonacja.pdf).
