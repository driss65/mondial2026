import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="Prono Coupe du Monde 2026", page_icon="⚽", layout="wide")

# GROUPES OFFICIELS
GROUPES_2026 = {
    "Groupe A": ["Mexique", "Afrique du Sud", "Corée du Sud", "République Tchèque"],
    "Groupe B": ["Canada", "Bosnie-Herzégovine", "Qatar", "Suisse"],
    "Groupe C": ["Maroc", "Brésil", "Haïti", "Écosse"],
    "Groupe D": ["États-Unis", "Paraguay", "Australie", "Turquie"],
    "Groupe E": ["Allemagne", "Curaçao", "Côte d'Ivoire", "Équateur"],
    "Groupe F": ["Pays-Bas", "Japon", "Suède", "Tunisie"],
    "Groupe G": ["Belgique", "Égypte", "Iran", "Nouvelle-Zélande"],
    "Groupe H": ["Espagne", "Cap-Vert", "Arabie Saoudite", "Uruguay"],
    "Groupe I": ["France", "Sénégal", "Irak", "Norvège"],
    "Groupe J": ["Argentine", "Algérie", "Autriche", "Jordanie"],
    "Groupe K": ["Portugal", "RD Congo", "Ouzbékistan", "Colombie"],
    "Groupe L": ["Angleterre", "Croatie", "Ghana", "Panama"]
}

def sauvegarder_prediction(donnees):
    fichier = "predictions.csv"
    df_nouveau = pd.DataFrame([donnees])
    if os.path.exists(fichier):
        df_existant = pd.read_csv(fichier)
        if donnees["Pseudo"] in df_existant["Pseudo"].values:
            return False
        df_final = pd.concat([df_existant, df_nouveau], ignore_index=True)
    else:
        df_final = df_nouveau
    df_final.to_csv(fichier, index=False)
    return True

st.title("🏆 Pronostiques Mondial 2026 — Version Officielle Intégrale")
st.write("Bonne chance!!.")

pseudo = st.text_input("👤 Entrez votre nom ou pseudo :", key="username").strip()

if pseudo:
    st.success(f"C'est parti, bon prono {pseudo} !")
    st.divider()

    # 1️⃣ PHASE DE GROUPES
    st.header("1️⃣ Classement de la Phase de Groupes")
    
    premiers = {}
    seconds = {}
    troisiemes = {}
    
    cols = st.columns(3)
    for i, (nom_groupe, equipes) in enumerate(GROUPES_2026.items()):
        with cols[i % 3]:
            st.markdown(f"### {nom_groupe}")
            p1 = st.selectbox(f"1er {nom_groupe}", equipes, key=f"{nom_groupe}_1")
            restantes_1 = [e for e in equipes if e != p1]
            
            p2 = st.selectbox(f"2e {nom_groupe}", restantes_1, key=f"{nom_groupe}_2")
            restantes_2 = [e for e in restantes_1 if e != p2]
            
            p3 = st.selectbox(f"3e {nom_groupe}", restantes_2, key=f"{nom_groupe}_3")
            p4 = [e for e in restantes_2 if e != p3][0]
            st.caption(f"❌ Éliminé : {p4}")
            
            lettre = nom_groupe.split()[-1]
            premiers[lettre] = p1
            seconds[lettre] = p2
            troisiemes[lettre] = p3
            st.divider()

    # 2️⃣ GESTION DE LA SÉLECTION DES TROISIÈMES (Utiles pour les cases 3e)
    st.header("2️⃣ Les Meilleurs Troisièmes Qualifiés")
    st.write("Cochez précisément **8 équipes** de troisième place :")
    
    groupes_3es_choisis = []
    cols_3e = st.columns(4)
    for idx, (lettre, equipe_3e) in enumerate(troisiemes.items()):
        with cols_3e[idx % 4]:
            if st.checkbox(f"{equipe_3e} (Grp {lettre})", key=f"chk_{lettre}", value=(idx < 8)):
                groupes_3es_choisis.append(equipe_3e)

    if len(groupes_3es_choisis) == 8:
        st.success("✅ Nombre de troisièmes correct.")
        st.divider()
        
        # Dispatching des troisièmes pour les affiches complexes
        t3_ABCDF = groupes_3es_choisis[0]
        t3_CDFGH = groupes_3es_choisis[1]
        t3_CEFHI = groupes_3es_choisis[2]
        t3_EHIJK = groupes_3es_choisis[3]
        t3_AEHIJ = groupes_3es_choisis[4]
        t3_BEFIJ = groupes_3es_choisis[5]
        t3_EFGIJ = groupes_3es_choisis[6]
        t3_DEIJL = groupes_3es_choisis[7]

        # 3️⃣ SEIZIÈMES DE FINALE (Image 1 & 2)
        st.header("3️⃣ Seizièmes de Finale")
        
        # Liste construite dans l'ordre EXACT des captures d'écran (Date + Heure)
        affiches_16e = [
            ("28 Juin - 15:00", seconds["A"], seconds["B"]),         # 2A vs 2B
            ("29 Juin - 13:00", premiers["C"], seconds["F"]),        # 1C vs 2F
            ("29 Juin - 16:30", premiers["E"], t3_ABCDF),            # 1E vs 3ABCDF
            ("29 Juin - 21:00", premiers["F"], seconds["C"]),        # 1F vs 2C -> PAYS-BAS vs BRÉSIL !
            ("30 Juin - 13:00", seconds["E"], seconds["I"]),         # 2E vs 2I
            ("30 Juin - 17:00", premiers["I"], t3_CDFGH),            # 1I vs 3CDFGH
            ("30 Juin - 21:00", premiers["A"], t3_CEFHI),            # 1A vs 3CEFHI
            ("01 Juillet - 12:00", premiers["L"], t3_EHIJK),         # 1L vs 3EHIJK
            ("01 Juillet - 16:00", premiers["G"], t3_AEHIJ),         # 1G vs 3AEHIJ
            ("01 Juillet - 20:00", premiers["D"], t3_BEFIJ),         # 1D vs 3BEFIJ
            ("02 Juillet - 15:00", premiers["H"], seconds["J"]),     # 1H vs 2J -> Ton autre correction !
            ("02 Juillet - 19:00", seconds["K"], seconds["L"]),         # 2K vs 2L
            ("02 Juillet - 23:00", premiers["B"], t3_EFGIJ),         # 1B vs 3EFGIJ
            ("03 Juillet - 14:00", seconds["D"], seconds["G"]),         # 2D vs 2G
            ("03 Juillet - 18:00", premiers["J"], seconds["H"]),     # 1J vs 2H
            ("03 Juillet - 21:30", premiers["K"], t3_DEIJL),         # 1K vs 3DEIJL
        ]

        gagnants_16e = {}
        cols_16e = st.columns(4)
        for m, (label, eq1, eq2) in enumerate(affiches_16e):
            # Identifiant unique de match basé sur sa position
            id_match = f"EF{m+1}" 
            with cols_16e[m % 4]:
                st.markdown(f"🗓️ **{label}** *(Match {id_match})*")
                choix = st.radio(f"{eq1} 🆚 {eq2}", [eq1, eq2], key=f"radio_{id_match}")
                gagnants_16e[id_match] = choix

        # 4️⃣ HUITIÈMES DE FINALE (Image 2)
        st.header("4️⃣ Huitièmes de Finale")
        
        # Ordre exact déterminé par l'image du 04 au 07 Juillet
        affiches_8e = [
            ("04 Juillet - 13:00", gagnants_16e["EF1"], gagnants_16e["EF4"]),  # 2A/2B vs 1F/2C
            ("04 Juillet - 17:00", gagnants_16e["EF3"], gagnants_16e["EF6"]),  # 1E/3ABCDF vs 1I/3CDFGH
            ("05 Juillet - 16:00", gagnants_16e["EF2"], gagnants_16e["EF5"]),  # 1C/2F vs 2E/2I
            ("05 Juillet - 20:00", gagnants_16e["EF7"], gagnants_16e["EF8"]),  # 1A/3CEFHI vs 1L/3EHIJK
            ("06 Juillet - 15:00", gagnants_16e["EF12"], gagnants_16e["EF11"]),# 2K/2L vs 1H/2J
            ("06 Juillet - 20:00", gagnants_16e["EF10"], gagnants_16e["EF9"]), # 1D/3BEFIJ vs 1G/3AEHIJ
            ("07 Juillet - 12:00", gagnants_16e["EF15"], gagnants_16e["EF14"]),# 1J/2H vs 2D/2G
            ("07 Juillet - 16:00", gagnants_16e["EF13"], gagnants_16e["EF16"]),# 1B/3EFGIJ vs 1K/3DEIJL
        ]

        gagnants_8e = {}
        cols_8e = st.columns(4)
        for m, (label, eq1, eq2) in enumerate(affiches_8e):
            id_match = f"QF{m+1}"
            with cols_8e[m % 4]:
                st.markdown(f"🔹 **{label}** *(Match {id_match})*")
                choix = st.radio(f"{eq1} 🆚 {eq2}", [eq1, eq2], key=f"radio_{id_match}")
                gagnants_8e[id_match] = choix

        # 5️⃣ QUARTS DE FINALE (Image 3)
        st.header("5️⃣ Quarts de Finale")
        
        affiches_quarts = [
            ("10 Juillet - 15:00", gagnants_8e["QF5"], gagnants_8e["QF6"]),    # Winner EF 5 vs Winner EF 6
            ("11 Juillet - 17:00", gagnants_8e["QF3"], gagnants_8e["QF4"]),    # Winner EF 3 vs Winner EF 4
            ("11 Juillet - 21:00", gagnants_8e["QF7"], gagnants_8e["QF8"]),    # Winner EF 7 vs Winner EF 8
            ("09 Juillet - 16:00", gagnants_8e["QF1"], gagnants_8e["QF2"]),    # Winner EF 1 vs Winner EF 2 (Placé chronologiquement)
        ]

        gagnants_quarts = {}
        cols_q = st.columns(2)
        # On boucle sur l'ordre pour l'affichage propre
        for m, (label, eq1, eq2) in enumerate(affiches_quarts):
            id_match = f"SF{m+1}"
            with cols_q[m % 2]:
                st.markdown(f"🔸 **{label}**")
                choix = st.radio(f"{eq1} 🆚 {eq2}", [eq1, eq2], key=f"radio_{id_match}")
                gagnants_quarts[id_match] = choix

        # 6️⃣ DEMI-FINALES (Image 3)
        st.header("6️⃣ Demi-Finales")
        
        affiches_demi = [
            ("14 Juillet - 15:00", gagnants_quarts["SF4"], gagnants_quarts["SF2"]), # Vainqueur QF 1 vs Vainqueur QF 2
            ("15 Juillet - 15:00", gagnants_quarts["SF1"], gagnants_quarts["SF3"]), # Vainqueur QF 3 vs Vainqueur QF 4
        ]

        gagnants_demi = {}
        perdants_demi = {}
        cols_d = st.columns(2)
        for m, (label, eq1, eq2) in enumerate(affiches_demi):
            id_match = f"F{m+1}"
            with cols_d[m % 2]:
                st.markdown(f"⭐ **{label}**")
                choix = st.radio(f"{eq1} 🆚 {eq2}", [eq1, eq2], key=f"radio_{id_match}")
                gagnants_demi[id_match] = choix
                perdants_demi[id_match] = eq1 if choix == eq2 else eq2

        # 7️⃣ FINALES (Petite et Grande - Image 3)
        st.header("7️⃣ Finales")
        
        # Match pour la 3ème place (18 Juillet)
        st.subheader("🥉 Match pour la 3e place")
        p3_1 = perdants_demi["F1"]
        p3_2 = perdants_demi["F2"]
        troisieme_place = st.radio(f"18 Juillet - 17:00 : {p3_1} 🆚 {p3_2}", [p3_1, p3_2], key="p3_place")
        
        # Finale (19 Juillet)
        st.subheader("👑 LA FINALE")
        f1 = gagnants_demi["F1"]
        f2 = gagnants_demi["F2"]
        champion = st.radio(f"19 Juillet - 15:00 : {f1} 🆚 {f2}", [f1, f2], key="la_finale_2026")
        
        st.markdown(f"### 🏆 Votre Champion du Monde 2026 : **{champion}**")
        st.divider()

       # 8️⃣ ENREGISTREMENT
        st.header("8️⃣ Enregistrer mes pronostics")
        if st.button("🚀 VALIDER MA GRILLE"):
            prediction_joueur = {
                "Pseudo": pseudo,
                "Champion": champion,
                "3eme": troisieme_place,
                "Finaliste_1": f1,
                "Finaliste_2": f2
            }
            if sauvegarder_prediction(prediction_joueur):
                st.balloons()
                st.success("🎉 Parfait ! L'intégralité du tableau est validée  !")
            else:
                st.error("❌ Ce pseudo existe déjà.")

    else:
        st.warning("⚠️ Veuillez cocher exactement 8 équipes troisièmes pour générer la grille de phase finale.")
else:
    st.info("Veuillez saisir votre pseudo en haut de l'écran pour débloquer l'application.")

# --- 🔓 ESPACE ADMINISTRATEUR SÉCURISÉ (TOUT EN BAS DU FICHIER) ---
st.divider()
with st.expander("🛠️ Espace Organisateur (Accès réservé)"):
    password = st.text_input("Entrez le mot de passe pour voir les résultats :", type="password")
    
    # Tu peux changer "mon_code_secret_2026" par le mot de passe de ton choix
    if password == "drissmontreal2026@":
        st.subheader("📊 Liste de toutes les prédictions enregistrées")
        
        if os.path.exists("predictions.csv"):
            df_global = pd.read_csv("predictions.csv")
            
            # Affiche le tableau directement à l'écran
            st.dataframe(df_global)
            
            # Bouton magique pour télécharger le fichier Excel/CSV d'un coup
            csv = df_global.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger le fichier des scores (CSV)",
                data=csv,
                file_name="resultats_mondial_2026.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun pronostic n'a encore été enregistré.")
