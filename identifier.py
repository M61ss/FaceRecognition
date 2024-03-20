import face_recognition
import os
import shutil

'''
Idea: creare un file name_list_file che contenga i nomi delle persone delle quali si ha almeno un volto. Ad ogni persona è associata una cartella
con lo stesso nome. All'interno di ogni cartella ci sono tutte le foto in cui compare la persona.
Il programma all'avvio crea una lista:
    1. lista dei nomi dei file contenuti in ogni cartella (esempio: Mattia/20201230.jpeg)
Il riconoscimento facciale avverrà facendo il confronto dell'immagine fornita con tutte le immagini presenti nelle cartelle e, in caso di riscontri,
si stabilirà il risultato in base alle percentuali di corrispondenza
'''

# --------------------------------------------------------------

# Function that requires file's path for copy them
def FileCopy():
    while True:
        src_path = input("Inserire il percorso sorgente del file che si desidera copiare (compreso il nome del file): ")
        if os.path.isdir(src_path) == False:
            continue
        dst_path = input("Inserire il percorso di destinazione del file che si desidera copiare (compreso il nome del file): ")
        break
    shutil.copy(src_path, dst_path)

# --------------------------------------------------------------

# Function to research model_name among folders
# Args:
#   - name: name of the folder where are stored models
# Returns:
#   - True: on existing folder (or correctly created)
#   - False: on unexisting folder or on error
def SelectSubject(name):
    if not os.path.isdir(name):
        # If the model_name inserted has no match, user has to define the behaviour of the program
        create_new = input("Il nome non risulta essere nella lista dei soggetti memorizzati. Digitare 1 per aggiungerlo alla lista, 2 per cercare un altro nome: ")
        if create_new == "1":
            # Create folder
            os.makedirs(os.getcwd() + "/" + name)
            # Requesting path of an image which represents the subject
            print("Ora seguire le istruzioni per inserire i file che si desidera utilizzare come modelli per i confronti.")
            FileCopy()
        else:
            return False
    return True

# --------------------------------------------------------------

# Function that preload all models
# Args:
#   - path: path of the folder that contains all model's images
#   - models_list: list of all names of all images contained in the model's folder
# Returns:
#   - model_encoding_list: list of encodings for every image 
def LoadModels(path, models_list):
    try:
        model_encodings_list = []
        for current_model in models_list:
            model_load_list = face_recognition.load_image_file(path + current_model)
            model_encodings_list.append(face_recognition.face_encodings(model_load_list)[0])
    except IndexError:
        print("[ERROR] Unable to recognize at least one face in model: " + current_model + ".\n"
                "Fatal error. Exiting...")
        quit()
    return model_encodings_list

# --------------------------------------------------------------


# ------- MAIN PROGRAM -------
listed = False
while not listed:
    # Searching the name of the subject that the user is looking for around folders
    model_name = input("Chi stai cercando? ")
    listed = SelectSubject(model_name)
# Saving the complete path of the folder that contains all model's images
model_path = os.getcwd() + "/" + model_name + "/"

# List of all images contained into the folder about the model
models_list = os.listdir(model_name)
print("Models list: ", models_list)
# List of all encodings of model's images
print("Loading model's images...")
model_encodings_list = LoadModels(model_path, models_list)

# Obtaining the path of the folder to inspect
while True:
    inspected_path = input("Inserisci il percorso della cartella in cui desideri cercare il soggetto: ")
    if not os.path.isdir(inspected_path):
        print("[WARNING] Il percorso specificato non esiste.")
        continue
    break
# Completing path of the folder that contains image to inspect
inspected_path += "/"

# Obtaining the list of all files contained in the folder
images_list = os.listdir(inspected_path)
print("Images list: ", images_list)

# Path for 'Faceless' and 'Extracted' folders
# Faceless: images of which is impossible to find at least a face
# Extracted: images that matches with at least one model
faceless_path = os.getcwd() + "/Faceless"
extracted_path = os.getcwd() + "/Extracted"

# Scrolling images one by one
for current_img in images_list:
    # Checking that the image taken in exam has at least one face into itself
    try:
        print("Processing " + current_img + "...")
        img = face_recognition.load_image_file(inspected_path + current_img)
        img_encoding = face_recognition.face_encodings(img)[0]
    except IndexError:
        # In case it does not contain any face, I move it into the folder 'Faceless' (creating it in case it doesn't exists)
        print("[WARNING] Unable to recognize at least one face into the image.\n"
            "Moving image in " + faceless_path + "...")
        if not os.path.isdir(faceless_path):
            print("That folder does not exists. Creating...")
            os.makedirs(faceless_path)
        shutil.move(inspected_path + current_img, faceless_path + "/" + current_img)
        continue
    # Comparing all models encodings with the encoding of the current image
    print("Comparing...")
    comparison_result = face_recognition.compare_faces(model_encodings_list, img_encoding)
    # Verifying if there are any matches
    if any(comparison_result):
        # Match found, moving image in Extracted folder (creating it in case it doesn't exists)
        print("*!*" + model_name + " has been recognized in " + current_img + ". *!*\n"
            "Moving image in " + extracted_path + "...")
        if not os.path.isdir("Extracted"):
            print("That folder does not exists. Creating...")
            os.makedirs(extracted_path)
        shutil.move(inspected_path + current_img, extracted_path + "/" + current_img)
    else:
        print("No match found for " + current_img)