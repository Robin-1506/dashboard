import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
file_path = "rapport_pharmacie.xlsx"
stats_df = pd.read_excel(file_path, sheet_name="Statistiques descriptives", engine="openpyxl", skiprows=1)
monthly_df = pd.read_excel(file_path, sheet_name="Synthèse mensuelle", engine="openpyxl")

# Titre
st.title("📊 Dashboard des ventes de médicaments - Pharmacie")

# Section 1 : Statistiques descriptives
st.header("🔍 Statistiques descriptives")
st.dataframe(stats_df.set_index(stats_df.columns[0]))

# Section 2 : Évolution mensuelle
st.header("📈 Évolution mensuelle des ventes")
selected_product = st.selectbox("Choisissez un médicament", monthly_df.columns[2:])
monthly_df["Date"] = pd.to_datetime(monthly_df[["Year", "Month"]].assign(DAY=1))
fig, ax = plt.subplots()
sns.lineplot(data=monthly_df, x="Date", y=selected_product, ax=ax)
ax.set_title(f"Évolution des ventes - {selected_product}")
ax.set_xlabel("Date")
ax.set_ylabel("Ventes")
st.pyplot(fig)

# Section 3 : Recherche par produit et date
st.header("🔎 Recherche ciblée")
selected_year = st.selectbox("Année", sorted(monthly_df["Year"].unique()))
selected_month = st.selectbox("Mois", sorted(monthly_df["Month"].unique()))
selected_product_2 = st.selectbox("Produit", monthly_df.columns[2:])
filtered_value = monthly_df[
    (monthly_df["Year"] == selected_year) & 
    (monthly_df["Month"] == selected_month)
][selected_product_2].values
if filtered_value.size > 0:
    st.success(f"Ventes de {selected_product_2} en {selected_month}/{selected_year} : {filtered_value[0]}")
else:
    st.warning("Aucune donnée disponible pour cette sélection.")

# Section 4 : Synthèse générale
st.header("📊 Synthèse des ventes totales")
# Exclure les colonnes non numériques
numeric_cols = monthly_df.select_dtypes(include='number').columns[2:]
total_sales = monthly_df[numeric_cols].sum()
fig2, ax2 = plt.subplots()
sns.barplot(x=total_sales.index, y=total_sales.values, ax=ax2)
ax2.set_title("Ventes totales par type de médicament")
ax2.set_xlabel("Type de médicament")
ax2.set_ylabel("Ventes totales")
plt.xticks(rotation=45)
st.pyplot(fig2)
