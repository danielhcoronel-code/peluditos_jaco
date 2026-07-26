import streamlit as st

def aplicar_estilos():
    st.markdown("""
    <style>
        /* =======================================================
           1. TIPOGRAFÍAS (Google Fonts)
           ======================================================= */
        /* Letra redondita general */
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');
        /* Letra burbuja para el título principal */
        @import url('https://fonts.googleapis.com/css2?family=Chewy&display=swap');
        
        /* =======================================================
           2. FONDOS Y TEXTOS GENERALES
           ======================================================= */
        /* Fondo cálido crema */
        .stApp { background-color: #FFF9F2; }
        
        /* Aplicamos Nunito a todo menos al título principal */
        h1, h2, h3, h4, p, label { font-family: 'Nunito', sans-serif !important; color: #5D4037 !important; }
        
        /* =======================================================
           3. CLASE ESPECIAL: TÍTULO BURBUJA
           ======================================================= */
        .titulo-burbuja {
            font-family: 'Chewy', cursive !important;
            font-size: 4rem !important; 
            color: #8B4513 !important;
            margin-bottom: -15px !important;
            padding-bottom: 0px !important;
            line-height: 1 !important;
            letter-spacing: 2px;
        }

        /* =======================================================
           4. BOTONES PRINCIPALES (Pantalla Central) 
           ======================================================= */
        section[data-testid="stMain"] div.stButton > button:first-child {
            background-color: #FFB347 !important; 
            color: white !important; 
            border-radius: 20px !important; 
            border: none !important; 
            font-weight: 600 !important; 
            width: 100%;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        section[data-testid="stMain"] div.stButton > button:first-child:hover { 
            background-color: #FF9800 !important; 
            transform: translateY(-2px); 
        }
        
        /* Botones de Urgencia (S.O.S): Rojo sandía */
        section[data-testid="stMain"] button[kind="primary"] { background-color: #FF6B6B !important; }
        section[data-testid="stMain"] button[kind="primary"]:hover { background-color: #FF4757 !important; }
        
        /* =======================================================
           5. BOTONES DEL MENÚ LATERAL (Alineados a la izquierda) 
           ======================================================= */
        section[data-testid="stSidebar"] div.stButton > button {
            background-color: transparent !important;
            color: #5D4037 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            padding: 8px 15px !important;
            border: none !important;
            display: flex !important;
            justify-content: flex-start !important;
        }
        section[data-testid="stSidebar"] div.stButton > button:hover {
            background-color: #f2e8dc !important; 
        }
        section[data-testid="stSidebar"] div.stButton > button div[data-testid="stMarkdownContainer"] {
            width: 100% !important;
            display: flex !important;
            justify-content: flex-start !important;
        }
        section[data-testid="stSidebar"] div.stButton > button p {
            font-size: 16px !important;
            font-weight: 600 !important;
            text-align: left !important;
            margin: 0 !important;
            width: 100% !important;
        }

        /* =======================================================
           6. CAJAS DE INFORMACIÓN
           ======================================================= */
        .caja-info { 
            background-color: #FFF3E0; 
            padding: 20px; 
            border-radius: 15px; 
            border-left: 6px solid #FFB347; 
            margin-bottom: 20px; 
        }
    </style>
    """, unsafe_allow_html=True)
