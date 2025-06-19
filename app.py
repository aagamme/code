import streamlit as st
import pandas as pd
import base64
from PIL import Image
from streamlit.components.v1 import html

# Configuração da página
st.set_page_config(page_title="FCN7 - Simulador de Entrega", layout="wide")

# Banner no topo da página
st.markdown(
    """
    <div style="text-align: center; margin-bottom: 30px;">
        <img src="data:image/png;base64,{}" style="width: 100%; max-height: 120px; object-fit: cover;"/>
    </div>
    """.format(base64.b64encode(open("Banner.png", "rb").read()).decode()),
    unsafe_allow_html=True
)

# 🔽 Espaçamento após o banner
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

# Carrega os dados
@st.cache_data
def carregar_dados():
    df = pd.read_excel("Price Table_FCN7_V6.xlsx", sheet_name="Table_Price", skiprows=5)
    df.dropna(axis=1, how='all', inplace=True)
    df = df[df.columns[:9]]
    df.columns = ["Estimated Weight", "Distance", "CAR", "MID-SIZED", "PICKUP TRUCK", "CARGO VAN", "CARGO VAN WITH HIGH TOP", "16' BOX TRUCK", "26' BOX TRUCK"]
    for col in df.columns[2:]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.strip(), errors='coerce')
    df["peso_key"] = df["Estimated Weight"].astype(str).str.strip()
    df["dist_key"] = df["Distance"].astype(str).str.strip()
    return df.reset_index(drop=True)

df = carregar_dados()

# Filtros
pesos = sorted(df["peso_key"].dropna().unique().tolist())
distancias = sorted(df["dist_key"].dropna().unique().tolist())

st.markdown("### Filters")
col1, col2 = st.columns(2)
with col1:
    peso = st.selectbox("Estimated Weight", ["Todos"] + pesos)
with col2:
    distancia = st.selectbox("Distance", ["Todos"] + distancias)

# Imagens dos veículos
imagem_veiculos = {
    "CAR": "Imagem1.png",
    "MID-SIZED": "Imagem2.png",
    "PICKUP TRUCK": "Imagem3.png",
    "CARGO VAN": "Imagem4.png",
    "CARGO VAN WITH HIGH TOP": "Imagem5.png",
    "16' BOX TRUCK": "Imagem6.png",
    "26' BOX TRUCK": "Imagem7.png"
}

# Filtragem de linha
linha = df.copy()
if peso != "Todos":
    linha = linha[linha["peso_key"] == peso]
if distancia != "Todos":
    linha = linha[linha["dist_key"] == distancia]

linha = linha.reset_index(drop=True)

# Estilo dos cards
card_style = """
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 12px;
    padding: 10px;
    width: 180px;
    height: 100px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
    text-align: center;
"""

# HTML para os cards
cards_html = """
<div style='
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 25px;
    justify-items: center;
    margin-top: 20px;
    padding: 0 40px;
'>
"""

for col in imagem_veiculos:
    img_path = imagem_veiculos[col]
    try:
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        img_tag = f"<img src='data:image/png;base64,{img_b64}' width='100' style='margin-bottom:8px;'/>"
    except FileNotFoundError:
        img_tag = "<div style='height:120px; width:120px; background:#eee; border-radius:5px;'></div>"

    if not linha.empty and col in linha.columns:
        try:
            valor = float(linha.iloc[0][col])
            preco_html = f"<div style='font-size: 15px; font-weight: bold; color: #001b60;'>R$ {valor:,.2f}</div>"
        except:
            preco_html = "<div style='color: gray;'>Sem valor</div>"
    else:
        preco_html = "<div style='color: gray;'>Sem valor</div>"

    cards_html += f"""
    <div style="{card_style}">
        {img_tag}
        <div style='font-weight: bold; font-size: 14px; margin-bottom: 5px;'>{col}</div>
        {preco_html}
    </div>
    """

cards_html += "</div>"

html(cards_html, height=600)

st.markdown("---")
st.caption("Simulador FCN7 - Todos os direitos reservados")
