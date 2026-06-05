#!/bin/bash

main_menu()
{
    echo -e "Menu principales : \n\t1 - Ajouter une tâche\n\t2 - Lister toutes les tâches\n\t3 - Modifier une tâche\n\t4 - Supprimer une tâche\n\tQuitter \"q\""
    read -p "Choix : " choix
    if [[ "$choix" -eq 1 ]] ; then
        get_date;get_task;save_task
    elif [[ "$choix" -eq 2 ]] ; then
        crontab -l | awk '{if($0 !~ /^#/) print $0}'
        read -p "[Tapez (R) : Retourner , (Q) : Quitter] " tape
        if [["$tape" == "R" || "$tape" == "r"]]; then
            main_menu
        elif [["$tape" == "Q" || "$tape" == "q"]]; then
            exit
        fi
    elif [[ "$choix" -eq 3 ]] ; then
        modification
    elif [[ "$choix" -eq 4 ]] ; then
        echo -e "\nToutes les tâches : "
        crontab -l | awk '{if($0 !~ /^#/) {for (i=6;i<=NF;i++) printf " " $i; print ""}}' > /tmp/taches.txt 
        cat -n /tmp/taches.txt | rm /tmp/taches.txt
        read -p "Entrez la tâche à supprimer : " task
        if [[ -z "$task" || "$task" == "" ]]; then
            echo "Aucune tâche sélectionnée. Aucune tâche supprimée."
        else    
            crontab -l | grep -v "$task" | crontab -
        fi
    elif [[ "$choix" == "q" || "$choix" == "Q" ]]; then
        exit 
    fi
}

get_date()
{
    echo -e "Entrez la date : \n"
    echo -e "Tapez \e[32m*\e[0m si chaque minute"
    read -p "Minute [0-59] : " min
    while [[ "$min" != "*"  ]] && { [[ ($min -lt 0 || $min -gt 59 ) ]] ;}  > /dev/null ; do 
        if [[ "$min" == "*" ]]; then
            break
        fi
        read -p "Minute [0-59] : " min
    done
    echo -e "Tapez \e[32m*\e[0m si chaque heure"
    read -p "Heure [0-23] : " hour
    while [[ "$hour" != "*"  ]] && { [[ ($hour -lt 0 || $hour -gt 23 ) ]] ;}  > /dev/null ; do 
        if [[ "$hour" == "*" ]]; then
            break
        fi
        read -p "Minute [0-59] : " hour
    done
    echo -e "Tapez \e[32m*\e[0m si chaque jour pendant le mois"
    read -p "Jour du mois [0-31] : " day_of_month
    while [[ "$day_of_month" != "*"  ]] && { [[ ($day_of_month -lt 0 || $day_of_month -gt 31 ) ]] ;}  > /dev/null ; do 
        if [[ "$day_of_month" == "*" ]]; then
            break
        fi
        read -p "Minute [0-59] : " day_of_month
    done
    echo -e "Tapez \e[32m*\e[0m si chaque mois"
    read -p "Mois [0-12] : " month
    while [[ "$month" != "*"  ]] && { [[ ($month -lt 0 || $month -gt 12 ) ]] ;}  > /dev/null ; do 
        if [[ "$month" == "*" ]]; then
            break
        fi
        read -p "Minute [0-59] : " month
    done
    echo -e "Tapez \e[32m*\e[0m si chaque jour de la semaine\n\t0- Lundi \n\t1- Mardi\n\t2- Mercredi\n\t3- Jeudi\n\t4- Vendredi\n\t5- Samedi \n\t6- Dimanche"
    read -p "Jour de la Semaine [0-6] : " day_of_week
    while [[ "$day_of_week" != "*"  ]] && { [[ ($day_of_week -lt 0 || $day_of_week -gt 59 ) ]] ;}  > /dev/null ; do 
        if [[ "$day_of_week" == "*" ]]; then
            break
        fi
        read -p "Minute [0-59] : " day_of_week
    done
}

get_task()
{
    read -p "Entrez la tache à éxécuter : " task
}

save_task()
{
    (crontab -l 2> /dev/null; echo "$min $hour $day_of_month $month $day_of_week $task") | crontab -
}

modification()
{
    echo -e "\nToutes les tâches : "
        crontab -l | awk '{if($0 !~ /^#/) {for (i=6;i<=NF;i++) printf " " $i; print ""}}' > /tmp/taches.txt 
        cat -n /tmp/taches.txt | rm /tmp/taches.txt
    read -p "Entrez la tâche à modifier (R: Retourner , Q: Quitter) : " task
    if [[ -z "$task" || "$task" == "" ]]; then
        echo "Aucune tâche sélectionnée. Aucune tâche supprimée."
    elif [["$task" == "R" || "$task" == "r"]]; then
        main_menu
    elif [["$task" == "Q" || "$task" == "q"]]; then
        exit
    else    
        get_date;get_task
        read -p "Enregistrer la modification [Oui/Non] : " reponse
        if [["$reponse" == "O" || "$reponse" == "o" || "$reponse" == "Oui" || "$reponse" == "OUI" || "$reponse" == "oui"]];then
            crontab -l | grep -v "$task" | crontab -
            save_task
        elif [["$reponse" == "N" || "$reponse" == "n" || "$reponse" == "Non" || "$reponse" == "NON" || "$reponse" == "non"]];then
            modification
        fi
    fi


}


while true ; do
    main_menu
    clear
done

