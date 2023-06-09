import mysql.connector
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="user",
    password="example",
    port="3307",
    database="breizhibus"
)
cursor = db.cursor()

# Page 1 : Horaires par lignes
def horaires_par_lignes():
    st.header("Breizhibus - Horaires par lignes")

    image = "https://www.proantic.com/galerie/patrick-serouge/img/775841-main-609f88f0c9c88.jpg"
    st.image(image, caption='Breizhibus Logo', use_column_width=True)

    # Récupérer la liste des lignes
    cursor.execute("SELECT DISTINCT ligne FROM horaires")
    lignes = cursor.fetchall()
    lignes = [ligne[0] for ligne in lignes]

    # Sélectionner la ligne
    selected_ligne = st.selectbox("Sélectionnez une ligne :", lignes)

    # Récupérer les arrêts pour la ligne sélectionnée
    cursor.execute("SELECT DISTINCT arret FROM horaires WHERE ligne = %s", (selected_ligne,))
    arrets = cursor.fetchall()
    arrets = [arret[0] for arret in arrets]

    # Sélectionner l'arrêt
    selected_arret = st.selectbox("Sélectionnez un arrêt :", arrets)

    # Récupérer les horaires et les adresses pour la ligne et l'arrêt sélectionnés
    query = """
    SELECT horaires.heure, arrets.adresse
    FROM horaires
    INNER JOIN arrets ON horaires.arret = arrets.id
    WHERE horaires.ligne = %s AND horaires.arret = %s
    """

    # Exécuter la requête avec les paramètres de ligne et d'arrêt sélectionnés
    cursor.execute(query, (selected_ligne, selected_arret))

    # Récupérer les résultats dans un DataFrame
    df_horaires = pd.DataFrame(cursor.fetchall(), columns=['heure', 'adresse'])

    # Afficher les horaires et les adresses
    st.subheader(f"Horaires et adresses pour la ligne {selected_ligne} et l'arrêt {selected_arret}:")
    st.dataframe(df_horaires)

    image = "https://images.pexels.com/photos/808846/pexels-photo-808846.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    st.image(image, caption='Breizhibus Logo', use_column_width=True)


        

# Page 2 : Statistiques internes
def statistiques_internes():
    st.header("Breizhibus - Statistiques internes")
    # Récupérer les données de fréquentation par ligne
    plt.figure()
    cursor.execute("SELECT lignes.nom AS Ligne, SUM(frequentation.nombre_passagers) AS Total_Passagers FROM frequentation INNER JOIN horaires ON frequentation.horaire = horaires.id INNER JOIN lignes ON horaires.ligne = lignes.id GROUP BY lignes.nom;")
    frequentation_ligne = cursor.fetchall()
    frequentation_ligne = pd.DataFrame(frequentation_ligne, columns=['horaire', 'frequentations'])
    
    # Afficher le graphique des frequentations par ligne
    st.subheader("Fréquentations par lignes:")
    plt.figure()
    plt.bar(frequentation_ligne['horaire'], frequentation_ligne['frequentations'])
    plt.xlabel("Ligne")
    plt.ylabel("Fréquentations")
    plt.title("Fréquentations par lignes")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Récupérer les données de fréquentation par heures
    cursor.execute("SELECT horaires.heure AS Horaire, SUM(frequentation.nombre_passagers) AS Total_Passagers FROM frequentation INNER JOIN horaires ON frequentation.horaire = horaires.id GROUP BY horaires.heure;")
    frequentations_heures = cursor.fetchall()
    frequentations_heures = pd.DataFrame(frequentations_heures, columns=['horaire', 'frequentations'])

    # Afficher le graphique linéaire des fréquentations par heures
    st.subheader("Fréquentations par heure:")
    plt.figure()
    plt.plot(frequentations_heures['horaire'], frequentations_heures['frequentations'])
    plt.xlabel("Horaire")
    plt.ylabel("Fréquentations")
    plt.title("Fréquentations par heure")
    plt.xticks(rotation=45)  # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
    st.pyplot(plt)
    
    
    # Récupérer les données de fréquentation par jours
    cursor.execute("SELECT frequentation.jour AS Jour, SUM(frequentation.nombre_passagers) AS Total_Passagers FROM frequentation GROUP BY frequentation.jour;")
    frequentations_jours = cursor.fetchall()
    frequentations_jours = pd.DataFrame(frequentations_jours, columns=['Jour', 'frequentations'])
    
    # Afficher le camembert des frequentations par jours
    st.subheader("frequentations par jours:")
    plt.figure()
    plt.pie(frequentations_jours['frequentations'], labels=frequentations_jours['Jour'], autopct='%1.1f%%')
    
    st.pyplot(plt)

# Application Streamlit
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choisissez une page :", ("Accueil", "Statistiques"))
    st.title("Breizhibus")
    if page == "Accueil":
        horaires_par_lignes()
    elif page == "Statistiques":
        statistiques_internes()

if __name__ == '__main__':
    main()





