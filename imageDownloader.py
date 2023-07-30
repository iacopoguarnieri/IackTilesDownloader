import urllib.request
import os
import time
from datetime import datetime

# Variabili di programma
revision = "1.0.0"
date_revision = "2023.07.30"
# Cartella contenente i file che crea il programma
fileFolder = "File"
# Cartella di log
folderLog = "Log"
# File di log
logFilePath = "imageDownloaderLog.txt"
# Nome del file che contiene i link delle tiles da scaricare
file_path = "tilesName.txt"

# Funzione che appende una riga di log nel file MapCoordinatesExtractorLog.txt
def appendInLogFile(line):
    # Apro il file in modalità 'a+' mode (appende o crea il file se non esiste)
    with open(folderLog + "/" + logFilePath, "a+") as file:
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

# Funzione che convert secondi in minuti e secondi
def format_time(seconds):
    # Convert the total seconds to hours, minutes, and seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # Create a formatted time string
    time_string = ""
    if hours > 0:
        time_string += f"{hours} hours "
    if minutes > 0:
        time_string += f"{minutes} minutes "
    time_string += f"{seconds:.2f} seconds"

    return time_string

# Mi salvo il tempo di inizio esecuzione
start_time = time.time()

# Stampo l'avviso di inizio programma
print("START PROGRAM imageDownloader.py, rev. " + revision + " - " + date_revision)
# Aggiorno il file di log
appendInLogFile("START PROGRAM, rev. " + revision + " - " + date_revision)

# Cartella principale che definisce il luogo del porto
city = "Download"
# Controllo se la folder esiste già altrimenti la creo
if not os.path.exists(city):
    os.makedirs(city)
    print(f"Folder '{city}' created successfully.")
else:
    print(f"Folder '{city}' already exists.")

# Controllo se la subfolder esiste già altrimenti la creo
if not os.path.exists(city  + "/tiles"):
    os.makedirs(city + "/tiles")
    print(f"Folder 'tiles' created successfully.")
else:
    print(f"Folder 'tiles' already exists.")

# Variabile contatore
i = 1

# Lista per salvare i tempi di esecuzione di ogni iterazione
recorded_times = []
# contatore delle righe totali del file
line_count = 0
# Ciclo per contare tutte le righe del file
with open(fileFolder + "/" + file_path, "r") as file:
    line_count = len(list(file))

# Ciclo per scaricare le immagini
with open(fileFolder + "/" + file_path, "r") as file:
    for line in file:
        # Mi salvo il tempo di inizio esecuzione per ogni iterazione
        iteration_start_time = time.time()

        # Rimuovo il \n dalla linea
        line = line.replace("\n", "")
        # Stampo l'avviso di avvio download immagine per l'utente
        print(f"\nStart downloading image {i}/{line_count}: " + line)

        # Url dell'immagine da scaricare
        # Esempio: imageUrl = "https://c.tile.openstreetmap.org/10/540/372.png"
        imageUrl = line

        # Devo splittare la stringa in base al / per ricavare cartella principale, sottocartella e nome del file
        words = imageUrl.split("/")
        # Esempio: words -> ['https:', '', 'c.tile.openstreetmap.org', '10', '540', '372.png']
        #print(words)

        # Cartella principale
        folder = words[3]
        # Sottocartella
        subfolder = words[4]
        # Nome con cui salvare l'immagine da scaricare
        imageFileName = words[5].replace("\n", "")

        # Controllo se la folder/subfolder esiste già altrimenti la creo
        if not os.path.exists(city + '/tiles/' + folder  + "/" + subfolder):
            os.makedirs(city + '/tiles/' + folder + "/" + subfolder)
            print(f"Folder {folder}/{subfolder} created successfully.")
        #else: print(f"Folder {folder}/{subfolder} already exists.")

        # Creo il percorso con il nome del file
        imagePathAndName = city + '/tiles/' + folder + '/' + subfolder + '/' + imageFileName
        # Apro l'url
        opener = urllib.request.URLopener()
        # Aggiungo l'header all'url
        opener.addheader('User-Agent', 'whatever')
        # Salvo l'immagine
        filename, headers = opener.retrieve(imageUrl, imagePathAndName)

        # Attendo 0.5 secondi prima di scaricare la nuova immagine
        time.sleep(0.5)

        # Mi salvo il tempo di fine esecuzione per ogni iterazione
        iteration_end_time = time.time()
        # Calcolo il tempo di esecuzione dell'iterazione attuale e lo aggiungo alla lista
        iteration_time = iteration_end_time - iteration_start_time
        recorded_times.append(iteration_time)
        # Calcolo il tempo medio di esecuzione per iterazione
        average_time_per_iteration = sum(recorded_times) / len(recorded_times)
        # Calcolo il tempo di esecuzione per le iterazioni rimanenti
        remaining_iterations = line_count - len(recorded_times)
        # Do una stima del tempo totale rimanente
        remaining_time = remaining_iterations * average_time_per_iteration

        # Format the output for better readability
        formatted_average_time = format_time(average_time_per_iteration)
        formatted_total_time = format_time(remaining_time)
        # Stampo i risultati
        print(f"Image {i}/{line_count} download compleated: " + imagePathAndName)
        print(f"Average time per iteration: {formatted_average_time}")
        print(f"Total time remaining: {formatted_total_time}")
        print("----------------------\n")

        # Incremento il contatore
        i += 1      

print("\nDownload compleated")
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
print("END PROGRAM imageDownloader.py\n")
# Aggiorno il file di log
appendInLogFile("END PROGRAM")
# Aggiorno il file di log
appendInLogFile("Execution time: " + readable_time)