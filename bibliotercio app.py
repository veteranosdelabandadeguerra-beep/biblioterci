import streamlit as st
import os
import fitz  # Librería PyMuPDF para extraer las portadas

# Configuración de la página
st.set_page_config(page_title="Bibliotercio", page_icon="📚", layout="wide")

# Ruta donde está este archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. MOSTRAR EL LOGO DE LA ASOCIACIÓN
ruta_logo = os.path.join(BASE_DIR, "logo asociación.png")
if os.path.exists(ruta_logo):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(ruta_logo, use_container_width=True)
else:
    st.title("Bibliotercio")

st.markdown("<h1 style='text-align: center;'>Biblioteca Histórica Digital</h1>", unsafe_allow_html=True)
st.markdown("---")

# Estructura de carpetas
ESTRUCTURA = {
    "Libros": [
        "01_Fundacion_Y_Origenes_1920_1926",
        "02_Republica_Y_Guerra_Civil_1931_1939",
        "03_Postguerra_Ifni_Sahara_1940_1975",
        "04_Reorganizacion_Moderna_Y_Misiones",
        "05_Bandas_De_Guerra_Y_Musica",
        "06_Reglamentos_Uniformidad_Y_Heraldica"
    ],
    "Expedientes": [],
    "Diarios_de_operaciones": [],
    "Revistas": [],
    "Decretos": []
}

# Crear carpetas físicas
os.makedirs(os.path.join(BASE_DIR, "imagenes"), exist_ok=True)
for categoria, subcategorias in ESTRUCTURA.items():
    ruta_categoria = os.path.join(BASE_DIR, categoria)
    os.makedirs(ruta_categoria, exist_ok=True)
    for sub in subcategorias:
        ruta_sub = os.path.join(ruta_categoria, sub)
        os.makedirs(ruta_sub, exist_ok=True)

# 2. FUNCIÓN PARA MOSTRAR LA ESTANTERÍA DE LIBROS CON PORTADAS REALES
def mostrar_estanteria(ruta):
    if not os.path.exists(ruta):
        return
    
    # Leer solo archivos PDF
    archivos = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f)) and f.lower().endswith('.pdf')]
    
    if archivos:
        st.markdown("<br>", unsafe_allow_html=True)
        libros_por_fila = 5  # Número de libros que caben en una balda
        
        # Generar filas y columnas
        for i in range(0, len(archivos), libros_por_fila):
            columnas = st.columns(libros_por_fila)
            for j, col in enumerate(columnas):
                if i + j < len(archivos):
                    archivo = archivos[i + j]
                    ruta_archivo = os.path.join(ruta, archivo)
                    # Limpiar el nombre para el pie de foto
                    nombre_limpio = archivo.replace(".pdf", "").replace(".PDF", "")
                    
                    with col:
                        try:
                            # Abrir el PDF y extraer la página 0 (la portada)
                            doc = fitz.open(ruta_archivo)
                            pagina = doc.load_page(0)
                            # Generar una miniatura ligera para que no sature la aplicación
                            pix = pagina.get_pixmap(matrix=fitz.Matrix(0.25, 0.25))
                            img_bytes = pix.tobytes("png")
                            
                            # Mostrar la portada extraída
                            st.image(img_bytes, use_container_width=True)
                            st.markdown(f"<p style='text-align: center; font-size: 13px; font-weight: bold;'>{nombre_limpio}</p>", unsafe_allow_html=True)
                            doc.close()
                        except:
                            # Si el PDF está dañado o protegido, muestra un diseño de respaldo
                            st.markdown(f"""
                            <div style="background-color: #2b2b2b; border-left: 12px solid #6b0000; border-radius: 4px 8px 8px 4px; padding: 15px 10px; text-align: center; height: 180px; box-shadow: 3px 4px 8px rgba(0,0,0,0.5); display: flex; flex-direction: column; justify-content: center; align-items: center; border: 1px solid #444;">
                                <div style="font-size: 30px; margin-bottom: 12px;">📄</div>
                                <div style="font-size: 13px; font-weight: bold; color: #e0e0e0; word-wrap: break-word;">{nombre_limpio}</div>
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.info("Estantería vacía. Añade tus archivos PDF a la carpeta.")

# Función para cargar imagen de las cabeceras
def mostrar_portada(nombre_archivo):
    ruta_img = os.path.join(BASE_DIR, "imagenes", nombre_archivo)
    if os.path.exists(ruta_img):
        st.image(ruta_img, use_container_width=True)

# Nombres exactos de tus cabeceras
imagenes_principales = {
    "Libros": "livros.jpeg",
    "Expedientes": "expedientes.jpeg",
    "Diarios_de_operaciones": "diarios de operaciones.jpeg",
    "Revistas": "revistas.jpeg",
    "Decretos": "decretos.jpeg"
}

imagenes_sub_libros = {
    "01_Fundacion_Y_Origenes_1920_1926": "origenes.jpeg",
    "02_Republica_Y_Guerra_Civil_1931_1939": "republica y guerra civil.jpeg",
    "03_Postguerra_Ifni_Sahara_1940_1975": "Postguerra, Ifni y Sahara.jpeg",
    "04_Reorganizacion_Moderna_Y_Misiones": "Reorganización Moderna y Misiones en el Exterior.jpeg",
    "05_Bandas_De_Guerra_Y_Musica": "Bandas de Guerra y Música Legionaria.jpeg",
    "06_Reglamentos_Uniformidad_Y_Heraldica": "Reglamentos, Uniformidad y Heráldica.jpeg"
}

# 3. RENDERIZAR INTERFAZ
pestañas = st.tabs([c.replace("_", " ") for c in ESTRUCTURA.keys()])

for i, (categoria, subcategorias) in enumerate(ESTRUCTURA.items()):
    with pestañas[i]:
        mostrar_portada(imagenes_principales[categoria])
        ruta_categoria = os.path.join(BASE_DIR, categoria)
        
        if subcategorias:
            st.markdown("### Selecciona una época histórica:")
            sub_pestañas = st.tabs([sub.replace("_", " ") for sub in subcategorias])
            for j, sub in enumerate(subcategorias):
                with sub_pestañas[j]:
                    mostrar_portada(imagenes_sub_libros[sub])
                    ruta_sub = os.path.join(ruta_categoria, sub)
                    st.markdown("---")
                    mostrar_estanteria(ruta_sub)
        else:
            st.markdown("---")
            mostrar_estanteria(ruta_categoria)