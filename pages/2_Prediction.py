# pages/2_Prediction.py
import streamlit as st
import pandas as pd
import pickle  # ou import joblib si utilisé
import shap
import plotly.graph_objects as go
import streamlit.components.v1 as components
import base64

# Fonction pour afficher les graphiques SHAP
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)

# Fonction pour créer une barre de scoring avec Plotly Gauge
def plot_gauge(prob):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob*100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Probabilité de Quitter (%)"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 60], 'color': "orange"},
                {'range': [60, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': prob*100
            }
        }
    ))
    fig.update_layout(height=300, margin={'t': 50, 'b': 0, 'l':0, 'r':0})
    return fig

# Fonction pour générer des graphiques de dispersion avec Plotly
def plot_dispersion_plotly(df, selected_features, employee_values):
    num_features = len(selected_features)
    cols_per_row = 2  # Nombre de colonnes par rangée
    rows = (num_features + cols_per_row - 1) // cols_per_row  # Calcul du nombre de rangées nécessaires

    for i in range(rows):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            feature_idx = i * cols_per_row + j
            if feature_idx < num_features:
                feature = selected_features[feature_idx]
                employee_value = employee_values[feature]
                
                # Créer le graphique avec Plotly
                fig = go.Figure()

                # Ajouter l'histogramme
                fig.add_trace(go.Histogram(
                    x=df[feature],
                    nbinsx=20,
                    name='Distribution',
                    marker_color='lightblue',
                    opacity=0.7
                ))

                # Ajouter une ligne verticale pour la valeur de l'employé
                fig.add_vline(x=employee_value, line=dict(color='red', width=2, dash='dash'), 
                             annotation=dict(text=f"Valeur de l'employé: {employee_value}", 
                                             showarrow=True, arrowhead=1, ax=0, ay=-40))

                # Mise en page du graphique
                fig.update_layout(
                    title=f'Distribution de {feature}',
                    xaxis_title=feature,
                    yaxis_title='Fréquence',
                    bargap=0.2,
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                    showlegend=False
                )

                # Afficher le graphique dans la colonne correspondante
                with cols[j]:
                    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="Prédiction - Turnover", layout="wide")

# ----------------------------
# Chargement des données
# ----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("df_model.csv")
        return df
    except FileNotFoundError:
        st.error("Le fichier 'df_model.csv' n'a pas été trouvé.")
        return pd.DataFrame()

df = load_data()

# ----------------------------
# Chargement du modèle
# ----------------------------
@st.cache_resource
def load_model():
    try:
        with open("logistic_model.pkl", "rb") as f:
            model = pickle.load(f)  # ou joblib.load(f) si utilisé
        return model
    except FileNotFoundError:
        st.error("Le fichier 'logistic_model.pkl' n'a pas été trouvé.")
        return None
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle : {e}")
        return None

model = load_model()

# ----------------------------
# Vérification du type du modèle
# ----------------------------
if model is not None:
    st.write(f"**Type du modèle chargé :** {type(model)}")
    if not hasattr(model, "predict"):
        st.error("Le modèle chargé ne possède pas la méthode 'predict'. Vérifiez que 'logistic_model.pkl' contient bien un modèle de régression logistique.")
        st.stop()
else:
    st.stop()

# ----------------------------
# Définir les features utilisées par le modèle
# ----------------------------
model_features = [
    "satisfaction_level",
    "last_evaluation",
    "number_project",
    "average_montly_hours",
    "time_spend_company",
    "work_accident",
    "salary_encoded"
]

st.title("Page de Prédiction")
st.write("Utilisez la régression logistique pour prédire si un employé va quitter l'entreprise.")

# Vérifier que le DataFrame n'est pas vide
if df.empty:
    st.write("Aucune donnée chargée.")
    st.stop()

# ----------------------------
# Sélection de l'ID de l'employé
# ----------------------------
unique_ids = df["id_colab"].unique()
selected_id = st.selectbox("Sélectionnez l'ID employé :", options=unique_ids)

# Récupérer les informations de l'employé sélectionné
row_emp = df[df["id_colab"] == selected_id]

if row_emp.empty:
    st.write("ID introuvable dans les données.")
    st.stop()

# ----------------------------
# Préparer les données pour la prédiction
# ----------------------------
X_emp = row_emp[model_features]

# ----------------------------
# Prédiction
# ----------------------------
try:
    pred = model.predict(X_emp)
    pred_proba = model.predict_proba(X_emp)
    prob_quit = pred_proba[0][1]  # Probabilité de quitter
except AttributeError as e:
    st.error(f"Erreur lors de la prédiction : {e}")
    st.stop()

# ----------------------------
# Fonction pour attribuer un niveau de risque
# ----------------------------
def assign_risk_level(prob):
    if prob < 0.3:
        return "Faible Risque"
    elif 0.3 <= prob < 0.6:
        return "Risque Modéré"
    else:
        return "Haut Risque"

risk_level = assign_risk_level(prob_quit)

# ----------------------------
# Mise en Page Centrée pour le Graphique et le DataFrame
# ----------------------------
# Créer trois colonnes : gauche vide, centre (contenant gauge et info), droite vide
left, center, right = st.columns([1, 3, 1])

with center:
    # Créer deux sous-colonnes pour le gauge et les informations
    gauge_col, info_col = st.columns([1.5, 2])
    
    with gauge_col:
        # Afficher la barre de scoring
        gauge_fig = plot_gauge(prob_quit)
        st.plotly_chart(gauge_fig, use_container_width=True)
    
    with info_col:
        # Afficher les détails de la prédiction
        st.markdown(f"**Probabilité de quitter :** {prob_quit*100:.2f}%")
        st.markdown(f"**Prédiction (left) :** {'Quitte (1)' if pred[0] == 1 else 'Reste (0)'}")
        
        # Afficher le niveau de risque avec des couleurs
        if risk_level == "Faible Risque":
            st.markdown("**Niveau de Risque :** <span style='color: green;'>Faible Risque</span>", unsafe_allow_html=True)
        elif risk_level == "Risque Modéré":
            st.markdown("**Niveau de Risque :** <span style='color: orange;'>Risque Modéré</span>", unsafe_allow_html=True)
        else:
            st.markdown("**Niveau de Risque :** <span style='color: red;'>Haut Risque</span>", unsafe_allow_html=True)
    
    st.markdown("---")  # Ligne de séparation

    # Afficher le DataFrame centré
    st.subheader("Détails de l'Employé")
    st.dataframe(row_emp[model_features])

# ----------------------------
# Section de Dispersion des Features (Alignée à Gauche)
# ----------------------------
st.markdown("---")  # Ligne de séparation
st.subheader("Visualisation de la Dispersion des Features")

# Ajouter un multiselect pour choisir les features à visualiser
selected_features = st.multiselect(
    "Sélectionnez les features pour visualiser leur dispersion :",
    options=model_features,
    default=[]  # Pas de sélection par défaut
)

# Récupérer les valeurs de l'employé pour les features sélectionnées
employee_values = {}
for feature in selected_features:
    employee_values[feature] = row_emp.iloc[0][feature]

# Générer et afficher les graphiques de dispersion pour les features sélectionnées
if selected_features:
    plot_dispersion_plotly(df, selected_features, employee_values)
else:
    st.info("Veuillez sélectionner au moins un feature pour afficher les graphiques de dispersion.")

# ----------------------------
# Bouton pour afficher les Explications SHAP (Aligné à Gauche)
# ----------------------------
st.markdown("---")  # Ligne de séparation
if st.button("Afficher les Explications SHAP"):
    st.subheader("Explications SHAP")
    try:
        explainer = shap.Explainer(model, df[model_features])
        shap_values = explainer(X_emp)
        force_plot = shap.plots.force(shap_values[0], matplotlib=False)
        st_shap(force_plot, height=600)  # Graphique plus long
    except Exception as e:
        st.error(f"Erreur lors du calcul des valeurs SHAP : {e}")

