import streamlit as st
import pandas as pd
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="FCN7 - Delivery Simulator", layout="wide", initial_sidebar_state="collapsed")

# --- FUNÇÃO PARA DEFINIR FUNDO E ESTILO ---
def set_page_background(image_file):
    try:
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
    except FileNotFoundError:
        st.error(f"ERROR: Image file '{image_file}' not found.")
        return

    style = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

        .stApp {{
            background-image: url("data:image/png;base64,{b64_encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            height: 100vh;
            font-family: 'Montserrat', sans-serif;
            --primary-color: #001b60;
            --secondary-color: #ff7f0e;
            --text-color: #ffffff;
            --card-text-color: #333;
            --card-background-color: #ffffff;
        }}

        .stApp > header {{
            background-color: transparent;
        }}
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"] {{
            display: none !important;
        }}
        .main .block-container {{
            padding: 0 !important;
            margin-top: 0 !important;
        }}

        main > div:first-child {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }


        h1, h3 {{
            color: var(--text-color) !important;
            text-align: center;
            text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.6);
        }}
        h1 {{ font-weight: 700; padding-top: 1rem; }}
        h3 {{ font-weight: 600; }}

        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: rgba(0, 27, 96, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.7);
            border-radius: 8px;
        }}
        .stSelectbox div[data-baseweb="select"] > div > div,
        .stSelectbox div[data-baseweb="select"] > span {{
            color: var(--text-color) !important;
        }}

        .vehicle-card {{
            background-color: var(--card-background-color);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            border: 1px solid #ddd;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 220px;
        }}

        .vehicle-name {{
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--card-text-color);
            margin-top: 10px;
            flex-grow: 1; 
        }}
        .vehicle-price {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--secondary-color);
            margin-top: 8px;
        }}
        .price-not-available {{
            color: #777;
            font-size: 0.9rem;
            margin-top: 8px;
        }}

        hr {{
            border-top: 1px solid rgba(255, 255, 255, 0.5);
            margin: 1.5rem 0;
        }}

        footer {{
            text-align: center;
            padding: 2rem 0;
            color: var(--text-color) !important;
            font-weight: 600;
            text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.6);
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# --- APLICA ESTILO E FUNDO ---
set_page_background('Capa_Dashboard.png')

# --- TÍTULO PRINCIPAL ---
st.markdown("<h1>FCN7 Simulator</h1>", unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS ---
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("Price Table_FCN7_V6.xlsx", sheet_name="Table_Price", skiprows=5)
        df.dropna(axis=1, how='all', inplace=True)
        df = df.iloc[:, :9]
        df.columns = ["Estimated Weight", "Distance", "CAR", "MID-SIZED", "PICKUP TRUCK", "CARGO VAN", "CARGO VAN WITH HIGH TOP", "16' BOX TRUCK", "26' BOX TRUCK"]
        for col in df.columns[2:]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
        df["peso_key"] = df["Estimated Weight"].astype(str).str.strip()
        df["dist_key"] = df["Distance"].astype(str).str.strip()
        return df.reset_index(drop=True)
    except FileNotFoundError:
        return None

df = carregar_dados()

# --- CONTEÚDO PRINCIPAL ---
if df is None:
    st.error("ERROR: File 'Price Table_FCN7_V6.xlsx' not found.")
else:
    st.markdown("<h3>Select Filters</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        weights = ["Select Estimated Weight"] + sorted(df["peso_key"].dropna().unique().tolist())
        weight = st.selectbox("Estimated Weight", weights, index=0)

    with col2:
        distances = ["Select Distance"] + sorted(df["dist_key"].dropna().unique().tolist())
        distance = st.selectbox("Distance", distances, index=0)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Prices by Vehicle Type</h3>", unsafe_allow_html=True)

    imagem_veiculos = {
        "CAR": "Imagem1.png", "MID-SIZED": "Imagem2.png", "PICKUP TRUCK": "Imagem3.png",
        "CARGO VAN": "Imagem4.png", "CARGO VAN WITH HIGH TOP": "Imagem5.png",
        "16' BOX TRUCK": "Imagem6.png", "26' BOX TRUCK": "Imagem7.png"
    }

    linha = df.copy()
    if weight != "Select Estimated Weight":
        linha = linha[linha["peso_key"] == weight]
    if distance != "Select Distance":
        linha = linha[linha["dist_key"] == distance]
    linha = linha.reset_index(drop=True)

    if linha.empty and (weight != "Select Estimated Weight" or distance != "Select Distance"):
        st.warning("No results found for selected filters.", icon="⚠️")
    else:
        num_veiculos = len(imagem_veiculos)
        cols = st.columns(num_veiculos)

        for idx, (veiculo, img_path) in enumerate(imagem_veiculos.items()):
            with cols[idx]:
                try:
                    with open(img_path, "rb") as f:
                        img_b64 = base64.b64encode(f.read()).decode()
                    img_tag = f"<img src='data:image/png;base64,{img_b64}' style='height:70px; object-fit:contain;'/>"
                except FileNotFoundError:
                    img_tag = f"<div style='height:70px; width:100%; background:#eee; border-radius:5px; display:flex; align-items:center; justify-content:center; color:#999; font-size:12px;'>{img_path}<br>not found</div>"

                preco_html = "<div class='price-not-available'>Select filters</div>"
                if not linha.empty and veiculo in linha.columns:
                    try:
                        valor = float(linha.iloc[0][veiculo])
                        preco_html = f"<div class='vehicle-price'>R$ {valor:,.2f}</div>"
                    except (ValueError, TypeError):
                        preco_html = "<div class='price-not-available'>Unavailable</div>"

                nome_veiculo_formatado = veiculo.replace("_", " ").title()

                st.markdown(f"""
                <div class="vehicle-card">
                    <div>{img_tag}</div>
                    <div class="vehicle-name">{nome_veiculo_formatado}</div>
                    <div>{preco_html}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<footer>FCN7 - All rights reserved</footer>", unsafe_allow_html=True)
