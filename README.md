# Instalacja Bibliotek
w pliku requirements.text  znajdują się biblioteki do głownego pliku pythonowego i notebookow

użyj komendy ```pip install -r requirements.txt ```

W sekcji data projektu jest cocktail_processed.json czyli przetworzony juz zbiór danych

Przebieg zadania

Projekt jest podzielony na przetwarzane kolumny

Category: Sprawdzamy jakie sa kategorie a nastepnie wykonujemy one-hot encoding  

Glass: Sprawdzamy kategorie i zliczamy ilosc ich wystapien,te rzadziej uzywane wrzucamy to kolumny others wykonujemy one-hot encoding

Tags: Wiekszosc tagów jest pusta, Zliczamy ich wystapienia.Wychodzi na to ze 3 sa najczęstsze reszta ma marginalne znaczenie. Tworzymy kolumny dla tych najpopularniejszych i oznaczamy o albo w zaleznosci od wystąpienia  

Instructions: Z tej kolumny staramy się wyciągnąć informacje jak trudny jest dany drink do przyrzadzenia i jakich narzędzi wymaga. Tworzymy kolumne zliczajaca dlugosc instrukcji   
a nastepnie sprawdzamy najczesciej wystpujace slowa. Okazuje sie ze czesto uzywane sa stir shake Strain i garnish. Tworzymy kolumny które daja nam informacje czy potrzebujemy łyzki barmańskiej sitka albo shakera 
oraz czy nasz drink jest dekorowany->garnish.

Ingredients: Tutaj pozyskujemy informacje o smaku koktajlu, jego bazy alkoholowej i jego mocy co pomoze w klasteryzacji. Bierzemy nazwy składników dzielimy je na smaki a nastepnie tworzymy kolumny zliczajace 
liczbe wystapien skladników o danym smaku np Sweet_count.Ilosc składników o danym smaku determinuje smak koktajlu. Nastepnie Sprawdzamy typy i wydzielamy kolumny głownego alkoholu jak Whiskey Vodka Gin
i oznaczamy 0 albo 1.Na koniec wyszukujemy miary i konwertujemy je na ml.Wyliczamy wielkosc koktajlu ilosc alkoholu a na koncu jego moc.  


W projekcie są 2 notebooki jeden od wizualizacji danych początkowych a drugi od klasteryzacji i ewaluacji jej wynikow. Klasteryzacje została wykonana za pomocą K-means bo dawał najlepsze rezultaty 

