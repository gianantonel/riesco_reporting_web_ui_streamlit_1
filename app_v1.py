# app.py
import os
import glob
import uuid
import requests
import streamlit as st

# =========================
# CONFIG
# =========================
MODO_PRODUCCION = True  # <- cambialo a True para PROD

WEBHOOK_DEV = "https://n8n.optimizar-ia.com/webhook-test/reporte_riesco"
# Seteá N8N_WEBHOOK_PROD en tu entorno o reemplazá el placeholder.
WEBHOOK_PROD = "https://n8n.optimizar-ia.com/webhook/reporte_riesco"
TIMEOUT_S = int(os.getenv("TIMEOUT_S", "300"))  # 5 min por defecto

# =========================
# HELPERS
# =========================
def get_webhook_url() -> str:
    return WEBHOOK_PROD if MODO_PRODUCCION else WEBHOOK_DEV


def find_logo_path(folder: str = "logo") -> str | None:
    """
    Busca un logo en ./logo con extensiones png/jpg/jpeg.
    Devuelve el primer match (ordenado).
    """
    patterns = [os.path.join(folder, "*.png"),
                os.path.join(folder, "*.jpg"),
                os.path.join(folder, "*.jpeg")]
    matches = []
    for p in patterns:
        matches.extend(glob.glob(p))
    matches = sorted(matches)
    return matches[0] if matches else None


def post_to_n8n(report_name: str) -> dict:
    """
    Modo SYNC: hace POST al webhook y espera la respuesta final del workflow (Respond to Webhook).
    n8n debería responder JSON del estilo:
      { "status": "success"|"failed", "message": "...", ... }
    """
    request_id = str(uuid.uuid4())
    payload = {
        "request_id": request_id,
        "report_name": report_name,
        "modo_produccion": MODO_PRODUCCION,
    }

    r = requests.post(get_webhook_url(), json=payload, timeout=TIMEOUT_S)
    try:
        data = r.json()
    except Exception:
        data = {"status": "unknown", "message": "Respuesta no-JSON desde n8n", "raw_text": r.text}

    # Adjuntamos info útil
    data.setdefault("request_id", request_id)
    data.setdefault("http_status", r.status_code)
    return data


# =========================
# UI
# =========================
st.set_page_config(page_title="Optimizar-IA | Reportes", layout="wide")

# CSS: centra el bloque y estiliza botones (alargados, bordes redondeados)
st.markdown(
    """
    <style>
      .center-block {
        max-width: 760px;
        margin: 0 auto;
      }
      .center-block div.stButton > button {
        width: 100%;
        border-radius: 16px;
        padding: 0.95rem 1.1rem;
        font-size: 1.05rem;
        font-weight: 650;
      }
      .btn-gap { margin-top: 12px; }
      h1 { margin-bottom: 0.25rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header: logo izquierda + texto
c1, c2 = st.columns([1, 8], vertical_alignment="center")

with c1:
    logo_path = find_logo_path("logo")
    if logo_path:
        st.image(logo_path, width=95)
    else:
        st.markdown("🧾")  # placeholder si no hay logo

with c2:
    st.title("Bienvenido Gabi a tu Web para Generación automatizada de reportes by Optimizar-IA.")
    st.write("Hacé click en un botón para comenzar el proceso de generación automática del reporte correspondiente.")

st.divider()

# Botones centrados
REPORTS = [
    "Generar reporte de DD.JJ. de IVA",
    "Generar reporte de DD.JJ. de Ingresos Brutos",
    "Generar reporte de Pagos a Profesionales",
    "Generar reporte de VEP de Sueldos",
]

if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.markdown('<div class="center-block">', unsafe_allow_html=True)

for i, label in enumerate(REPORTS):
    st.markdown('<div class="btn-gap">', unsafe_allow_html=True)
    clicked = st.button(label, key=f"btn_{i}")
    st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        with st.spinner("Ejecutando proceso"):
            try:
                result = post_to_n8n(label)
            except requests.RequestException as e:
                result = {"status": "failed", "message": f"Error enviando POST a n8n: {e}"}
            except Exception as e:
                result = {"status": "failed", "message": f"Error inesperado: {e}"}

        st.session_state.last_result = result

st.markdown("</div>", unsafe_allow_html=True)

# Mostrar resultado
res = st.session_state.last_result
if res:
    status = (res.get("status") or "").lower()
    msg = res.get("message") or "—"

    if status in {"success", "ok", "exitoso", "exito"}:
        st.success(f"✅ Proceso finalizó exitosamente. {msg}")
    elif status in {"failed", "fail", "error", "fallo"}:
        st.error(f"❌ Proceso falló. {msg}")
    else:
        st.info(f"ℹ️ Estado: {res.get('status','unknown')} | {msg}")

    with st.expander("Ver detalle"):
        st.json(res)

with st.expander("Debug"):
    st.write(
        {
            "MODO_PRODUCCION": MODO_PRODUCCION,
            "WEBHOOK_USADO": get_webhook_url(),
            "TIMEOUT_S": TIMEOUT_S,
            "LOGO_ENCONTRADO": bool(find_logo_path("logo")),
        }
    )
