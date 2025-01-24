# pages/1_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard - Turnover", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("df_model.csv")
    return df

df = load_data()

st.title("KPI Dashboard - Turnover")
st.subheader("Visualisez les indicateurs clés de performance")

# ----------------------------
# Sélecteur de job (filtre)
# ----------------------------
all_jobs = sorted(df["job"].unique())
selected_job = st.selectbox(
    "Choisissez un Job à afficher :",
    options=["Tous"] + all_jobs,
    index=0
)

if selected_job != "Tous":
    df = df[df["job"] == selected_job]

# ----------------------------
# Calculs des métriques de base
# ----------------------------
if not df.empty:
    turnover_rate = df["left"].mean() * 100
    avg_satisfaction = df["satisfaction_level"].mean()
    avg_monthly_hours = df["average_montly_hours"].mean()

    # Calcul de l'écart de satisfaction entre partants et restants
    satisfaction_left = df.loc[df["left"] == 1, "satisfaction_level"].mean()
    satisfaction_stay = df.loc[df["left"] == 0, "satisfaction_level"].mean()
    satisfaction_gap = satisfaction_stay - satisfaction_left if not pd.isna(satisfaction_left) and not pd.isna(satisfaction_stay) else 0
else:
    turnover_rate = 0
    avg_satisfaction = 0
    avg_monthly_hours = 0
    satisfaction_gap = 0

# ----------------------------
# Affichage des 4 KPI
# ----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Turnover Global (%)", f"{turnover_rate:.1f}%")
    with st.expander("Détails sur le Turnover"):
        if not df.empty:
            fig_turnover = px.histogram(df, x="left", title="Histogramme du Turnover (0=reste, 1=quitte)")
            st.plotly_chart(fig_turnover, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

with col2:
    st.metric("Satisfaction Moyenne", f"{avg_satisfaction:.2f}")
    with st.expander("Détails sur la Satisfaction"):
        if not df.empty:
            fig_satisfaction = px.histogram(
                df, 
                x="satisfaction_level", 
                nbins=20, 
                title="Histogramme du niveau de Satisfaction"
            )
            st.plotly_chart(fig_satisfaction, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

with col3:
    st.metric("Heures Mensuelles Moyennes", f"{avg_monthly_hours:.0f} h")
    with st.expander("Détails sur les Heures Mensuelles"):
        if not df.empty:
            fig_hours = px.histogram(
                df, 
                x="average_montly_hours", 
                nbins=20, 
                title="Histogramme des Heures Mensuelles"
            )
            st.plotly_chart(fig_hours, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

with col4:
    st.metric("Écart de Satisfaction", f"{satisfaction_gap:.2f} pts")
    with st.expander("Satisfaction : Partants vs Restants"):
        if not df.empty:
            df_compare = pd.DataFrame({
                "Statut": ["Partants", "Restants"],
                "Satisfaction": [satisfaction_left, satisfaction_stay]
            })
            fig_comp = px.bar(
                df_compare, 
                x="Statut", 
                y="Satisfaction", 
                range_y=[0,1], 
                title="Comparaison Satisfaction"
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.write("Aucune donnée pour ce filtre.")

# ----------------------------
# Bloc de visualisations (2x2)
# ----------------------------
st.header("Visualisations Clés")

row1_col1, row1_col2 = st.columns(2)

# 1) Turnover par Niveau de Salaire
with row1_col1:
    if not df.empty:
        df_salary = df.groupby("salary_encoded", as_index=False)["left"].mean()
        fig_salary = px.bar(
            df_salary, 
            x="salary_encoded", 
            y="left",
            title="Turnover par Niveau de Salaire (Moyenne)",
            labels={"salary_encoded": "Niveau de Salaire", "left": "Taux de Turnover"}
        )
        st.plotly_chart(fig_salary, use_container_width=True)
    else:
        st.write("Aucune donnée.")

# 2) Job vs Turnover (Pie chart)
with row1_col2:
    if not df.empty:
        df_job_full = df.groupby("job").agg(
            total_count=("job", "count"),
            left_sum=("left", "sum")
        ).reset_index()
        df_job_full["left_rate"] = df_job_full["left_sum"] / df_job_full["total_count"]

        fig_job = go.Figure()
        # Trace 1 : Nombre absolu
        fig_job.add_trace(go.Pie(
            labels=df_job_full["job"],
            values=df_job_full["left_sum"],
            name="Départs (Absolu)",
            hole=0.3
        ))
        # Trace 2 : Taux de départs
        fig_job.add_trace(go.Pie(
            labels=df_job_full["job"],
            values=df_job_full["left_rate"],
            name="Taux de départs",
            visible=False,
            hole=0.3
        ))
        fig_job.update_layout(
            title="Nombre de Départs par Poste (Absolu) vs Taux de Départ par Poste",
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[
                        dict(
                            label="Nombre (Absolu)",
                            method="update",
                            args=[{"visible": [True, False]}]
                        ),
                        dict(
                            label="Taux (Pourcentage)",
                            method="update",
                            args=[{"visible": [False, True]}]
                        )
                    ]
                )
            ]
        )
        st.plotly_chart(fig_job, use_container_width=True)
    else:
        st.write("Aucune donnée.")

row2_col1, row2_col2 = st.columns(2)

# 3) Turnover vs Heures Mensuelles
with row2_col1:
    if not df.empty:
        df_hours_evol = df.groupby("average_montly_hours", as_index=False)["left"].mean()
        df_hours_evol.rename(columns={"average_montly_hours": "x_value", "left": "turnover"}, inplace=True)
        fig_hours_evol = px.line(
            df_hours_evol.sort_values("x_value"),
            x="x_value",
            y="turnover",
            title="Évolution du Turnover selon les Heures Mensuelles",
            labels={"x_value": "Heures Mensuelles", "turnover": "Taux de Turnover"}
        )
        turnover_mean = df["left"].mean()
        fig_hours_evol.add_hline(
            y=turnover_mean,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Turnover Moyen: {turnover_mean:.2f}",
            annotation_position="top left"
        )
        st.plotly_chart(fig_hours_evol, use_container_width=True)
    else:
        st.write("Aucune donnée.")

# 4) Turnover vs Satisfaction
with row2_col2:
    if not df.empty:
        df_satisf_evol = df.groupby("satisfaction_level", as_index=False)["left"].mean()
        df_satisf_evol.rename(columns={"satisfaction_level": "x_value", "left": "turnover"}, inplace=True)
        fig_satisf_evol = px.line(
            df_satisf_evol.sort_values("x_value"),
            x="x_value",
            y="turnover",
            title="Évolution du Turnover selon la Satisfaction",
            labels={"x_value": "Niveau de Satisfaction", "turnover": "Taux de Turnover"}
        )
        turnover_mean_satisf = df["left"].mean()
        fig_satisf_evol.add_hline(
            y=turnover_mean_satisf,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Turnover Moyen: {turnover_mean_satisf:.2f}",
            annotation_position="top left"
        )
        st.plotly_chart(fig_satisf_evol, use_container_width=True)
    else:
        st.write("Aucune donnée.")

# ----------------------------
# Scatter Plot Dynamique (fin de page)
# ----------------------------
st.subheader("Scatter Plot Dynamique")

if not df.empty:
    numeric_cols = [
        "satisfaction_level",
        "last_evaluation",
        "number_project",
        "average_montly_hours",
        "time_spend_company",
        "salary_encoded"
    ]
    x_var = st.selectbox("Axe X", numeric_cols, index=0)
    y_var = st.selectbox("Axe Y", numeric_cols, index=3)

    fig_scatter = px.scatter(
        df,
        x=x_var,
        y=y_var,
        color="left",
        title=f"{x_var} vs {y_var} (coloré par Turnover)",
        hover_data=["id_colab", "job"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.write("Aucune donnée.")
