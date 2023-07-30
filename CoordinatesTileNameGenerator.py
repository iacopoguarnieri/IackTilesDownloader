import mercantile
import time
import os
from datetime import datetime

# Variabili di programma
revision = "1.0.0"
date_revision = "2023.07.30"
# File contenente tutte le coordinate
file_path = "latLon.txt"
# File che conterrà tutti gli URL delle tiles da scaricare
tiles_file_path = "tilesName.txt"
# Cartella contenente i file che crea il programma
fileFolder = "File"
# Cartella di log
folder = "Log"
# File di log
logFilePath = "CoordinatesTileNameGeneratorLog.txt"

# Funzione che ricava l'URL della tile in base a latitudine, longitudine e zoom
def get_tile_url(latitude, longitude, zoom):
    # Ottengo il nome della tile in base ad una coordinata specifica e livello di zoom
    tile = mercantile.tile(longitude, latitude, zoom)
    # Genero l'URL della tile
    url = f"https://a.tile.openstreetmap.org/{zoom}/{tile.x}/{tile.y}.png"
    # Ritorno l'URL
    return url

# Funzione che ordina e rimuove i duplicati delle righe di un file
def order_and_remove_duplicates(file_path):
    # Leggo tutte le righe del file
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    # Eseguo un sort per ordinarle (in base al livello di zoom)
    sorted_lines = sorted(lines)

    # Uso un set per tenere traccia delle righe già viste
    seen_lines = set()

    # Creo una nnuova lista con le righe uniche preservando l'ordine
    unique_lines = []
    for line in sorted_lines:
        if line not in seen_lines:
            seen_lines.add(line)
            unique_lines.append(line)

    # Scrivo le righe uniche nel file
    with open(file_path, 'w') as file:
        file.write("\n".join(unique_lines))

# Funzione che controlla se una stringa è già presente in un array, entrambi dati come parametri in ingresso
def is_string_not_present(array, string_to_check):
    return string_to_check not in array

# Funzione che appende una riga di log nel file MapCoordinatesExtractorLog.txt
def appendInLogFile(line):
    # Apro il file in modalità 'a+' mode (appende o crea il file se non esiste)
    with open(folder + "/" + logFilePath, "a+") as file:
        # Posiziono il cursore del file all'inizio del file stesso
        file.seek(0)
        # Leggo il contenuto del file per verificare che sia vuoto
        content = file.read()
        # Se non è vuoto posiziono il cursore alla fine del file
        if content:
            # Mi posiziono alla fine del file
            file.seek(0, 2) 
            
        # Recupero il date time corrente
        current_datetime = datetime.now()
        # Formatto come stringa
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # Scrivo la stringa all'interno del file
        file.write(formatted_datetime + " - > " + line + "\n")

# Mi salvo il tempo di inizio esecuzione
start_time = time.time()

# Stampo l'avviso di inizio programma
print("START PROGRAM CoordinatesTileNameGenerator.py, rev. " + revision + " - " + date_revision)
# Aggiorno il file di log
appendInLogFile("START PROGRAM, rev. " + revision + " - " + date_revision)

# Controllo se la folder esiste già altrimenti la creo
if not os.path.exists(folder):
    os.makedirs(folder)
    print(f"Folder '{folder}' created successfully.")
else:
    print(f"Folder '{folder}' already exists.")

# Apro il file in modalità scrittura, cancella il contenuto o crea il file se non esiste
with open(fileFolder + "/" + tiles_file_path, "w") as file:
     # Il file è adesso pulito, la fine del blocco with lo chiuderà automaticamente
    pass 
# Stampo il risultato
print(f"{tiles_file_path} has been cleared or created.")

# Inizializzo una lista vuota che conterrà tutte le stringhe
unique_strings = []
# Ciclo per scaricare le immagini
with open(fileFolder + "/" + file_path, "r") as file:
    for line in file: 
        # Devo splittare la stringa in base alla , per ricavare la latitudine e la longitudine
        coordinates = line.split(",")
        # Recupero le coordinate
        latitude = float(coordinates[0])    
        longitude = float(coordinates[1])
        # Per ogni zoom calcolo l'URL
        for zoom in range(10,20):
            # Richiamo la funzione per calcolare l'URL
            tile_url = get_tile_url(latitude, longitude, zoom)
            # Controllo se l'URL è uguale ad uno dei precedenti
            if is_string_not_present(unique_strings, tile_url):
                # Appendo la stringa
                unique_strings.append(tile_url)
                # Stampo il risultato
                print(tile_url)

                # Apro il file in modalità 'a+' (appende o crea il file se non esiste)
                with open(fileFolder + "/" + tiles_file_path, "a+") as file:
                    # Posiziono il cursore del file all'inizio del file stesso
                    file.seek(0)
                    # Leggo il contenuto del file per verificare che sia vuoto
                    content = file.read()
                    # Se non è vuoto posiziono il cursore alla fine del file
                    if content:
                        # Mi posiziono alla fine del file
                        file.seek(0, 2) 
                    # Scrivo la stringa nel file
                    file.write(tile_url + "\n")

# Richiamo la funzione per ordinare le righe e rimuovere i duplicati
order_and_remove_duplicates(fileFolder + "/" + tiles_file_path)

# Mi salvo il tempo di fine esecuzione
end_time = time.time()
# Calcolo la differenza per ricavare il tempo di esecuzione del programma
execution_time = end_time - start_time
# Converto in ore, minuti e secondi
minutes, seconds = divmod(execution_time, 60)
hours, minutes = divmod(minutes, 60)
# Specifico il formato per rendere leggibile il tempo di esecuzione
readable_time = f"{int(hours)}h {int(minutes)}m {seconds:.2f}s"
# Stampo il risultato
print(f"Execution time: {readable_time}")
# Stampo l'avviso di fine programma
print("END PROGRAM MapCoordinatesExtractor.py\n")
# Aggiorno il file di log
appendInLogFile("END PROGRAM")
# Aggiorno il file di log
appendInLogFile("Execution time: " + readable_time)