import tkinter as tk
from tkinter import ttk
from PIL import Image , ImageTk #Pour l'icon
import csv
from tkcalendar import DateEntry 
import subprocess



#Enregistrer dans le table cron
def enregistrer_nouvelle_tache(nouvelle_tache):

    tache_cron = ""
    type_planification = ["Exécution unique","Tous les jours","Chaque semaine","Chaque mois"]
    ##Ecrire les tâches sur le table cron
    #Lire le crontab actuel
    resultat = subprocess.run(['crontab','-l'],capture_output=True,text=True)
    crontab_actuel=resultat.stdout
    #Ajouter une nouvelle tâche 
        #Forme de tâche cron : 
        # * * * * * commande
        # │ │ │ │ │
        # │ │ │ │ └── Jour de la semaine (0-7) [0 et 7 = dimanche]
        # │ │ │ └──── Mois (1-12)
        # │ │ └────── Jour du mois (1-31)
        # │ └──────── Heure (0-23)
        # └────────── Minute (0-59)
    
    h,min=nouvelle_tache[4].split(":")
    anne,mois,jour=str(nouvelle_tache[3]).split("-")
    #Forme de chaque tache dans le table cron 
    #   * * * * * commande      #Nom de la tâche:Type de planification
    if nouvelle_tache[2]==type_planification[0]:
        tache_cron =min + " " + h + " " + jour + " " + mois + " " +  "*" + " " + nouvelle_tache[1] + "\t#" + nouvelle_tache[0] + ":" + nouvelle_tache[2] + "\n"  
    elif nouvelle_tache[2] == type_planification[1]:
        tache_cron = min + " " + h + " " +  "*" + " " + "*" + " "+ "*" + " " + nouvelle_tache[1] + "\t#" + nouvelle_tache[0] + ":" + nouvelle_tache[2] + "\n"
    elif nouvelle_tache[2] == type_planification[2]:
        tache_cron = min + " " + h + " " + "*" + " " + "*" + " " + nouvelle_tache[6] + " " + nouvelle_tache[1] + "\t#" + nouvelle_tache[0] + ":" + nouvelle_tache[2] + "\n"  
    elif nouvelle_tache[2] == type_planification[3]:
        tache_cron =min + " " + h + " " +  nouvelle_tache[5] + " " + "*" + " " + "*" + " " + nouvelle_tache[1] + "\t#" + nouvelle_tache[0] + ":" + nouvelle_tache[2] + "\n"  
    nouveau_crontab = crontab_actuel + tache_cron

    #Écrire le nouveau crontab 
    subprocess.run(['crontab','-'],input=nouveau_crontab,text=True)

def ajouter_une_tache(*args):
    retoure=None
    tache=["","","","00/00/00","00:00","*","*"]
    jours=["Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"]
    type_planification = ["Exécution unique","Tous les jours","Chaque semaine","Chaque mois"]
    fenetre = tk.Tk()
    if args :
        fenetre.title(args[0])
    else: 
        fenetre.title("Nouvelle tâche")
    fenetre.geometry("500x275")
    fenetre.columnconfigure(1, weight=1)
    #Nom de la tâche
    tk.Label(fenetre, text="Nom de la tâche").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    nom_entry = tk.Entry(fenetre)
    nom_entry.grid(row=0, column=1, sticky="we", padx=10, pady=5)
    #Commande  à exécuter
    tk.Label(fenetre, text="Commande").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    commande_entry = tk.Entry(fenetre)
    commande_entry.grid(row=1, column=1, sticky="we", padx=10, pady=5)
    #Type de planification
    tk.Label(fenetre, text="Type de planification").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    type=ttk.Combobox(fenetre,values=type_planification)
    type.grid(row=2, column=1, sticky="we", padx=10, pady=5)
    #Date
    tk.Label(fenetre, text="Date").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    date_entry = DateEntry(fenetre, date_pattern="dd/mm/yyyy")
    date_entry.grid(row=3, column=1, sticky="we", padx=10, pady=5)
    #Heure
    tk.Label(fenetre, text="Heure").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    heure = tk.Spinbox(fenetre, from_=0, to=23, width=5)
    heure.grid(row=4, column=0, sticky="e", padx=10)
    minute = tk.Spinbox(fenetre, from_=0, to=59, width=5)
    minute.grid(row=4, column=1, sticky="w", padx=10)
    #Jour du mois
    tk.Label(fenetre, text="Jour du mois").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    jour_mois = tk.Spinbox(fenetre, from_=0, to=31, width=5)
    jour_mois.grid(row=5, column=0, sticky="e", padx=10)
    #Jour de la semaine
    tk.Label(fenetre, text="Jour de la semaine").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    jour_semaine=ttk.Combobox(fenetre,values=jours)
    jour_semaine.grid(row=6, column=1, sticky="we", padx=10, pady=5)
    
    def annuler():
        nonlocal retoure
        retoure=-1
        fenetre.destroy()

    #Recuperer toutes les informations sur la tâche 
    def enregistrer():
        nonlocal retoure
        tache[0] = nom_entry.get()
        tache[1] = commande_entry.get()
        tache[2] = type.get()
        tache[3] = date_entry.get_date()
        tache[4] = heure.get() + ":" + minute.get()
        tache[5] = jour_mois.get()
        for i, jour in enumerate(jours):
            if jour == jour_semaine.get():
                tache[6] = str(i)
                break
        enregistrer_nouvelle_tache(tache)
        retoure = 1
        fenetre.destroy()


    #Boutons Annuler , Enregistrer
    btn_annuler=tk.Button(fenetre, text="Annuler",bg="#222121",width=25,fg="white",command=annuler)
    btn_annuler.grid(row=8,column=0,sticky='w')
    btn_enregistrer=tk.Button(fenetre, text="Enregistrer",bg="#222121",width=25,fg="white",command=enregistrer)
    btn_enregistrer.grid(row=8,column=1,sticky='e')

    fenetre.mainloop()
    return(retoure)


def recuperer_tache_cron_dans_fichier():
    jours = ["Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"]
    type_planification = ["Exécution unique","Tous les jours","Chaque semaine","Chaque mois"]
    
    # Lire le crontab actuel
    resultat = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    lignes = resultat.stdout.splitlines()
    
    taches = []
    
    for ligne in lignes:
        # Ignorer les lignes vides ou commentaires purs
        if not ligne.strip() or ligne.strip().startswith("#"):
            continue
        
        # Séparer la partie cron du commentaire  (#Nom:Type)
        if "#" in ligne:
            partie_cron, commentaire = ligne.split("#", 1)
        else:
            continue  # Sans commentaire, on ne peut pas récupérer le nom/type
        
        partie_cron = partie_cron.strip().split()
        if len(partie_cron) < 6:
            continue
        
        # Extraire les champs cron : minute heure jour_mois mois jour_semaine commande
        minute       = partie_cron[0]
        heure        = partie_cron[1]
        jour_mois    = partie_cron[2]
        mois         = partie_cron[3]
        jour_semaine = partie_cron[4]
        commande     = " ".join(partie_cron[5:])
        
        # Extraire nom et type depuis le commentaire
        if ":" in commentaire:
            nom, type_tache = commentaire.split(":", 1)
            nom = nom.strip()
            type_tache = type_tache.strip()
        else:
            nom = commentaire.strip()
            type_tache = ""
        
        # Reconstruire date et heure
        heure_exec = heure.zfill(2) + ":" + minute.zfill(2)
        
        if type_tache == type_planification[0]:  # Exécution unique
            date_exec = f"20{mois.zfill(2)}-{mois.zfill(2)}-{jour_mois.zfill(2)}"
            # Reconstruire : année inconnue, on met les champs disponibles
            date_exec = f"??/{mois.zfill(2)}/{jour_mois.zfill(2)}"
        else:
            date_exec = "00/00/00"
        
        taches.append([nom, commande, type_tache, date_exec, heure_exec, jour_mois, jour_semaine])
    
    # Écrire dans liste_taches.csv
    with open("liste_taches.csv", "w", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        if taches:
            writer.writerows(taches)
        else:
            # Ligne par défaut si aucune tâche
            writer.writerow(["", "", "", "00/00/00", "00:00", "*", "*"])



def liste_de_taches(centre_frame):
    recuperer_tache_cron_dans_fichier()
    jours=["Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"]
    type_planification=["Exécution unique","Tous les jours","Chaque semaine","Chaque mois"]

    # Canvas
    canvas = tk.Canvas(centre_frame,bg="#4D4C4C")
    canvas.pack(side=tk.LEFT, fill="both", expand=True)
    # Barre de défilement
    scrollbar = tk.Scrollbar(centre_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    # Frame contenant les tâches
    conteneur = tk.Frame(canvas,bg="#4D4C4C")
    canvas.create_window((0, 0), window=conteneur, anchor="nw")
    conteneur.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    ##Lire le fichier liste_taches.csv qui contient toutes les tâches dans crontab -l avec leurs informations
    #Forme de liste_taches.csv : Nom de tâche,Commande à exécuter,Type de planification,Date d'exécution ,Heure d'exécution,Jour du mois , Jour de la semaine
    with open("liste_taches.csv") as fichier:
        donnes = csv.reader(fichier)
        for ligne in donnes:
            liste_frame=tk.Frame(conteneur,bg="#4D4C4C",height=80,highlightthickness=3,highlightbackground="#616164")
            liste_frame.pack(fill=tk.X,padx=50,pady=5,ipadx=310,ipady=5)
            liste_frame.pack_propagate(False)
            if ligne[2]==type_planification[0]:
                date=ligne[3]+" à "+ligne[4]
            elif ligne[2]==type_planification[1]:
                date=ligne[2]+" à "+ligne[4]
            elif ligne[2]==type_planification[2]:
                date=ligne[2]+": Tous le "+jours[int(ligne[6])] + " à " + ligne[4]
            elif ligne[2]==type_planification[3]:
                date=ligne[2]+" : Tous le "+ligne[5] + "ème jour du mois à " + ligne[4]
            commande="("+ligne[1]+")"
            #Afficher le nom , commande et date d'exécution de chque tâche 
            tache_label=tk.Label(liste_frame,text=ligne[0],font=("TkDefaultFont",12,"bold"),bg="#4D4C4C")
            tache_label.pack(fill=tk.X)
            commande_label=tk.Label(liste_frame,text=commande,fg="#AFA2A2",bg="#4D4C4C")
            commande_label.pack(fill=tk.X)
            date_label=tk.Label(liste_frame,text=date,fg="#FFFFFF",bg="#4D4C4C")
            date_label.pack(fill=tk.X)

            #Boutton pour supprimer et modifier 
            icon=ImageTk.PhotoImage(Image.open("delete.png").resize((25,25)))
            supprimer=tk.Button(liste_frame,image=icon ,width=25,height=3)
            supprimer.pack(side=tk.RIGHT,anchor='center')

#Cette fonction permet de supprimer une tâche qui contient la chaîne dans la variable "tache_a_supprimer" dans le table cron
def supprimer_une_tache_dans_table_cron(tache_a_supprimer):
    #Lire le crontab actuel
    resultat = subprocess.run(['crontab','-l'],capture_output=True,text=True)
    crontab_actuel=resultat.stdout

    #Supprimer une tâche 
    liste_tache = crontab_actuel.splitlines()
    for tache in liste_tache:
        if str(tache_a_supprimer) in tache :
            liste_tache.remove(tache)
    
    #Réecrire le nouveau crontab
    crontab_actuel="\n".join(liste_tache)+ "\n"
    subprocess.run(['crontab','-'],input=crontab_actuel,text=True)




def modifier_une_tache():
    fenetre = tk.Tk()
    fenetre.title("Nom de la tâhe")
    fenetre.geometry("350x120")
    nom_label=tk.Label(fenetre,text="Nom de la tâche / Commande ")
    nom_label.grid(row=1,column=0)
    nom_entry=tk.Entry(fenetre)
    nom_entry.grid(row=2, column=0, columnspan=2, sticky="we", padx=5,pady=10)
    tache=nom_entry.get()
    def annuler():
        fenetre.destroy()
    def enregistrer():
        fenetre.destroy()
        retoure=ajouter_une_tache("Modification d'une tâche")
        if retoure==1:
            supprimer_une_tache_dans_table_cron(tache)

    btn_annuler=tk.Button(fenetre, text="Annuler",bg="#222121",width=15,fg="white",command=annuler)
    btn_annuler.grid(row=3,column=0,sticky='w',pady=10)
    btn_enregistrer=tk.Button(fenetre, text="Modifier",bg="#222121",width=15,fg="white",command=enregistrer)
    btn_enregistrer.grid(row=3,column=1,sticky='e',pady=10)
    fenetre.mainloop()
    

#Fonction qui permet de supprimer une tâche 
def supprimer_une_tache():
    fenetre = tk.Tk()
    fenetre.title("Nom de la tâhe")
    fenetre.geometry("350x120")
    nom_label=tk.Label(fenetre,text="Nom de la tâche / Commande ")
    nom_label.grid(row=1,column=0)
    nom_entry=tk.Entry(fenetre)
    nom_entry.grid(row=2, column=0, columnspan=2, sticky="we", padx=5,pady=10)
    
    def annuler():
        fenetre.destroy()
    def enregistrer():
        supprimer_une_tache_dans_table_cron(nom_entry.get())
        fenetre.destroy()

    btn_annuler=tk.Button(fenetre, text="Annuler",bg="#222121",width=15,fg="white",command=annuler)
    btn_annuler.grid(row=3,column=0,sticky='w',pady=10)
    btn_enregistrer=tk.Button(fenetre, text="Supprimer",bg="#222121",width=15,fg="white",command=enregistrer)
    btn_enregistrer.grid(row=3,column=1,sticky='e',pady=10)
    fenetre.mainloop()
    



def menu_principale():
    fenetre = tk.Tk()
    fenetre.title("PLANIFICATEUR DE TÂCHE")
    fenetre.geometry("1000x700")

    #Créer le frame de menu
    menu_frame = tk.Frame(fenetre,bg="#222121",width=250,highlightthickness=3,highlightbackground="#616164")
    menu_frame.pack(side=tk.LEFT,fill=tk.Y)
    menu_frame.pack_propagate(False) #Fixe le largeur du frame

    #Creer "centre_frame"
    centre_frame = tk.Frame(fenetre,bg="#4D4C4C",highlightthickness=3,highlightbackground="#616164")
    centre_frame.pack(fill=tk.BOTH,expand=True)
    centre_frame.pack_propagate(False) #Fixe le largeur du frame

    ##Boutton : Nouvelle tâche
    #Creer un boutton "Nouvelle tâche" qui permet de créer une tâche
    icon1=ImageTk.PhotoImage(Image.open("add.png").resize((25,25)))
    ajouter_tache=tk.Button(centre_frame,text="Nouvelle tâche",bg="#222121",fg="white",image=icon1,compound="left",activebackground="#C5C1C1",highlightthickness=3,highlightbackground="#616164",command=ajouter_une_tache)
    ajouter_tache.pack(side=tk.TOP,anchor='e',padx=30,pady=30)
    ajouter_tache.image=icon1

    #Creer les menu (Bouttons): Liste de tâches ,Ajouter une tâche , Modifier une tâche , Supprimer une tâche
    icon1=ImageTk.PhotoImage(Image.open("list.png").resize((25,25)))
    liste_taches = tk.Button(menu_frame,text="Liste de tâches",fg="white",bg="#222121",image=icon1,compound="left",anchor="w",bd=0,relief="groove",highlightthickness=0,activebackground="#C5C1C1",height=40,command=lambda:liste_de_taches(centre_frame))
    liste_taches.pack(fill=tk.X,pady=0)
    icon2=ImageTk.PhotoImage(Image.open("add.png").resize((25,25)))
    ajouter_tache=tk.Button(menu_frame,text="Ajouter une tâche",fg="white",bg="#222121",image=icon2,compound="left",anchor="w",bd=0,relief="groove",highlightthickness=0,activebackground="#C5C1C1",height=40,command=ajouter_une_tache)
    ajouter_tache.pack(fill=tk.X,pady=0)
    icon3=ImageTk.PhotoImage(Image.open("edit.png").resize((25,25)))
    modifier_tache=tk.Button(menu_frame,text="Modifier une tâche",fg="white",bg="#222121",image=icon3,compound="left",anchor="w",bd=0,relief="groove",highlightthickness=0,activebackground="#C5C1C1",height=40,command=modifier_une_tache)
    modifier_tache.pack(fill=tk.X,pady=0)
    icon4=ImageTk.PhotoImage(Image.open("delete.png").resize((25,25)))
    supprimer_tache=tk.Button(menu_frame,text="Supprimer une tâche",fg="white",bg="#222121",image=icon4,compound="left",anchor="w",bd=0,relief="groove",highlightthickness=0,activebackground="#C5C1C1",height=40,command=supprimer_une_tache)
    supprimer_tache.pack(fill=tk.X,pady=0)



    liste_de_taches(centre_frame)

    fenetre.mainloop()

menu_principale()
