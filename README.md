# FPL

## English

A script written in Python to collect information about the mini-league in the browser game Fantasy Premier League.

### Technologies used 
- SQL to store data pulled from the game API,
- Python to write the script

### Libraries used 

- pandas to handle data.frames and operations on them,
- sqlite3 to create SQL queries in Python,
- requests to collect data from the API,
- seaborn and matplotlib to make graphs.

### Game description
This script collects data on a variety of numerical parameters related to the performances of footballers in the English football league, the Premier League. Players receive points for "positive" performances such as goals scored, assists, saves and "clean sheets". They lose points for a "negative" influence on the game, such as a yellow or red card or every two goals conceded (in the case of defenders and goalkeepers). Each player costs a certain price of the virtual currency and each player has a limited amount of this currency. The starting value is 100 million. Player prices can increase or decrease, so the value of each player's team will vary. Creating the team itself poses some optimisation problems, as only a limited number of players can be selected for each position. 

### Script description
At the start of the season, a database has been initialised containing all the necessary data on the players participating in the mini-league.  Then, every gameweek, the data about points scored by footballers and their values, the selection of footballers by each player and the points scored by each player in a gameweek are written to the database. This data is then compiled into tables which are the overall league standings and the gameweek standings. I export all the necessary data to a csv file, which I then merge into an xlsx file based on which I make a small visualisation in Tableau Public (available at http://tabsoft.co/2NEkSzQ). Every round I also write a short report with the most important events in our league, which is made available to the players (sample report - https://pastebin.pl/view/350affc6).

I use SQL databases only for data storage. I don't perform any operations on the databases and I don't worry about their structure because everything is taken care of in a Python script. Next season (starting September 2021) I plan to change my approach to this script. I will create primary and foreign keys that will serve as additional database validation. I will also try to use more database queries rather than using the Pandas library as before.
I also plan to create an optimization algorithm that will create a team on its own based on metrics provided by the game developers and scraped from external sites (e.g. understat.com)

## Polski

Skrypt napisany w języku Python zbierający informacje na temat mini-ligi w grze przeglądarkowej Fantasy Premier League.

### Użyte technologie 

- SQL do przechowywania danych ściągniętych z API gry,
- Python do napisania skryptu.

### Użyte biblioteki 

- pandas do obsługi data frame i operacji na nich,
- sqlite3 do tworzenia zapytań SQL w Pythonie,
- requests do zbierania danych z API,
- seaborn oraz matplotlib do wykonania wykresów.

### Opis gry

Skrypt ten pobiera dane dotyczące różnych parametrów numerycznych związanych z występami piłkarzy w angielskiej lidze piłkarskiej - Premier League. Piłkarze otrzymują punkty za "pozytywny" wpływ na grę, czyli np. strzelenie bramki, asystę przy bramce, ilość obron czy zachowanie "czystego konta". Tracą je przy "negatywnym" wpływie na grę, czyli np. za żółtą lub czerwoną kartkę lub co dwa stracone gole (w przypadku obrońców i bramkarzy). Każdy z piłkarzy kosztuje określoną cenę wirtualnej waluty, a każdy z graczy ma ograniczoną ilość tej waluty. Startowa wartość to 100 milionów. Ceny piłkarzy mogą wzrastać lub maleć, więc wartość zespołu każdego z graczy będzie się zmieniać. Samo stworzenie zespołu stanowi pewien problem optymalizacyjny, ponieważ można wybrać jedynie ograniczoną ilość piłkarzy na każdą z pozycji. 

### Opis działania

Na początku sezonu została zainicjalizowana baza danych zawierające wszystkie potrzebne dane dotyczące graczy zebranych w mini-lidze. Następnie, co kolejkę do bazy danych zapisywane są dane dotyczące punktów zdobytych przez piłkarzy oraz ich wartości, wybór piłkarzy przez każdego z graczy oraz punkty zdobyte przez każdego z graczy. Następnie dane te są zbierane do tabel, które stanowią klasyfikację generalną ligi oraz klasyfikację kolejki. Wszystkie potrzebne dane eksportuję do pliku csv, który potem scalam w plik xlsx na podstawie którego wykonuję małą wizualizację w Tableau Public (dostępna pod linkiem - http://tabsoft.co/2NEkSzQ). Co kolejkę również piszę krótki raport z najważniejszymi wydarzeniami w naszej lidze, który jest udostępniany graczom (przykładowy raport - https://pastebin.pl/view/350affc6).

Z baz SQL korzystam tylko i wyłącznie do przechowywania danych. Nie przeprowadzam żadnych operacji na bazach oraz nie dbam o ich strukturę ponieważ wszystko mam dopilnowane w skrypcie Pythona. W następnym sezonie (rozpoczynającym się we wrześniu 2021) planuję zmienić podejście do tego skryptu. Stworzę klucze główne oraz obce, które będą służyć jako dodatkowa walidacja bazy danych. Postaram się również wykonywać więcej operacji na bazach danych, a nie jak dotychczas z pomocą biblioteki Pandas.

Planuję również stworzenie algorytmu optymalizującego, który sam będzie tworzył zespół na podstawie metryk udostępnionych przez twórców gry oraz z zewnętrznych stron (np. understat.com)
