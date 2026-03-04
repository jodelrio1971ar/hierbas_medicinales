# 05_app.py

"""
🌿 Hierbas Medicinales — Sabiduría Ancestral para la Vida Moderna
Sitio web educativo construido con Streamlit
"""

import streamlit as st
from pathlib import Path
import base64
import time
import os
from io import BytesIO

# ---------------------------------------------------------------------------
# Configuración de página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="🌿 Hierbas Medicinales — Sabiduría Ancestral",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
IMG_DIR = BASE_DIR / "public" / "Imagenes"
HIST_DIR = BASE_DIR / "public" / "Historia"

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def load_md(filepath: Path) -> str:
    """Lee un archivo Markdown y devuelve su contenido."""
    return filepath.read_text(encoding="utf-8")


def img_to_base64(path: Path) -> str:
    """Convierte una imagen a base64 para uso inline en HTML/CSS."""
    return base64.b64encode(path.read_bytes()).decode()


def local_image_html(path: Path, alt: str = "", extra_style: str = "") -> str:
    """Genera un tag <img> con la imagen embebida en base64."""
    b64 = img_to_base64(path)
    suffix = path.suffix.lstrip(".")
    mime = f"image/{suffix}" if suffix != "jpg" else "image/jpeg"
    return (
        f'<img src="data:{mime};base64,{b64}" '
        f'alt="{alt}" style="width:100%;border-radius:16px;{extra_style}" />'
    )


# ---------------------------------------------------------------------------
# CSS personalizado
# ---------------------------------------------------------------------------
def load_css(filepath: Path) -> str:
    """Lee el archivo CSS externo y lo envuelve en un tag <style>."""
    css_content = filepath.read_text(encoding="utf-8")
    return f'<style>\n{css_content}\n</style>'

st.markdown(load_css(BASE_DIR / "style.css"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Funciones de sección
# ---------------------------------------------------------------------------

def render_divider(icon: str = "&#9672;"):
    st.markdown(
        f'<div class="fancy-divider">'
        f'  <span class="line"></span>'
        f'  <span class="icon">{icon}</span>'
        f'  <span class="line"></span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_hero():
    """Sección hero con imagen de fondo y título superpuesto."""
    b64 = img_to_base64(IMG_DIR / "hero-bg.jpg")
    st.markdown(
        f"""
        <div class="hero-container">
            <img src="data:image/jpeg;base64,{b64}" alt="Hierbas medicinales" />
            <div class="hero-overlay">
                <h1>🌿 Hierbas Medicinales</h1>
                <p>
                    Descubrí la sabiduría ancestral que la naturaleza nos ofrece.
                    Desde las civilizaciones antiguas hasta la ciencia moderna,
                    las plantas medicinales han sido aliadas de la salud humana.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_intro():
    """Texto introductorio."""
    st.markdown(
        '<h2 class="section-title">¿Por Qué las Hierbas Medicinales?</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="centered-description">'
        "Durante miles de años, la humanidad encontró en las plantas la clave para aliviar el dolor, "
        "curar enfermedades y mantener el bienestar. Hoy, la ciencia moderna valida lo que nuestros "
        "ancestros ya sabían por experiencia. Conoce su historia, sus bondades y cómo "
        "la producción ecológica potencia su poder curativo."
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# NUEVA SECCIÓN 1: Historia — Timeline / Acordeón
# ---------------------------------------------------------------------------

def render_historia():
    """Sección de historia con acordeón de épocas."""
    st.markdown(
        '<h2 class="section-title">Un Viaje a Través del Tiempo</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="centered-description">'
        "Desde las cavernas prehistóricas hasta los laboratorios modernos, "
        "las plantas medicinales han acompañado cada capítulo de la humanidad."
        "</div>",
        unsafe_allow_html=True,
    )

    epocas = [
        {
            "icono": "🪨",
            "titulo": "Prehistoria — Los Inicios Instintivos",
            "contenido": (
                "Los primeros humanos aprendieron a usar las plantas por instinto, observación y ensayo/error. "
                "Observaban a los animales enfermos buscar ciertas plantas para purgarse o curarse. "
                "El chamán era médico y líder espiritual: las plantas no solo curaban el cuerpo, sino que se usaban "
                "en rituales. Evidencia arqueológica —como el polen de milenrama y efedra en tumbas neandertales "
                "de hace 60,000 años— sugiere un uso intencionado."
            ),
        },
        {
            "icono": "🏛️",
            "titulo": "Grandes Civilizaciones — La Sistematización",
            "contenido": (
                "Con la escritura, el conocimiento oral fue registrado. Las tablillas sumerias (3000 a.C.) describen "
                "el uso de regaliz, adormidera y tomillo. El Papiro de Ebers egipcio (1550 a.C.) contiene más de 700 "
                "fórmulas. La Medicina Tradicional China atribuye sus orígenes al legendario Shennong. "
                "El Ayurveda indio sistematizó miles de remedios en textos sagrados como el Charaka Samhita, "
                "con pilares como la cúrcuma, la ashwagandha y el neem."
            ),
        },
        {
            "icono": "🏺",
            "titulo": "Antigüedad Clásica — La Base Occidental",
            "contenido": (
                "Hipócrates separó la medicina de la superstición y promovió remedios herbales simples. "
                "Teofrasto, el 'Padre de la Botánica', clasificó las plantas sistemáticamente. "
                "Dioscórides escribió De Materia Medica: más de 600 plantas con descripción, recolección y usos "
                "terapéuticos —texto de referencia estándar durante 1,500 años. Galeno creó complejos sistemas "
                "de farmacia con mezclas de hierbas, conocidas como 'galénicos'."
            ),
        },
        {
            "icono": "⛪",
            "titulo": "Edad Media — Preservación en los Monasterios",
            "contenido": (
                "Tras la caída del Imperio Romano, los monjes preservaron y copiaron los textos de Dioscórides "
                "y Galeno, cultivando 'jardines de simples' (hortus medicus). "
                "En el mundo islámico, Avicena (Ibn Sina) no solo tradujo las obras griegas sino que las expandió "
                "con saberes de India y Persia. Su Canon de la Medicina fue enciclopedia fundamental "
                "en ambas civilizaciones."
            ),
        },
        {
            "icono": "⛵",
            "titulo": "Renacimiento y Exploración — Nuevos Mundos",
            "contenido": (
                "La imprenta difundió los herbarios ilustrados masivamente. Paracelso desafió las ideas galénicas "
                "introduciendo la química y el concepto de 'principio activo', popularizando 'la dosis hace al veneno'. "
                "La llegada de europeos a América supuso una revolución farmacológica: la corteza de quina "
                "(con quinina) para la malaria, la coca como anestésico y estimulante, entre muchas otras."
            ),
        },
        {
            "icono": "⚗️",
            "titulo": "Revolución Científica — El Aislamiento",
            "contenido": (
                "Los químicos comenzaron a aislar compuestos puros. En 1804 se extrajo la morfina del opio; "
                "en 1820 la quinina de la corteza de quina; en 1828 la salicina del sauce —que décadas después "
                "se convertiría en la Aspirina. También se descubrieron la digitalina (para afecciones cardíacas) "
                "y la atropina de la belladona. Nació la farmacología moderna."
            ),
        },
        {
            "icono": "🔬",
            "titulo": "Siglo XXI — El Resurgimiento Científico",
            "contenido": (
                "La fitoterapia vive un renacimiento impulsado por la búsqueda de tratamientos más naturales "
                "y la validación científica de usos tradicionales. Fármacos contra el cáncer como el Taxol "
                "(del tejo del Pacífico) y la vincristina (de la vinca de Madagascar) provienen de plantas. "
                "La OMS reconoce el valor de la medicina tradicional y promueve su estudio y uso seguro. "
                "La biodiversidad sigue siendo fuente inagotable para nuevos medicamentos."
            ),
        },
    ]

    # Construir items HTML
    items_html = ""
    for epoca in epocas:
        items_html += f"""
        <div class="ac-item">
            <button class="ac-btn" onclick="toggle(this)">
                <span class="ac-icono">{epoca['icono']}</span>
                <span class="ac-titulo">{epoca['titulo']}</span>
                <span class="ac-flecha">&#9660;</span>
            </button>
            <div class="ac-body">
                <p>{epoca['contenido']}</p>
            </div>
        </div>"""

    componente_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .ac-wrapper { display: flex; flex-direction: column; gap: 0.6rem; }
  .ac-item {
    border: 1px solid rgba(107,142,35,0.35);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(22,27,34,0.85);
    transition: border-color 0.3s;
  }
  .ac-item:hover { border-color: rgba(200,169,81,0.5); }
  .ac-btn {
    width: 100%;
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 1rem 1.4rem;
    background: transparent;
    border: none;
    cursor: pointer;
    text-align: left;
    transition: background 0.25s;
  }
  .ac-btn:hover { background: rgba(107,142,35,0.08); }
  .ac-btn.active {
    background: rgba(107,142,35,0.13);
    border-bottom: 1px solid rgba(107,142,35,0.3);
  }
  .ac-icono { font-size: 1.4rem; flex-shrink: 0; line-height: 1; }
  .ac-titulo {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 1.05rem;
    color: #E8E4DC;
    flex: 1;
    line-height: 1.4;
  }
  .ac-btn.active .ac-titulo { color: #C8A951; }
  .ac-flecha {
    font-size: 0.8rem;
    color: #6B8E23;
    flex-shrink: 0;
    transition: transform 0.35s ease;
  }
  .ac-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, padding 0.3s ease;
    padding: 0 1.4rem;
  }
  .ac-body p {
    color: #d1d5db;
    font-size: 0.97rem;
    line-height: 1.78;
    padding: 1.1rem 0;
  }
</style>
</head>
<body>
  <div class="ac-wrapper">
""" + items_html + """
  </div>
  <script>
    function toggle(btn) {
      var body = btn.nextElementSibling;
      var flecha = btn.querySelector('.ac-flecha');
      var isOpen = btn.classList.contains('active');
      // cerrar todos
      document.querySelectorAll('.ac-btn').forEach(function(b) {
        b.classList.remove('active');
        b.querySelector('.ac-flecha').style.transform = 'rotate(0deg)';
        b.nextElementSibling.style.maxHeight = null;
      });
      // abrir si estaba cerrado
      if (!isOpen) {
        btn.classList.add('active');
        flecha.style.transform = 'rotate(180deg)';
        body.style.maxHeight = body.scrollHeight + 60 + 'px';
      }
    }
  </script>
</body>
</html>"""

    import streamlit.components.v1 as components
    components.html(componente_html, height=530, scrolling=False)


# ---------------------------------------------------------------------------
# NUEVA SECCIÓN 2: Las 10 Hierbas — Cards
# ---------------------------------------------------------------------------

def render_hierbas():
    """Sección con las 10 hierbas medicinales más importantes en cards."""
    st.markdown(
        '<h2 class="section-title">Las 10 Plantas que Cambiaron la Historia</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="centered-description">'
        "Estas plantas son el testimonio vivo de la sabiduría ancestral. "
        "Su eficacia ha sido tan notable a lo largo de la historia que la ciencia moderna "
        "no ha hecho más que confirmar lo que nuestros antepasados ya sabían."
        "</div>",
        unsafe_allow_html=True,
    )

    hierbas = [
        {
            "emoji": "🧄",
            "nombre": "Ajo",
            "nombre_cientifico": "Allium sativum",
            "ancestral": "Los egipcios lo daban a los constructores de las pirámides para aumentar su fuerza. Hipócrates lo recetaba para infecciones y problemas digestivos. Los romanos se lo daban a sus soldados antes de la batalla.",
            "actual": "Su compuesto activo, la alicina, posee propiedades antibacterianas, antivirales y antifúngicas. Ampliamente usado para la salud cardiovascular: reduce la presión arterial y el colesterol.",
        },
        {
            "emoji": "🌼",
            "nombre": "Manzanilla",
            "nombre_cientifico": "Matricaria recutita",
            "ancestral": "Los egipcios la dedicaron al sol y la usaron para tratar la fiebre. Griegos y romanos la utilizaban como antiinflamatorio y calmante. En la Edad Media era el remedio casero imprescindible para el insomnio.",
            "actual": "Una de las infusiones más populares del mundo. Sus flavonoides y aceites esenciales tienen propiedades calmantes, sedantes y antiespasmódicas para aliviar cólicos y problemas digestivos.",
        },
        {
            "emoji": "🌿",
            "nombre": "Menta",
            "nombre_cientifico": "Mentha piperita",
            "ancestral": "Se han encontrado hojas secas de menta en pirámides egipcias. Griegos y romanos la usaban para aliviar dolores de estómago y como tónico general.",
            "actual": "Su principal componente, el mentol, es muy eficaz para el síndrome del intestino irritable (SII), náuseas e indigestión. Aplicado tópicamente, alivia los dolores de cabeza tensionales.",
        },
        {
            "emoji": "🫚",
            "nombre": "Jengibre",
            "nombre_cientifico": "Zingiber officinale",
            "ancestral": "Piedra angular de la Medicina Tradicional China y el Ayurveda desde hace más de 5,000 años. Se utilizaba para problemas digestivos, náuseas, resfriados y artritis.",
            "actual": "Su eficacia contra náuseas y vómitos —incluidos los del embarazo y la quimioterapia— está científicamente probada. Sus gingeroles le confieren potentes efectos antiinflamatorios y antioxidantes.",
        },
        {
            "emoji": "🟡",
            "nombre": "Cúrcuma",
            "nombre_cientifico": "Curcuma longa",
            "ancestral": "La 'especia dorada' de la India, usada durante milenios en el Ayurveda como purificador de la sangre, antiinflamatorio y para problemas de piel y digestivos.",
            "actual": "Su curcumina es un potentísimo agente antiinflamatorio. Se investiga activamente por su potencial en la prevención del cáncer, enfermedades neurodegenerativas como el Alzheimer y la artritis.",
        },
        {
            "emoji": "🌳",
            "nombre": "Corteza de Sauce",
            "nombre_cientifico": "Salix spp.",
            "ancestral": "El 'analgésico' original de la naturaleza. Usado por sumerios, egipcios y griegos para aliviar el dolor y reducir la fiebre. Hipócrates recomendaba masticarla para el dolor del parto.",
            "actual": "La historia de esta planta es la historia de la Aspirina. Su principio activo, la salicina, fue aislado en el siglo XIX y luego sintetizado como ácido acetilsalicílico por Bayer en 1897.",
        },
        {
            "emoji": "🪴",
            "nombre": "Aloe Vera",
            "nombre_cientifico": "Aloe barbadensis",
            "ancestral": "Conocida como la 'planta de la inmortalidad' por los egipcios. Usada para curar heridas y quemaduras. Los griegos la usaban para sanar heridas de guerra.",
            "actual": "Su gel es extremadamente eficaz para calmar quemaduras solares, cortes y rozaduras, gracias a sus propiedades cicatrizantes, hidratantes y antiinflamatorias universalmente reconocidas.",
        },
        {
            "emoji": "😴",
            "nombre": "Valeriana",
            "nombre_cientifico": "Valeriana officinalis",
            "ancestral": "Hipócrates y Galeno la recetaban para el insomnio. Durante la Edad Media se le conocía como 'la cura-todo': ansiedad, temblores y dolores de cabeza.",
            "actual": "Uno de los suplementos herbales más populares para el sueño y la ansiedad. Sus compuestos actúan sobre los receptores GABA del cerebro, clave en la regulación del sueño y la calma nerviosa.",
        },
        {
            "emoji": "💜",
            "nombre": "Equinácea",
            "nombre_cientifico": "Echinacea purpurea",
            "ancestral": "La planta medicinal más importante para los nativos americanos de las Grandes Llanuras. Usada para el resfriado común, el dolor de muelas, mordeduras de serpiente y heridas infectadas.",
            "actual": "Famosa por estimular el sistema inmunológico. Ampliamente utilizada para prevenir y acortar el resfriado y la gripe. La ciencia ha validado su capacidad para aumentar la producción de glóbulos blancos.",
        },
        {
            "emoji": "🫚",
            "nombre": "Ginseng",
            "nombre_cientifico": "Panax ginseng",
            "ancestral": "La raíz más venerada en la Medicina Tradicional China desde hace milenios, reservada para los emperadores. Considerado un adaptógeno que ayuda al cuerpo a adaptarse al estrés.",
            "actual": "Sus ginsenósidos son investigados por sus efectos neuroprotectores, antiinflamatorios y de mejora del rendimiento físico y mental. Sigue siendo uno de los suplementos más populares.",
        },
    ]

    # Construir grid HTML puro con altura uniforme por fila
    cards_html = ""
    for h in hierbas:
        cards_html += f"""
        <div class="h-card">
            <div class="h-header">
                <span class="h-emoji">{h['emoji']}</span>
                <div>
                    <div class="h-nombre">{h['nombre']}</div>
                    <div class="h-cientifico">{h['nombre_cientifico']}</div>
                </div>
            </div>
            <div class="h-body">
                <div class="h-bloque">
                    <span class="h-label ancestral">🏺 Uso Ancestral</span>
                    <p>{h['ancestral']}</p>
                </div>
                <div class="h-bloque">
                    <span class="h-label actual">🔬 Uso Actual</span>
                    <p>{h['actual']}</p>
                </div>
            </div>
        </div>"""

    hierbas_html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.2rem;
    align-items: stretch;
  }
  .h-card {
    background: #161B22;
    border: 1px solid rgba(107,142,35,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: border-color 0.3s, box-shadow 0.3s;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  }
  .h-card:hover {
    border-color: rgba(200,169,81,0.5);
    box-shadow: 0 12px 32px rgba(0,0,0,0.45);
    transform: translateY(-3px);
  }
  .h-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.1rem;
    border-bottom: 1px solid rgba(107,142,35,0.2);
    padding-bottom: 0.9rem;
  }
  .h-emoji { font-size: 2.1rem; line-height: 1; flex-shrink: 0; }
  .h-nombre {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #C8A951;
  }
  .h-cientifico { font-size: 0.83rem; color: #6b7280; font-style: italic; margin-top: 0.1rem; }
  .h-body { display: flex; flex-direction: column; gap: 0.9rem; flex: 1; }
  .h-bloque p { color: #d1d5db; font-size: 0.91rem; line-height: 1.65; margin: 0.35rem 0 0 0; }
  .h-label {
    display: inline-block;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 0.22rem 0.6rem;
    border-radius: 20px;
  }
  .h-label.ancestral {
    background: rgba(107,142,35,0.2);
    color: #86a848;
    border: 1px solid rgba(107,142,35,0.3);
  }
  .h-label.actual {
    background: rgba(200,169,81,0.15);
    color: #C8A951;
    border: 1px solid rgba(200,169,81,0.3);
  }
</style></head><body>
<div class="grid">""" + cards_html + """
</div></body></html>"""

    import streamlit.components.v1 as components
    components.html(hierbas_html, height=1950, scrolling=False)


# ---------------------------------------------------------------------------
# NUEVA SECCIÓN: Frutas y Semillas Ancestrales — Cards
# ---------------------------------------------------------------------------

def render_frutas_semillas():
    """Sección con las 10 frutas y semillas ancestrales más saludables."""
    st.markdown(
        '<h2 class="section-title">Frutas y Semillas que Sanan</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="centered-description">'
        "Mas alla de las hierbas, nuestros ancestros encontraron en frutas y semillas "
        "una poderosa farmacia natural. Diez tesoros que el tiempo ha validado."
        "</div>",
        unsafe_allow_html=True,
    )

    frutas = [
        {
            "emoji": "🍫",
            "nombre": "Cacao",
            "cientifico": "Theobroma cacao",
            "origen": "Mesoamerica - Mayas y Aztecas",
            "tratamiento": "Energizante, antidepresivo natural y afrodisiaco. Usado en ceremonias sagradas para la conexion espiritual y para combatir la fatiga.",
            "preparacion": "Semillas fermentadas, secadas y tostadas. Se molian para crear xocolatl: una bebida amarga con chile y vainilla, sin azucar.",
        },
        {
            "emoji": "🤍",
            "nombre": "Semillas de Chia",
            "cientifico": "Salvia hispanica",
            "origen": "Mexico y Guatemala - Aztecas y Mayas",
            "tratamiento": "Resistencia y energia para guerreros. Regulaba la digestion, aportaba hidratacion y actuaba como antiinflamatorio.",
            "preparacion": "Mezcladas con agua formaban un gel bebible (iskiate), o molidas como harina para tortillas y tamales.",
        },
        {
            "emoji": "🌾",
            "nombre": "Quinoa",
            "cientifico": "Chenopodium quinoa",
            "origen": "Andes - Imperio Inca y culturas preincaicas",
            "tratamiento": "La madre de todos los granos. Fortalecia el cuerpo, aceleraba la recuperacion y se aplicaba topicamente para reducir inflamacion y curar heridas.",
            "preparacion": "Se lavaban para eliminar saponinas y se cocian como arroz. Para uso topico, cataplasma de semillas molidas o hojas.",
        },
        {
            "emoji": "🍒",
            "nombre": "Bayas de Goji",
            "cientifico": "Lycium barbarum",
            "origen": "China, Tibet y Mongolia - Medicina Tradicional China",
            "tratamiento": "Tonico de longevidad. Mejoraba la vista, fortalecia higado y rinones, nutria la sangre y potenciaba el sistema inmunologico.",
            "preparacion": "Se consumian secas como pasas, en sopas, tes e infusiones, o maceradas para vino medicinal.",
        },
        {
            "emoji": "🫑",
            "nombre": "Amla (Grosella India)",
            "cientifico": "Phyllanthus emblica",
            "origen": "India y Sudeste Asiatico - Medicina Ayurvedica",
            "tratamiento": "Potente rejuvenecedor. Trataba problemas digestivos, fortalecia cabello y piel, mejoraba la vista y reforzaba el sistema inmune.",
            "preparacion": "Fresca, en jugo, encurtida o en polvo mezclado con agua o miel. En pasta para aplicar en cabello y piel.",
        },
        {
            "emoji": "🫒",
            "nombre": "Oliva",
            "cientifico": "Olea europaea",
            "origen": "Region Mediterranea - Grecia, Roma, Egipto",
            "tratamiento": "Sagrada en el Mediterraneo. Trataba heridas, quemaduras y sequedad de piel, aliviaba dolores articulares y favorecia la salud cardiovascular.",
            "preparacion": "Olivas curadas por inmersion. Aceite extraido por prensado en frio para ingesta y uso topico en masajes y heridas.",
        },
        {
            "emoji": "🍎",
            "nombre": "Granada",
            "cientifico": "Punica granatum",
            "origen": "Iran y Norte de India, difundida en el Mediterraneo",
            "tratamiento": "Eliminaba parasitos intestinales, trataba diarrea, reducia la fiebre y aliviaba inflamaciones de garganta.",
            "preparacion": "Arilos frescos o en jugo. Decoccion de corteza de raiz para parasitos. Gargaras con jugo para la garganta.",
        },
        {
            "emoji": "🌳",
            "nombre": "Fruto del Baobab",
            "cientifico": "Adansonia digitata",
            "origen": "Africa Subsahariana - Multiples culturas africanas",
            "tratamiento": "El Arbol de la Vida. Combatia la fiebre (la aspirina africana), la disenteria, el escorbuto y restauraba la fuerza y vitalidad.",
            "preparacion": "La pulpa seca en polvo se disolvia en agua o leche formando una bebida nutritiva, o se anadia a gachas.",
        },
        {
            "emoji": "🟫",
            "nombre": "Datiles",
            "cientifico": "Phoenix dactylifera",
            "origen": "Mesopotamia - Oriente Medio y Norte de Africa",
            "tratamiento": "Combatian la fatiga y aportaban energia rapida. Trataban el estrenimiento, aliviaban la tos y fortalecian el corazon.",
            "preparacion": "Frescos o secos. Jarabe de datiles hervidos en leche para la tos. Fuente de energia para viajeros del desierto.",
        },
        {
            "emoji": "🫐",
            "nombre": "Maqui",
            "cientifico": "Aristotelia chilensis",
            "origen": "Patagonia - Pueblo Mapuche (Chile y Argentina)",
            "tratamiento": "Potente antiinflamatorio. Trataba heridas, dolores de garganta, diarrea y servia como tonico energizante general.",
            "preparacion": "Bayas frescas o secas. Bebida fermentada llamada tecu. Hojas machacadas en cataplasma para heridas.",
        },
    ]

    # Construir cards HTML
    cards = ""
    for f in frutas:
        cards += (
            '<div class="fc">'
            '<div class="fc-head">'
            '<span class="fc-em">' + f["emoji"] + '</span>'
            '<div>'
            '<div class="fc-nom">' + f["nombre"] + '</div>'
            '<div class="fc-sci">' + f["cientifico"] + '</div>'
            '<div class="fc-ori">&#128205; ' + f["origen"] + '</div>'
            '</div>'
            '</div>'
            '<div class="fc-body">'
            '<div class="fc-bloque">'
            '<span class="fc-tag trat">&#127866; Tratamiento Ancestral</span>'
            '<p>' + f["tratamiento"] + '</p>'
            '</div>'
            '<div class="fc-bloque">'
            '<span class="fc-tag prep">&#127807; Preparacion</span>'
            '<p>' + f["preparacion"] + '</p>'
            '</div>'
            '</div>'
            '</div>'
        )

    CSS = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: transparent; font-family: 'Inter', sans-serif; }
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
  align-items: stretch;
}
.fc {
  background: #161B22;
  border: 1px solid rgba(200,169,81,0.22);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  transition: border-color 0.3s, box-shadow 0.3s, transform 0.3s;
}
.fc:hover {
  border-color: rgba(200,169,81,0.6);
  box-shadow: 0 12px 32px rgba(0,0,0,0.45);
  transform: translateY(-3px);
}
.fc-head {
  display: flex;
  align-items: flex-start;
  gap: 0.9rem;
  padding-bottom: 0.9rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(200,169,81,0.15);
}
.fc-em { font-size: 2rem; line-height: 1; flex-shrink: 0; margin-top: 0.1rem; }
.fc-nom {
  font-family: 'Playfair Display', serif;
  font-size: 1.18rem;
  font-weight: 700;
  color: #C8A951;
}
.fc-sci { font-size: 0.8rem; color: #6b7280; font-style: italic; margin-top: 0.1rem; }
.fc-ori { font-size: 0.76rem; color: #6B8E23; font-weight: 600; margin-top: 0.28rem; }
.fc-body { display: flex; flex-direction: column; gap: 0.85rem; flex: 1; }
.fc-bloque p { color: #d1d5db; font-size: 0.9rem; line-height: 1.65; margin-top: 0.3rem; }
.fc-tag {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 0.18rem 0.55rem;
  border-radius: 20px;
}
.trat { background: rgba(200,169,81,0.13); color: #C8A951; border: 1px solid rgba(200,169,81,0.3); }
.prep { background: rgba(107,142,35,0.13); color: #86a848; border: 1px solid rgba(107,142,35,0.3); }
</style>
</head>
<body>
<div class="grid">
"""

    HTML_CLOSE = """
</div>
</body>
</html>"""

    import streamlit.components.v1 as components
    components.html(CSS + cards + HTML_CLOSE, height=1850, scrolling=False)


# ---------------------------------------------------------------------------
# NUEVA SECCIÓN 3: Relación con lo Ecológico
# ---------------------------------------------------------------------------

def render_ecologico():
    """Sección sobre la relación entre hierbas medicinales y producción ecológica."""
    st.markdown(
        '<h2 class="section-title">¿Por Qué Ecológico?</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="centered-description">'
        "La potencia, pureza y seguridad de una hierba medicinal dependen directamente "
        "de la salud del ecosistema en el que crece."
        "</div>",
        unsafe_allow_html=True,
    )

    pilares = [
        {
            "icono": "🌱",
            "titulo": "Pureza Garantizada",
            "texto": (
                "Una planta cultivada convencionalmente puede absorber pesticidas, "
                "herbicidas y metales pesados. El cultivo ecológico garantiza una "
                "hierba libre de residuos tóxicos, esencial cuando se consume de forma "
                "concentrada en extractos o tinturas."
            ),
        },
        {
            "icono": "💪",
            "titulo": "Mayor Potencia Medicinal",
            "texto": (
                "Un suelo vivo, rico en microorganismos y materia orgánica, nutre a la planta "
                "de una manera que los fertilizantes sintéticos no pueden replicar. "
                "Plantas cultivadas ecológicamente producen mayor cantidad de metabolitos "
                "secundarios —los mismos que les confieren valor medicinal."
            ),
        },
        {
            "icono": "🌍",
            "titulo": "Sistema Agroecológico",
            "texto": (
                "La agroecología va más allá: diseña sistemas que imitan la inteligencia "
                "de los ecosistemas naturales. Policultivos, biodiversidad, ciclos cerrados "
                "y conocimiento local se combinan para crear una producción verdaderamente "
                "sostenible que regenera el suelo y protege los recursos hídricos."
            ),
        },
    ]

    pilares_html = ""
    for p in pilares:
        pilares_html += f"""
        <div class="ep-card">
            <div class="ep-icono">{p['icono']}</div>
            <div class="ep-titulo">{p['titulo']}</div>
            <p class="ep-texto">{p['texto']}</p>
        </div>"""

    eco_cards_html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Inter', sans-serif; }
  .ep-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 1.2rem;
    align-items: stretch;
  }
  .ep-card {
    background: #161B22;
    border: 1px solid rgba(107,142,35,0.25);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: border-color 0.3s, transform 0.3s;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  }
  .ep-card:hover {
    border-color: rgba(200,169,81,0.5);
    transform: translateY(-4px);
  }
  .ep-icono { font-size: 3rem; margin-bottom: 1rem; line-height: 1; }
  .ep-titulo {
    font-family: 'Playfair Display', serif;
    font-size: 1.18rem;
    font-weight: 700;
    color: #C8A951;
    margin-bottom: 0.75rem;
    text-align: center;
  }
  .ep-texto {
    color: #9ca3af;
    font-size: 0.91rem;
    line-height: 1.65;
    text-align: center;
    flex: 1;
  }
</style></head><body>
<div class="ep-grid">""" + pilares_html + """
</div></body></html>"""

    import streamlit.components.v1 as components
    components.html(eco_cards_html, height=380, scrolling=False)

    # Tabla comparativa
    st.markdown(
        '<h3 class="section-subtitle">Comparativa de Modelos de Cultivo</h3>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="tabla-wrapper">
            <table class="tabla-comparativa">
                <thead>
                    <tr>
                        <th>Característica</th>
                        <th>⚠️ Convencional</th>
                        <th>✅ Ecológico</th>
                        <th>🌟 Agroecológico</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Fertilización</strong></td>
                        <td>Fertilizantes químicos sintéticos</td>
                        <td>Compost, estiércol, abonos verdes</td>
                        <td>Ciclos de nutrientes en la propia finca</td>
                    </tr>
                    <tr>
                        <td><strong>Control de Plagas</strong></td>
                        <td>Pesticidas y herbicidas sintéticos</td>
                        <td>Métodos biológicos y preventivos</td>
                        <td>Diseño del ecosistema como defensa</td>
                    </tr>
                    <tr>
                        <td><strong>Biodiversidad</strong></td>
                        <td>Monocultivo</td>
                        <td>Rotación de cultivos</td>
                        <td>Policultivo — pilar del sistema</td>
                    </tr>
                    <tr>
                        <td><strong>Visión del Suelo</strong></td>
                        <td>Soporte inerte</td>
                        <td>Recurso a proteger</td>
                        <td>Organismo vivo, corazón del sistema</td>
                    </tr>
                    <tr>
                        <td><strong>Resultado</strong></td>
                        <td class="resultado-malo">Posibles residuos tóxicos</td>
                        <td class="resultado-bueno">Hierbas puras y seguras</td>
                        <td class="resultado-excelente">Hierbas potentes, puras y regenerativas</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Secciones originales
# ---------------------------------------------------------------------------

def render_grid_gallery():
    """Galería de imágenes grid con estilo premium."""
    st.markdown(
        '<h2 class="section-title">La Botica Natural</h2>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="centered-description">'
        "Desde la antigua botica herbal hasta los huertos ecológicos modernos: "
        "la belleza de cultivar y preservar las plantas que sanan."
        "</div>",
        unsafe_allow_html=True,
    )

    grid_images = [
        ("grid-1.jpg", "La Botica Ancestral — frascos, velas y sabiduría milenaria"),
        ("grid-2.jpg", "Cosecha Ecológica — manos que cuidan la tierra"),
        ("grid-3.jpg", "Productos Artesanales — aceites, tinturas y sachets naturales"),
    ]

    cols = st.columns(3, gap="large")
    for col, (img_name, caption) in zip(cols, grid_images):
        with col:
            b64 = img_to_base64(IMG_DIR / img_name)
            st.markdown(
                f"""
                <div class="grid-img-wrapper">
                    <img src="data:image/jpeg;base64,{b64}" alt="{caption}" />
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(caption)


def render_breath():
    """Sección visual de cierre con imagen breath-bg."""
    b64 = img_to_base64(IMG_DIR / "breath-bg.jpg")
    st.markdown(
        f"""
        <div class="breath-section">
            <img src="data:image/jpeg;base64,{b64}" alt="Jardín de hierbas" />
            <div class="breath-overlay">
                <h2>🌿 Naturaleza, Ciencia y Tradición</h2>
                <p>
                    Buscar hierbas medicinales de origen ecológico no es una simple moda.
                    Es la forma más coherente y responsable de aprovechar el poder curativo
                    de la naturaleza, asegurando que tanto nuestra salud como la del
                    planeta prosperen juntas.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        '<p class="footer-text">'
        "© 2026 Hierbas Medicinales · Sabiduría ancestral · Ciencia moderna · Producción ecológica<br>"
        '<span style="font-size:.78rem;color:#4b5563;">Construido con ❤️ por Jorge Omar del Rio · WhatsApp 54 9 1144353202</span>'
        "</p>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Botón exportar a PDF
# ---------------------------------------------------------------------------

def render_pdf_button():
    """Botón fijo en esquina superior derecha para exportar la página a PDF.
    Usa components.html() para que el <script> y position:fixed funcionen
    correctamente fuera del shadow DOM de Streamlit."""

    import streamlit.components.v1 as components

    # SVG del ícono PDF
    pdf_icon_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="24" height="24"><rect width="64" height="64" rx="8" fill="#fff"/><text x="50%" y="56%" dominant-baseline="middle" text-anchor="middle" font-family="Arial Black,sans-serif" font-size="22" font-weight="900" fill="#E53935">PDF</text></svg>"""
    pdf_icon_b64 = base64.b64encode(pdf_icon_svg.encode()).decode()

    btn_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; overflow: hidden; }}

  /* ── Botón PDF ── */
  #pdf-btn {{
    position: fixed;
    top: 14px;
    right: 18px;
    z-index: 99999;
    display: flex;
    align-items: center;
    gap: 7px;
    background: linear-gradient(135deg, #c0392b, #e74c3c);
    color: #fff;
    border: none;
    border-radius: 50px;
    padding: 8px 18px 8px 12px;
    font-family: 'Inter', Arial, sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.04em;
    cursor: pointer;
    box-shadow: 0 4px 18px rgba(231,76,60,0.5);
    transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
    user-select: none;
  }}
  #pdf-btn:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(231,76,60,0.6); }}
  #pdf-btn:active {{ transform: scale(0.97); }}
  #pdf-btn img {{ width: 24px; height: 24px; border-radius: 4px; flex-shrink: 0; }}

  /* ── Overlay de progreso ── */
  #pdf-overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(14,17,23,0.88);
    z-index: 999998;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1.4rem;
  }}
  #pdf-overlay.visible {{ display: flex; }}
  #pdf-overlay-title {{
    font-family: 'Georgia', serif;
    font-size: 1.3rem;
    color: #E8E4DC;
    letter-spacing: 0.03em;
  }}
  #pdf-overlay-sub {{
    font-family: Arial, sans-serif;
    font-size: 0.88rem;
    color: #9ca3af;
  }}
  #pdf-progress-track {{
    width: 320px;
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 99px;
    overflow: hidden;
  }}
  #pdf-progress-bar {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #6B8E23, #C8A951);
    border-radius: 99px;
    transition: width 0.25s ease;
  }}

  @media print {{
    #pdf-btn, #pdf-overlay {{ display: none !important; }}
  }}
</style>
</head>
<body>

  <button id="pdf-btn" onclick="iniciarExportacion()" title="Exportar página a PDF">
    <img src="data:image/svg+xml;base64,{pdf_icon_b64}" alt="PDF" />
    Exportar a PDF
  </button>

  <div id="pdf-overlay">
    <div id="pdf-overlay-title">🌿 Preparando exportación...</div>
    <div id="pdf-progress-track">
      <div id="pdf-progress-bar"></div>
    </div>
    <div id="pdf-overlay-sub" id="pdf-step-label">Iniciando...</div>
  </div>

  <script>
    function setProgreso(pct, texto) {{
      document.getElementById('pdf-progress-bar').style.width = pct + '%';
      document.getElementById('pdf-overlay-sub').textContent = texto;
    }}

    function iniciarExportacion() {{
      var overlay = document.getElementById('pdf-overlay');
      overlay.classList.add('visible');
      setProgreso(0, 'Iniciando...');

      // Comunicar al documento padre (Streamlit) para hacer scroll al top
      window.parent.scrollTo({{ top: 0, behavior: 'smooth' }});

      setTimeout(function() {{ setProgreso(20, 'Cargando estilos de página...'); }}, 200);
      setTimeout(function() {{ setProgreso(45, 'Procesando imágenes...'); }}, 600);
      setTimeout(function() {{ setProgreso(70, 'Preparando secciones...'); }}, 1000);
      setTimeout(function() {{ setProgreso(90, 'Generando documento...'); }}, 1400);
      setTimeout(function() {{
        setProgreso(100, '¡Listo! Abriendo diálogo de impresión...');
      }}, 1800);
      setTimeout(function() {{
        overlay.classList.remove('visible');
        // Imprimir desde el frame padre (la página completa de Streamlit)
        window.parent.print();
      }}, 2200);
    }}
  </script>
</body>
</html>"""

    components.html(btn_html, height=70, scrolling=False)


# ---------------------------------------------------------------------------
# 🌿 MAIN — Composición de la página
# ---------------------------------------------------------------------------

def main():
    # 0. Botón PDF (fijo, visible en toda la página)
    render_pdf_button()

    # 1. Hero
    render_hero()

    # 2. Introducción
    render_intro()
    render_divider("&#10047;")

    # 3. Historia (NUEVO)
    render_historia()
    render_divider("&#9672;")

    # 4. Galería
    render_grid_gallery()
    render_divider("&#10047;")

    # 5. Las 10 Hierbas (NUEVO)
    render_hierbas()
    render_divider("&#9672;")

    # 6. Frutas y Semillas (NUEVO)
    render_frutas_semillas()
    render_divider("&#10047;")

    # 7. Relación Ecológica (NUEVO)
    render_ecologico()
    render_divider("&#10047;")

    # 8. Cierre visual
    render_breath()

    # 9. Footer
    render_footer()


if __name__ == "__main__":
    main()
