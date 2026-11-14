VilágJáró

Név: Balogh Bence
Neptun-kód: ZDB7VI

A program leírása
A VilágJáró egy grafikus földrajzi kvíz két játékosnak. A játékosok felváltva
válaszolnak a kérdésekre. A végén megjelenik az eredmény és a győztes. A
főmenüből versenyt indíthatunk, országadatokat nézhetünk meg, és a korábbi
eredményeket is megtekinthetjük.

A verseny indítása után adjuk meg a két játékos nevét. A kvíz 12 országból
véletlenszerűen kiválaszt 8-at, így mindkét játékos 4 kérdést kap. Minden
kérdésnél négy, az adott országhoz tartozó város közül kell választani. A
válasz ellenőrzése után rövid magyarázat jelenik meg.

Az eredményeket a program a statisztika.txt fájlba menti. A korábbi eredmények
a főmenü Statisztika pontjában nézhetők meg.

Felépítés
main.py indítja el a grafikus ablakot.
BB_modul.py tartalmazza az országadatokat, a kvízfüggvényeket és a
BBVilagjaro osztályt.
README.md tartalmazza a program leírását és használatát.

Saját elemek
A program a tkinter grafikus modult és a random modult használja.
A saját modul neve BB_modul.py.
A saját függvények például: bb_orszag_lista, bb_kviz, bb_valaszok és
bb_eredmeny.
A saját osztály neve BBVilagjaro. Fontos metódusai: bb_indit,
bb_ellenoriz és bb_kovetkezo.
A programban a gombok kattintásai eseményeket kezelnek.