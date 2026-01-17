Projekt SCADA – wykonany w języku Python z wykorzystaniem biblioteki PyQt5: Aplikacja wizualizująca proces napełniania zbiorników.

Funkcje:
- Wizualizacja przepływu cieczy pomiędzy zbiornikami;
- Sterowanie zaworami oraz obsługa alarmów poziomu (LOW / HIGH);
- Symulacja automatycznego procesu;
- Prezentacja elementów dynamicznych (pompa).

Uruchomienie -- python main.py

Opis działania systemu:
- Przepływ grawitacyjny -- ze zbiornika nr 1 do zbiornika nr 2;
- Przepływ sterowany pompą -- ze zbiornika nr 2 do zbiornika nr 3;
- Rozgałęzienie -- ze zbiornika nr 3: 1/2 trafia do zbiornika nr 4 oraz 1/2 - do zbiornika nr 5.
  Przepływ cieczy jest wizualizowany niebieskim kolorem w rurach.
  Proces przebiega automatycznie, sterowany zegarem (QTimer).

Dla każdego zbiornika generowane są alarmy:
- LOW - poziom ≤ 5% pojemności;
- HIGH - poziom ≥ 95% pojemności.
  Alarmy są sygnalizowane wizualnie (kolor ramki zbiornika) oraz prezentowane w osobnym oknie „Alarmy systemowe”.

Projekt oparty jest na klasach:
- Zbiornik -- reprezentuje zbiornik procesu (pojemność, poziom, alarmy);
- Rura -- wizualizacja połączeń rurowych i przepływu;
- Pompa -- element dynamiczny wpływający na proces;
- SymulacjaKaskady -- główne okno aplikacji i logika symulacji.

Przyciski sterujące:
- Start / Stop symulacji;
- Pompa ON / OFF;
- Alarmy;
- Ręczne napełnianie i opróżnianie odpowiednich zbiorników.
  
Autor -- Anastasiia Heraimovych, 206470, ARiSS sem. 3, gr. 2a

