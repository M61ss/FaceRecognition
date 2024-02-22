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

listed = False
while not listed:
    # searching the name of the subject that the user is looking for around folders
    model_name = input("Chi stai cercando? ")
    if not os.path.isdir(model_name):
        # if the model_name inserted has no match, user has to define the behaviour of the program
        new_model = input("Il nome non risulta essere nella lista. Digitare 1 per aggiungerlo alla lista, 2 per cercare un altro nome: ")
        if new_model == "1":
            # create folder and add one or more images
            os.makedirs(os.getcwd() + "/" + model_name)
            file_path = input("Inserire il percorso completo dell'immagine che si desidera fornire come modello (compreso il suo nome): ")
            file_name = input("Inserire il nome dell'immagine modello: ")
            shutil.copy(file_path, model_name + "/" + file_name)
            listed = True
        else:
            continue
    else:
        listed = True
model_name += "/"

# list of all images contained into the folder about the model
models_list = os.listdir(model_name)
print("Models list: ", models_list)

# obtaining the path of the folder to inspect
exists = False
while not exists:
    inspected_directory = input("Inserisci il percorso della cartella in cui desideri cercare il soggetto: ")
    if not os.path.isdir(inspected_directory):
        print("Il percorso specificato non esiste.")
    else:
        exists = True
inspected_directory += "/"

# obtaining the list of all files contained in the folder
images_list = os.listdir(inspected_directory)
print("Images list: ", images_list)

# comparing images one by one with all models I have stored
work = True
while work:
    work = False
    for current_img in images_list:
        print("Processing " + current_img + "...")
        try:
            img = face_recognition.load_image_file(inspected_directory + current_img)
            img_encoding = face_recognition.face_encodings(img)[0]
        except IndexError:
            print("Unable to recognize at least one face into the image.\n"
                  "Moving image in " + os.getcwd() + "/Faceless...")
            if not os.path.isdir(os.getcwd() + "/Faceless"):
                print("That folder does not exists. Creating...")
                os.makedirs(os.getcwd() + "/Faceless")
            shutil.move(inspected_directory + current_img, os.getcwd() + "/Faceless/" + current_img)
            continue
        for current_model in models_list:
            try:
                model = face_recognition.load_image_file(model_name + current_model)
                model_encoding = face_recognition.face_encodings(model)[0]
            except IndexError:
                print("Unable to recognize at least one face in model: " + current_model + ".\n"
                      "Fatal error. Exiting...")
                quit()
            comparison_result = face_recognition.compare_faces([model_encoding], img_encoding)
            # counting positive and negative outcomes
            if any(comparison_result):
                # match found, copying image in Exstracted folder
                print("Match found between " + current_img + " and " + current_model)
                print("Subject has been recognized.\n"
                  "Copying image in " + os.getcwd() + "/Extracted...")
                if not os.path.isdir("Extracted"):
                    print("That folder does not exists. Creating...")
                    os.makedirs(os.getcwd() + "/Extracted")
                shutil.copy(inspected_directory + current_img, os.getcwd() + "/Extracted/" + current_img)
                break