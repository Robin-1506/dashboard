import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
file_path = "rapport_pharmacie.xlsx"
stats_df = pd.read_excel(file_path, sheet_name="Statistiques descriptives", engine="openpyxl")
monthly_df = pd.read_excel(file_path, sheet_name="Synthèse mensuelle", engine="openpyxl")

# Ajouter une colonne avec les noms de mois en français
mois_fr = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
           'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
monthly_df["NomMois"] = monthly_df["Month"].apply(lambda x: mois_fr[x - 1])
monthly_df["Date"] = pd.to_datetime(monthly_df[["Year", "Month"]].assign(DAY=1))

# Colonnes numériques
numeric_cols = monthly_df.select_dtypes(include='number').columns[2:]
monthly_df["TotalVentes"] = monthly_df[numeric_cols].sum(axis=1)
total_sales = monthly_df[numeric_cols].sum()

# Titre principal
st.title("📊 Dashboard des ventes de médicaments - Pharmacie")

# Onglets
tab1, tab2, tab3 = st.tabs(["📊 Statistiques & Synthèse", "📈 Évolution & Recherche", "🧑‍⚕️ Analyse stratégique"])

# Onglet 1 : Statistiques descriptives + Synthèse
with tab1:
    st.header("🔍 Statistiques descriptives")
    st.dataframe(stats_df, use_container_width=True)

    st.header("📊 Synthèse des ventes totales")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=total_sales.index, y=total_sales.values, ax=ax2)
    ax2.set_title("Ventes totales par type de médicament")
    ax2.set_xlabel("Type de médicament")
    ax2.set_ylabel("Ventes totales")
    plt.xticks(rotation=45)
    st.pyplot(fig2, use_container_width=True)

# Onglet 2 : Évolution mensuelle + Recherche ciblée
with tab2:
    st.header("📈 Évolution mensuelle des ventes")
    selected_product = st.selectbox("Choisissez un médicament", monthly_df.columns[2:])
    fig, ax = plt.subplots()
    sns.lineplot(data=monthly_df, x="Date", y=selected_product, ax=ax)
    ax.set_title(f"Évolution des ventes - {selected_product}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Ventes")
    st.pyplot(fig, use_container_width=True)

    st.header("🔎 Recherche ciblée")
    selected_year = st.selectbox("Année", sorted(monthly_df["Year"].unique()))
    selected_month_name = st.selectbox("Mois", mois_fr)
    selected_month = mois_fr.index(selected_month_name) + 1
    selected_product_2 = st.selectbox("Produit", monthly_df.columns[2:])
    filtered_value = monthly_df[
        (monthly_df["Year"] == selected_year) &
        (monthly_df["Month"] == selected_month)
    ][selected_product_2].values
    if filtered_value.size > 0:
        st.success(f"Ventes de {selected_product_2} en {selected_month_name} {selected_year} : {filtered_value[0]}")
    else:
        st.warning("Aucune donnée disponible pour cette sélection.")

# Onglet 3 : Analyse stratégique
with tab3:
    st.header("📊 Vue d’ensemble des ventes")
    fig_overview, ax_overview = plt.subplots()
    sns.lineplot(data=monthly_df, x="Date", y="TotalVentes", ax=ax_overview)
    ax_overview.set_title("Vue d’ensemble des ventes mensuelles")
    st.pyplot(fig_overview, use_container_width=True)

    st.header("📉 Produits à forte variation")
    variations = monthly_df[numeric_cols].std().sort_values(ascending=False)
    fig_var, ax_var = plt.subplots()
    sns.barplot(x=variations.index, y=variations.values, ax=ax_var)
    ax_var.set_title("Produits à forte variation de ventes")
    ax_var.set_ylabel("Écart-type des ventes")
    plt.xticks(rotation=45)
    st.pyplot(fig_var, use_container_width=True)

    st.header("🏆 Produits les plus vendus")
    top_products = total_sales.sort_values(ascending=False).head(5)
    fig_top, ax_top = plt.subplots()
    sns.barplot(x=top_products.index, y=top_products.values, ax=ax_top)
    ax_top.set_title("Top 5 des produits les plus vendus")
    st.pyplot(fig_top, use_container_width=True)

    st.header("📅 Saisonnalité des ventes")
    monthly_avg = monthly_df.groupby("Month")[numeric_cols].mean()
    fig_season, ax_season = plt.subplots()
    sns.heatmap(monthly_avg.T, cmap="YlGnBu", ax=ax_season)
    ax_season.set_title("Saisonnalité des ventes par produit")
    st.pyplot(fig_season, use_container_width=True)

    st.header("📉 Produits faibles en ventes")
    low_products = total_sales.sort_values().head(5)
    fig_low, ax_low = plt.subplots()
    sns.barplot(x=low_products.index, y=low_products.values, ax=ax_low)
    ax_low.set_title("Produits avec les ventes les plus faibles")
    st.pyplot(fig_low, use_container_width=True)

    st.header("📊 Comparaison par catégorie")
    fig_cat, ax_cat = plt.subplots()
    sns.boxplot(data=monthly_df[numeric_cols], ax=ax_cat)
    ax_cat.set_title("Distribution des ventes par catégorie de médicament")
    plt.xticks(rotation=45)
    st.pyplot(fig_cat, use_container_width=True)

    st.header("📈 Analyse temporelle")
    fig_time, ax_time = plt.subplots()
    sns.lineplot(data=monthly_df, x="Date", y="TotalVentes", ax=ax_time)
    ax_time.set_title("Analyse temporelle des ventes globales")
    st.pyplot(fig_time, use_container_width=True)

    st.header("💡 Opportunités d’amélioration")
    st.markdown("""
    - Renforcer la promotion des produits à faible vente.
    - Adapter les stocks selon la saisonnalité observée.
    - Cibler les produits à forte variation pour des campagnes spécifiques.
    """)

    st.header("📌 Propositions stratégiques")
    st.markdown("""
    - Mettre en place un suivi mensuel automatisé des ventes.
    - Développer des partenariats pour les produits clés.
    - Optimiser les catégories sous-performantes.
    """)