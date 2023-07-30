import xml.etree.ElementTree as ET
import time
import os
from datetime import datetime

# Variabili di programma
revision = "1.0.0"
date_revision = "2023.07.30"
# File xml contenente tutte le coordinate da estrarre
xml_file_path = "map.xml"
# File su cui salvare le coordinate
final_file_path = "latLon.txt"
# Cartella contenente i file che crea il programma
fileFolder = "File"
# Cartella di log
folder = "Log"
# File di log
logFilePath = "MapCoordinatesExtractorLog.txt"

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
print("START PROGRAM MapCoordinatesExtractor.py, rev. " + revision + " - " + date_revision)
# Aggiorno il file di log
appendInLogFile("START PROGRAM, rev. " + revision + " - " + date_revision)

# Controllo se la folder esiste già altrimenti la creo
if not os.path.exists(folder):
    os.makedirs(folder)
    print(f"Folder '{folder}' created successfully.")
else:
    print(f"Folder '{folder}' already exists.")

# Controllo se la folder esiste già altrimenti la creo
if not os.path.exists(fileFolder):
    os.makedirs(fileFolder)
    print(f"Folder '{fileFolder}' created successfully.")
else:
    print(f"Folder '{fileFolder}' already exists.")

# Apro il file in modalità scrittura, elimina il contenuto o crea il file se non esiste
with open(fileFolder + "/" + final_file_path, "w") as file:
    # Il file è vuoto adesso, il blocco with lo chiuderà automaticamente
    pass
# Stampo l'avviso per l'utente
print(f"{final_file_path} has been cleared or created.")

# Eseguo il parsing del file XML
tree = ET.parse(xml_file_path)
# Recupero la root del file
root = tree.getroot()
# Recupero tutti i nodi
nodes = root.findall('node')
# Recupero il numero di nodi da iterare
total_iterations = len(nodes)
# Lista per salvare i tempi di esecuzione di ogni iterazione
recorded_times = []

# Eseguo le iterazioni di tutti gli elementi
for node in root.findall('node'):
    # Mi salvo il tempo di inizio esecuzione per ogni iterazione
    iteration_start_time = time.time()

    # Recupero gli elementi interni ad ogni nodo
    node_id = node.get('id')
    latitude = float(node.get('lat'))
    longitude = float(node.get('lon'))
    version = int(node.get('version'))
    timestamp = node.get('timestamp')
    changeset = int(node.get('changeset'))
    uid = int(node.get('uid'))
    user = node.get('user')
    # stampo i valori trovati
    print(f"Node ID: {node_id}")
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    print(f"Version: {version}")
    print(f"Timestamp: {timestamp}")
    print(f"Changeset: {changeset}")
    print(f"UID: {uid}")
    print(f"User: {user}")

    # Apro il file in modalità 'a+' mode (appende o crea il file se non esiste)
    with open(fileFolder + "/" + final_file_path, "a+") as file:
        # Posiziono il cursore del file all'inizio del file stesso
        file.seek(0)
        # Leggo il contenuto del file per verificare che sia vuoto
        content = file.read()
        # Se non è vuoto posiziono il cursore alla fine del file
        if content:
            # Mi posiziono alla fine del file
            file.seek(0, 2) 
        # Scrivo la stringa all'interno del file
        file.write(str(latitude) + "," + str(longitude) + "\n")

    # Mi salvo il tempo di fine esecuzione per ogni iterazione
    iteration_end_time = time.time()
    # Calcolo il tempo di esecuzione dell'iterazione attuale e lo aggiungo alla lista
    iteration_time = iteration_end_time - iteration_start_time
    recorded_times.append(iteration_time)
    # Calcolo il tempo medio di esecuzione per iterazione
    average_time_per_iteration = sum(recorded_times) / len(recorded_times)
    # Calcolo il tempo di esecuzione per le iterazioni rimanenti
    remaining_iterations = total_iterations - len(recorded_times)
    # Do una stima del tempo totale rimanente
    remaining_time = remaining_iterations * average_time_per_iteration
    # Stampo i risultati
    print(f"Average time per iteration: {average_time_per_iteration:.4f} seconds")
    print(f"Total time remaining: {remaining_time:.2f} seconds")
    print("----------------------\n")

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
