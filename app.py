import streamlit as st
import pandas as pd
import numpy as np
import os

# ==============================================================================
# 1. ARQUITECTURA DE LA INTERFAZ PRO (BI & CORPORATIVO)
# ==============================================================================
st.set_page_config(
    page_title="World Cup Intelligence Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS avanzados para transformar la UI por completo
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; max-width: 100%; }
    h1 { color: #0F172A; font-weight: 800; font-size: 2.4rem; letter-spacing: -1px; margin-bottom: 0.2rem; }
    h2 { color: #1E3A8A; font-weight: 700; font-size: 1.5rem; margin-top: 1.5rem; border-bottom: 2px solid #E2E8F0; padding-bottom: 0.5rem; }
    h3 { color: #334155; font-weight: 600; font-size: 1.1rem; margin-top: 0.5rem; }
    .kpi-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #0F172A 100%);
        color: #FFFFFF;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .kpi-title { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #93C5FD; }
    .kpi-value { font-size: 2rem; font-weight: 800; line-height: 1.2; margin-top: 0.25rem; }
    .kpi-subtext { font-size: 0.75rem; color: #CBD5E1; margin-top: 0.4rem; font-style: italic; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: #F8FAFC; padding: 6px; border-radius: 8px; border: 1px solid #E2E8F0; }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 6px;
        padding: 10px 24px;
        font-weight: 600;
        color: #64748B;
        transition: all 0.2s ease;
        border: none !important;
    }
    .stTabs [aria-selected="true"] { background-color: #1E3A8A !important; color: #FFFFFF !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. CAPA DE GESTIÓN Y CARGA SEGURA DE DATOS
# ==============================================================================
archivo_nombre = "WorldCupMatches-selected-columns.csv"
ruta_al_csv = os.path.join("data", archivo_nombre)

if not os.path.exists(ruta_al_csv):
    ruta_al_csv = archivo_nombre

df = pd.read_csv(ruta_al_csv)

# Ingeniería de variables básica con columnas garantizadas
df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(0).astype(int)
df['Home Team Goals'] = pd.to_numeric(df['Home Team Goals'], errors='coerce').fillna(0).astype(int)
df['Away Team Goals'] = pd.to_numeric(df['Away Team Goals'], errors='coerce').fillna(0).astype(int)
df['Total Goles'] = df['Home Team Goals'] + df['Away Team Goals']

df['Home Team Name'] = df['Home Team Name'].fillna('Desconocido').astype(str).str.strip()
df['Away Team Name'] = df['Away Team Name'].fillna('Desconocido').astype(str).str.strip()

def calcular_resultado(row):
    if row['Home Team Goals'] > row['Away Team Goals']:
        return 'Victoria Local 🏠'
    elif row['Away Team Goals'] > row['Home Team Goals']:
        return 'Victoria Visitante ✈️'
    return 'Empate 🤝'

df['Resultado_Clase'] = df.apply(calcular_resultado, axis=1)

# ==============================================================================
# 3. PANEL DE CONTROL
# ==============================================================================
st.sidebar.title("Panel de Control")
st.sidebar.markdown("Modifica el entorno analítico global:")

lista_anios = sorted(list(df['Year'].unique()), reverse=True)
anio_sel = st.sidebar.selectbox("Seleccionar Edición del Mundial:", options=["Todos los Tiempos"] + lista_anios)

paises_disponibles = sorted(list(set(df['Home Team Name'].unique()) | set(df['Away Team Name'].unique())))
pais_sel = st.sidebar.selectbox("Enfoque Particular por Selección:", options=["Ver Todos los Países"] + paises_disponibles)

fases_disponibles = sorted(list(df['Stage'].dropna().unique())) if 'Stage' in df.columns else []
fase_sel = st.sidebar.selectbox("Filtrar por Fase del Torneo:", options=["Todas las Fases"] + fases_disponibles)

# Lógica de filtrado dinámico cruzado seguro
df_filtrado = df.copy()

if anio_sel != "Todos los Tiempos":
    df_filtrado = df_filtrado[df_filtrado['Year'] == int(anio_sel)]

if pais_sel != "Ver Todos los Países":
    df_filtrado = df_filtrado[(df_filtrado['Home Team Name'] == pais_sel) | (df_filtrado['Away Team Name'] == pais_sel)]

if fase_sel != "Todas las Fases":
    df_filtrado = df_filtrado[df_filtrado['Stage'] == fase_sel]

# ==============================================================================
# 4. DASHBOARD HEADER & KPI PANELS
# ==============================================================================
st.title("📊 Dashboard Ejecutivo: Business Intelligence de los Mundiales")
st.markdown(f"Plataforma interactiva de analítica avanzada. *Filtros actuales: **{anio_sel}** | Enfoque: **{pais_sel}** | Fase: **{fase_sel}***")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Muestra de Partidos</div><div class="kpi-value">{len(df_filtrado):,}</div><div class="kpi-subtext">Volumen total analizado</div></div>""", unsafe_allow_html=True)
with kpi_col2:
    goles_t = int(df_filtrado['Total Goles'].sum()) if not df_filtrado.empty else 0
    st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Volumen de Goles</div><div class="kpi-value">{goles_t:,}</div><div class="kpi-subtext">Anotaciones globales logradas</div></div>""", unsafe_allow_html=True)
with kpi_col3:
    ratio_g = df_filtrado['Total Goles'].mean() if not df_filtrado.empty else 0.0
    st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Ratio de Efectividad</div><div class="kpi-value">{ratio_g:.2f}</div><div class="kpi-subtext">Promedio de goles por Match</div></div>""", unsafe_allow_html=True)
with kpi_col4:
    volatilidad = df_filtrado['Total Goles'].std() if len(df_filtrado) > 1 else 0.0
    st.markdown(f"""<div class="kpi-container"><div class="kpi-title">Volatilidad (Std Dev)</div><div class="kpi-value">{volatilidad:.2f}</div><div class="kpi-subtext">Desviación estándar del gol</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==============================================================================
# 5. MATRIZ DE MÓDULOS NAVEGABLES
# ==============================================================================
tab_overview, tab_performance = st.tabs([
    "📊 Macrotendencias Globales", 
    "🏆 Eficiencia y Performance Técnico"
])

# --------------------------------------------------------------------------
# PESTAÑA 1: MACROTENDENCIAS
# --------------------------------------------------------------------------
with tab_overview:
    if df_filtrado.empty:
        st.warning("No existen registros para la combinación de filtros seleccionada en el Panel de Control.")
    else:
        col_ov1, col_ov2 = st.columns(2)
        with col_ov1:
            st.markdown("## Evolución Cronológica Acumulada")
            df_temp = df_filtrado.reset_index(drop=True)
            df_temp['Acumulado Histórico'] = df_temp['Total Goles'].cumsum()
            st.line_chart(data=df_temp, y='Acumulado Histórico', color="#1E3A8A", use_container_width=True)
            
        with col_ov2:
            st.markdown("## Frecuencia de Distribución del Gol")
            g_dist = df_filtrado['Total Goles'].value_counts().reset_index()
            g_dist.columns = ['Goles', 'Partidos']
            st.bar_chart(data=g_dist, x='Goles', y='Partidos', color="#10B981", use_container_width=True)

        st.markdown("## Análisis de Tendencia de Resultados (Localía vs Visitante)")
        res_counts = df_filtrado['Resultado_Clase'].value_counts().reset_index()
        res_counts.columns = ['Tipo de Resultado', 'Cantidad de Partidos']
        st.bar_chart(data=res_counts, x='Tipo de Resultado', y='Cantidad de Partidos', color="#4F46E5", use_container_width=True)

# --------------------------------------------------------------------------
# PESTAÑA 2: PERFORMANCE TÉCNICO
# --------------------------------------------------------------------------
with tab_performance:
    if df_filtrado.empty:
        st.warning("No existen registros para la combinación de filtros seleccionada en el Panel de Control.")
    else:
        goles_h = df_filtrado.groupby('Home Team Name')['Home Team Goals'].sum().reset_index()
        goles_h.columns = ['Selección', 'Goles Marcados Local']
        top_casa = goles_h.nlargest(10, 'Goles Marcados Local')

        goles_a = df_filtrado.groupby('Away Team Name')['Away Team Goals'].sum().reset_index()
        goles_a.columns = ['Selección', 'Goles Marcados Visitante']
        top_fuera = goles_a.nlargest(10, 'Goles Marcados Visitante')

        st.markdown("## 📊 Distribución de Potencias Ofensivas (Goles Convertidos)")
        col_pf1, col_pf2 = st.columns(2)
        
        with col_pf1:
            st.write("**Top 10 Selecciones con Más Goles de Local:**")
            st.dataframe(top_casa, use_container_width=True, hide_index=True)
            
        with col_pf2:
            st.write("**Top 10 Selecciones con Más Goles de Visitante:**")
            st.dataframe(top_fuera, use_container_width=True, hide_index=True)
