#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//Structure utiliser 
typedef struct tache
{
    char nom[100];
    char type_planification[50];
    char date[15];
    char heure[8];
    int jour_semaine;
    int jour_mois;
} tache;

//Declaration des fonctions
void menu_principal();
void  ajouter_une_tache();
void liste_taches(int utilisation);
tache supprimer_une_tache(int utilisation);
void modifier_une_tache();
int nombre_taches();

//Afficher le menu principal et demander à l'utilisateur de faire un choix
void menu_principal()
{
     int choix;
    printf("\033[10C \033[1;106;30m  MENU PRINCIPALE  \033[0m\n\n");
    printf("\033[10C\033[1;32m[1]\033[1;37m Ajouter une tâche \033[0m\n");
    printf("\033[10C\033[1;32m[2]\033[1;37m Tous les tâches \033[0m\n");
    printf("\033[10C\033[1;32m[3]\033[1;37m Modifier une tâche \033[0m\n");
    printf("\033[10C\033[1;32m[4]\033[1;37m Supprimer une tâche \033[0m\n");
    printf("\033[10C\033[1;32m[5]\033[1;37m Quitter \033[0m\n");
    printf("\033[10C\033[3;36mEntrez votre choix : \033[0m");
    scanf("%d", &choix);
    if(choix==1){ ajouter_une_tache();}
    else if(choix==2){liste_taches(0);}
    else if(choix==3){modifier_une_tache();}
    else if (choix==4){supprimer_une_tache(2);}
    else if (choix==5){exit(0);}
    else{menu_principal();}
}

//Cette demande au utilisateur la tâche avec la date d'exécution 
//Et puis enregistre cette dans un fichier "Liste_taches.csv" et dans le fichier cron (crontab -e)
void  ajouter_une_tache()
{
    int choix,i,min,heure,jour_du_mois,mois;
    char commande[255];
    char * type_planification [4] = {"Exécution unique","Tous les jours","Chaque semaine","Chaque mois"};
    tache nouvelle_tache ;
    //Alocation
    strcpy(nouvelle_tache.date,"00/00/0000");
    strcpy(nouvelle_tache.heure,"00:00");

    printf("\033[10C\033[1;106;30m  AJOUTER UNE TÂCHE  \033[0m\n\n");

    //Recuperer le type de planification de tâche
    printf("\033[10C\033[1;93mType de planification\033[0m\n");
    printf("\033[15C\033[1;32m[1]\033[1;37m Exécution unique \033[0m\n\033[15C\033[1;32m[2]\033[1;37m Tous les jours \033[0m\n\033[15C\033[1;32m[3]\033[1;37m Chaque semaine \033[0m\n\033[15C\033[1;32m[4]\033[1;37m Chaque mois \033[0m\n");
    printf("\033[15C\033[1;32m[5]\033[1;37m Retourner \033[0m\n\033[15C\033[1;32m[6]\033[1;37m Quitter \033[0m\n");
    printf("\033[10C\033[3;36mEntrez votre choix : \033[0m");
    scanf("%d", &choix);
    for (i=0;i<6;i++)
    {
        if(choix==i+1)
        {
            if(choix==5){ }
            else if(choix==6){exit(0);}
            else{strcpy(nouvelle_tache.type_planification,type_planification[i]);}
        }
    }
    //Recuperer la tâche à exécuter
    printf("\033[10C\033[1;93mTâche à exécuter : \033[0m");
    while(getchar() != '\n');  
    fgets(nouvelle_tache.nom,100,stdin);
    nouvelle_tache.nom[strcspn(nouvelle_tache.nom, "\n")] = '\0';
    //Recuperer la date et heure d'exécution d'une tâche
    if(strcmp(nouvelle_tache.type_planification,type_planification[0]) == 0)
    {
        printf("\033[10C\033[1;93mDate d'exécution [jj/mm/aaaa] : \033[0m");
        scanf("%s",nouvelle_tache.date);
    }
    if(strcmp(nouvelle_tache.type_planification,type_planification[3]) == 0)
    {
        printf("\033[10C\033[1;93mJour d'exécution chaque mois [1-31] : \033[0m");
        scanf("%d",&nouvelle_tache.jour_mois);
    }
    printf("\033[10C\033[1;93mHeure d'exécution [hh:mm] : \033[0m");
    scanf("%s",nouvelle_tache.heure);
    if(strcmp(nouvelle_tache.type_planification,type_planification[2]) == 0)
    {
        printf("\033[10C\033[1;93mJour de la semaine : \033[0m\n");
        printf("\033[15C\033[1;32m[0]\033[1;37m Dimanche \033[0m\n\033[15C\033[1;32m[1]\033[1;37m Lundi \033[0m\n\033[15C\033[1;32m[2]\033[1;37m Mardi \033[0m\n");
        printf("\033[15C\033[1;32m[3]\033[1;37m Mercredi \033[0m\n\033[15C\033[1;32m[4]\033[1;37m Jeudi \033[0m\n\033[15C\033[1;32m[5]\033[1;37m Vendredi \033[0m\n\033[15C\033[1;32m[6]\033[1;37m Samedi \033[0m\n");
        printf("\033[10C\033[3;36mEntrez votre choix : \033[0m");
        scanf("%d",&nouvelle_tache.jour_semaine);
    }

    //Ajouter la tâche dans le fichier "Liste_taches.csv" de la forme : Tâche,Type de planification,date,heure,joud de la semaine,jour du mois
    sprintf(commande,"echo \"%s,%s,%s,%s,%d,%d\" >> Liste_taches.csv",nouvelle_tache.nom,nouvelle_tache.type_planification,nouvelle_tache.date,nouvelle_tache.heure,nouvelle_tache.jour_semaine,nouvelle_tache.jour_mois);
    system(commande);

    //Recuperer : minute,heure,mois
    sscanf(nouvelle_tache.heure,"%d:%d",&heure,&min);
    sscanf(nouvelle_tache.date,"%d/%d/%*d",&jour_du_mois,&mois);

    //Ajouter une tâche cron 
    if(strcmp(nouvelle_tache.type_planification,type_planification[0]) == 0){sprintf(commande, " echo \"%d %d %d %d * %s\" >> temp_cron ", min, heure,jour_du_mois , mois, nouvelle_tache.nom);}
    else if(strcmp(nouvelle_tache.type_planification,type_planification[1]) == 0){sprintf(commande, " echo \"%d %d * * * %s\" >> temp_cron ", min, heure,nouvelle_tache.nom);}
    else if(strcmp(nouvelle_tache.type_planification,type_planification[2]) == 0){sprintf(commande, " echo \"%d %d * * %d %s\" >> temp_cron ", min, heure,nouvelle_tache.jour_semaine, nouvelle_tache.nom);}
    else if(strcmp(nouvelle_tache.type_planification,type_planification[3]) == 0){sprintf(commande, " echo \"%d %d %d * * %s\" >> temp_cron ", min, heure,jour_du_mois, nouvelle_tache.nom);}
    system(commande);
    sprintf(commande, "cat temp_cron | crontab -");
    system(commande);
}

//Cette fonction permet de compter le nombre de tâches dans le fichier Liste_taches.csv
int nombre_taches()
{
    int compter ;
    char * ligne = malloc(255*sizeof(char));
    FILE *fichier = fopen("Liste_taches.csv", "r");
    compter = 0;
    if (fichier != NULL)
    {
        while (fgets(ligne, 255, fichier) != NULL) 
        {
            compter++;
        }
        fclose(fichier);
    }
    return (compter-1);
}


void liste_taches(int utilisation)
{
    int nombreTaches,i;
    char * ligne = malloc(255*sizeof(char));
    char * jour_de_semaine[7]={"Dimanche","Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi"};
    char * type_planification [4] = {"Exécution unique","Tous les jours","Chaque semaine","Chaque mois"};
    tache tache1;
    FILE *fichier = fopen("Liste_taches.csv", "r");
    nombreTaches = nombre_taches();
    if (fichier != NULL) 
    {
        //Afficher le titre selon l'utilisation : LISTES , MODIFICATION , SUPPRESSION
        if(utilisation==0){printf("\033[10C\033[1;106;30m  TOUTES LES TÂCHES  \033[0m\n\n");}
        else if(utilisation==1){printf("\033[10C\033[1;106;30m  MODIFIER UNE TÂCHE  \033[0m\n\n");}
        else if(utilisation==2){printf("\033[10C\033[1;106;30m  SUPPRIMER UNE TÂCHE  \033[0m\n\n");}
        
        printf("\033[10C\033[1;32m[Numero de tâche]\033[1;93m\tTâche\t  \033[0;3;46mType de planification\033[3;0m (Date d'exécution)\033[0m\n\n");

        //Afficher toutes les tâches dans le fichier "Liste_taches.csv": qui contient toutes les tâches cron
        for (i=0;i<nombreTaches;i++)
        {
            fgets(ligne,255,fichier);
            sscanf(ligne, "%[^,],%[^,],%[^,],%[^,],%d,%d", tache1.nom, tache1.type_planification, tache1.date, tache1.heure, &tache1.jour_semaine, &tache1.jour_mois);
            
            if(strcmp(tache1.type_planification,type_planification[0])==0){printf("\033[10C\033[1;32m[%d]\033[1;93m\t%s \n\033[10C\t  \033[0;3;46m%s\033[3;0m (%s à %s)\033[0m\n\n",i,tache1.nom, tache1.type_planification, tache1.date, tache1.heure);}
            else if(strcmp(tache1.type_planification,type_planification[1])==0){printf("\033[10C\033[1;32m[%d]\033[1;93m\t%s \n\033[10C\t  \033[0;3;44m%s\033[3;0m ( à %s)\033[0m\n\n",i,tache1.nom, tache1.type_planification, tache1.heure);}
            else if(strcmp(tache1.type_planification,type_planification[2])==0){printf("\033[10C\033[1;32m[%d]\033[1;93m\t%s \n\033[10C\t  \033[0;3;45m%s\033[3;0m (tous le %s à %s)\033[0m\n\n",i,tache1.nom, tache1.type_planification, jour_de_semaine[tache1.jour_semaine], tache1.heure);}
            else if(strcmp(tache1.type_planification,type_planification[3])==0){printf("\033[10C\033[1;32m[%d]\033[1;93m\t%s \n\033[10C\t  \033[0;3;42m%s\033[3;0m (Tous le %dème du mois à %s)\033[0m\n\n",i,tache1.nom, tache1.type_planification, tache1.jour_mois, tache1.heure);}
        }
        fclose(fichier);
    }
}

//Cette fonction permet de supprimer une tâche dans crontab -e
tache supprimer_une_tache(int utilisation)
{
    int choix,i;
    char ligne[255];
    char commade[255];
    tache tache_supprimer;
    FILE *fichier_src = fopen("Liste_taches.csv", "r");
    FILE *tmp = fopen("temp.csv", "w");
    liste_taches(utilisation);        
    printf("\033[10C\033[3;36mEntrez votre choix : \033[0m");
    scanf("%d",&choix);
    if(fichier_src!=NULL && tmp!=NULL)
    {
        i=0;
        while (fgets(ligne, sizeof(ligne), fichier_src))
        {
            if(i!=choix){fputs(ligne, tmp); } // Copier toutes les lignes sauf celle à supprimer
            else{sscanf(ligne, "%[^,],%[^,],%[^,],%[^,],%d,%d",tache_supprimer.nom,tache_supprimer.type_planification,tache_supprimer.date,tache_supprimer.heure,&tache_supprimer.jour_semaine,&tache_supprimer.jour_mois);}
            i++;
        }
        fclose(fichier_src);
        fclose(tmp);
    }
    // Remplacer le fichier original par le fichier temporaire
    remove("Liste_taches.csv");
    rename("temp.csv", "Liste_taches.csv");
    sprintf(commade,"crontab -l | grep -v \"%s\" | crontab -",tache_supprimer.nom);
    system(commade);
    return(tache_supprimer);
}

//Cette fonction permet de modifier une tâche 
void modifier_une_tache()
{
    tache tache_a_modifier;
    //Cette fonction demande au utilisateur le numero de tâche à modifier puis supprimer l'ancienne tâche 
    tache_a_modifier=supprimer_une_tache(1);
    //Afficher les ancienne tâche 
    printf("\033[10C\033[1;106;30m  ANCIENNE TÂCHE  \033[0m\n\n");
    printf("\033[10C\033[1;93mTâche à exécuter : \033[3;37m %s \033[0m",tache_a_modifier.nom);
    printf("\033[10C\033[1;93mType de planification :\033[3;37m %s \033[0m\n",tache_a_modifier.type_planification);
    printf("\033[10C\033[1;93mDate d'exécution [jj/mm/aaaa] :\033[3;37m %s \033[0m",tache_a_modifier.date);
    printf("\033[10C\033[1;93mHeure d'exécution [hh:mm] : \033[3;37m %s\033[0m",tache_a_modifier.heure);
    printf("\033[10C\033[1;93mJour d'exécution chaque mois [1-31] :\033[3;37m %d \033[0m",tache_a_modifier.jour_mois);
    printf("\033[10C\033[1;93mJour de la semaine : \033[3;37m %d\033[0m\n",tache_a_modifier.jour_semaine);
    ajouter_une_tache();
}

int main()
{
   menu_principal();
}