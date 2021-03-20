# FPL

Skrypt napisany w języku Python zbierający informacje na temat mini-ligi w grze przeglądarkowej Fantasy Premier League.

### Użyte technologie 

• PostgreSQL do przechowywania danych ściągniętych z API gry,

• Python do napisania skryptu.

### Użyte biblioteki 

• pandas do obsługi data.frame i operacji na nich,

• sqlite3 do tworzenia zapytań SQL w Pythonie,

• requests do zbierania danych z API,

• seaborn oraz matplotlib do wykonania wykresów.

### Opis gry

Skrypt ten pobiera dane dotyczące różnych parametrów numerycznych związanych z występami piłkarzy w angielskiej lidze piłkarskiej - Premier League. Piłkarze otrzymują punkty za "pozytywny" wpływ na grę, czyli np. strzelenie bramki, asystę przy bramce, ilość obron czy zachowanie "czystego konta". Tracą je przy "negatywnym" wpływie na grę, czyli np. za żółtą lub czerwoną kartkę lub co dwa stracone gole (w przypadku obrońców i bramkarzy). Każdy z piłkarzy kosztuje określoną cenę wirtualnej waluty, a każdy z graczy ma ograniczoną ilość tej waluty. Startowa wartość to 100 milionów. Ceny piłkarzy mogą wzrastać lub maleć, więc wartość zespołu każdego z graczy będzie się zmieniać. Samo stworzenie zespołu stanowi pewien problem optymalizacyjny, ponieważ można wybrać jedynie ograniczoną ilość piłkarzy na każdą z pozycji. 

### Opis działania

Na początku sezonu została zainicjalizowana baza danych zawierające wszystkie potrzebne dane dotyczące graczy zebranych w mini-lidze. Następnie, co kolejkę do bazy danych zapisywane są dane dotyczące punktów zdobytych przez piłkarzy oraz ich wartości, wybór piłkarzy przez każdego z graczy oraz punkty zdobyte przez każdego z graczy. Następnie dane te są zbierane do tabel, które stanowią klasyfikację generalną ligi oraz klasyfikację kolejki. Wszystkie potrzebne dane eksportuję do pliku csv, który potem scalam w plik xlsx na podstawie którego wykonuję małą wizualizację w Tableau Public (dostępna pod linkiem - http://tabsoft.co/2NEkSzQ). Co kolejkę również piszę krótki raport z najważniejszymi wydarzeniami w naszej lidze, który jest udostępniany graczom (przykładowy raport - https://pastebin.pl/view/350affc6).

Z baz SQL korzystam tylko i wyłącznie do przechowywania danych. Nie przeprowadzam żadnych operacji na bazach oraz nie dbam o ich strukturę ponieważ wszystko mam dopilnowane w skrypcie Pythona. W następnym sezonie (rozpoczynającym się we wrześniu 2021) planuję zmienić podejście do tego skryptu. Stworzę klucze główne oraz obce, które będą służyć jako dodatkowa walidacja bazy danych. Postaram się również wykonywać więcej operacji na bazach danych, a nie jak dotychczas z pomocą biblioteki Pandas.

Planuję stworzenie algorytmu optymalizującego, który sam będzie tworzył zespół na podstawie metryk udostępnionych przez twórców gry oraz z zewnętrznych stron (np. understat.com)
