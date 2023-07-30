******* PREREQUISITI PER L'ESECUZIONE DEGLI SCRIPT PYTHON *******
- Phyton ver. 3
- modulo request (installato tramite comando pip3 install requests)

******* PROCEDURA D'USO PER SCARICARE LE TILES ******* 
1. Recarsi sul sito: https://www.openstreetmap.org/
2. Cliccare su 'Esporta'
3. Inserire le coordinate della porzione di mappa che si vuole esportare
4. Premere su 'Overpass API'
5. Salvare il file esportato con il nome 'map.xml' (l'estensione è importante che sia presente)
6. Spostare il file nella cartella dov'è presente il programma in python da eseguire
7. Eseguire il programma denominato IacksTileDownloader.py
ATTENZIONE: è importante che durante l'esecuzione del programma il computer non vada in sospensione ò in blocco schermo altrimenti bisogna far ripartire il programma dall'inizio

******* SPIEGAZIONE PROGRAMMI *******
MapCoordinatesExtractor.py -> dato il file denomaito 'map.xml' crea un file denominato 'latLon.txt' contenente tutte le coordinate presenti nel file xml.
CoordinatesTileNameGenerator.py -> dato il file denominato 'latLon.txt' ricava l'URL delle immagini delle coordinate di opestreetmap e le salva il un file denominato 'tilesName.txt'.
imageDownloader.py -> dato il file denominato 'tilesName.txt' contenente tutti gli URL delle immagini le scarica e le salva sotto determinate cartelle impostate dall'URL stesso.
IackTilesDownloader.py - > esegue in sequenza tutti e tre i prcedenti programmi