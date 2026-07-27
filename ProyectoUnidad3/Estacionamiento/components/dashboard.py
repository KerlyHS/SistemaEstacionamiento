import json
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"
CSS_DIR = BASE_DIR / "static" / "css"
JS_DIR = BASE_DIR / "static" / "js"

HEADER_CAR_ICON = """<svg viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="8" width="18" height="9" rx="3"/>
  <rect x="6" y="10" width="12" height="5" rx="2" fill="rgba(0,0,0,0.15)"/>
  <circle cx="6" cy="17" r="2" fill="rgba(255,255,255,0.4)"/>
  <circle cx="18" cy="17" r="2" fill="rgba(255,255,255,0.4)"/>
  <circle cx="6" cy="8" r="2" fill="rgba(255,255,255,0.4)"/>
  <circle cx="18" cy="8" r="2" fill="rgba(255,255,255,0.4)"/>
</svg>"""

CAR_ICON_SMALL = """<svg viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="8" width="18" height="8" rx="3"/>
  <rect x="6" y="10" width="12" height="4" rx="1.5" fill="rgba(0,0,0,0.15)"/>
  <circle cx="6" cy="8" r="1.5"/>
  <circle cx="18" cy="8" r="1.5"/>
  <circle cx="6" cy="16" r="1.5"/>
  <circle cx="18" cy="16" r="1.5"/>
</svg>"""

CLOCK_ICON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</svg>"""

WIFI_ON = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg>"""

WIFI_OFF = """<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/></svg>"""

CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
CLOSE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>'


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _inline_svg(name):
    p = ASSETS / name
    raw = _read_text(p)
    if raw:
        raw = raw.strip()
        if raw.startswith("<svg"):
            return raw
    return ""


CAR_SVG = _inline_svg("car.svg")
LOGO_SVG = _inline_svg("logo.svg")


def _build_html(plaza1, plaza2, libres, ocupadas, conectado, hora):
    p1_is_free = plaza1 == "LIBRE"
    p1_is_occ = plaza1 == "OCUPADA"
    p1_has_data = p1_is_free or p1_is_occ
    p1_cls = "free" if p1_is_free else ("occupied" if p1_is_occ else "")
    p1_disp_spinner = "none" if p1_has_data else ""
    p1_disp_content = "" if p1_has_data else "none"
    p1_text = plaza1 if p1_has_data else ""

    p2_is_free = plaza2 == "LIBRE"
    p2_is_occ = plaza2 == "OCUPADA"
    p2_has_data = p2_is_free or p2_is_occ
    p2_cls = "free" if p2_is_free else ("occupied" if p2_is_occ else "")
    p2_disp_spinner = "none" if p2_has_data else ""
    p2_disp_content = "" if p2_has_data else "none"
    p2_text = plaza2 if p2_has_data else ""

    conn_text = "CONECTADO" if conectado else "DESCONECTADO"
    conn_cls = "connected" if conectado else "disconnected"
    conn_icon = WIFI_ON if conectado else WIFI_OFF

    data = {
        "plaza1": plaza1,
        "plaza2": plaza2,
        "libres": libres,
        "ocupadas": ocupadas,
        "conexion": conn_text,
        "hora": hora,
    }
    data_json = json.dumps(data)
    css = _read_text(CSS_DIR / "style.css")
    js_code = _read_text(JS_DIR / "dashboard.js")

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard Estacionamiento</title>
<style>{css}</style>
</head>
<body>
<div class="dashboard">
  <header class="dashboard-header">
    <div class="header-left">
      <div class="header-car-icon">{HEADER_CAR_ICON}</div>
      <h1>DASHBOARD - ESTACIONAMIENTO</h1>
    </div>
    <div class="header-right">
      <div class="header-logo-icon">{LOGO_SVG}</div>
      <span>Ecol&oacute;gico Dirigido</span>
    </div>
  </header>

  <main class="dashboard-main">
    <section class="panel-resumen">
      <h2 class="panel-title">RESUMEN</h2>
      <div class="resumen-counters">
        <div class="resumen-counter">
          <div class="resumen-counter-circle green">{CAR_ICON_SMALL}</div>
          <div class="resumen-counter-info">
            <span class="resumen-counter-label">LIBRES</span>
            <span id="count-libres" class="resumen-counter-number green">{libres}</span>
          </div>
        </div>
        <div class="resumen-counter">
          <div class="resumen-counter-circle red">{CAR_ICON_SMALL}</div>
          <div class="resumen-counter-info">
            <span class="resumen-counter-label">OCUPADAS</span>
            <span id="count-ocupadas" class="resumen-counter-number red">{ocupadas}</span>
          </div>
        </div>
      </div>
      <div class="resumen-update">
        <div class="resumen-update-icon">{CLOCK_ICON}</div>
        <div class="resumen-update-info">
          <span class="resumen-update-label">&Uacute;LTIMA ACTUALIZACI&Oacute;N</span>
          <span id="clock-time" class="resumen-update-time">{hora}</span>
        </div>
      </div>
      <div id="conn-status" class="resumen-conexion {conn_cls}">
        <div class="conexion-icon">{conn_icon}</div>
        <span class="conexion-text">{conn_text}</span>
      </div>
    </section>

    <section class="panel-plaza">
      <div id="plaza1-header" class="plaza-header {p1_cls}">PLAZA 1</div>
      <div class="plaza-body">
        <div id="plaza1-spinner" class="plaza-spinner" style="display:{p1_disp_spinner}">
          <div class="spinner"></div>
          <p>Esperando datos desde la ESP32 Gateway...</p>
        </div>
        <div id="plaza1-content" class="plaza-content" style="display:{p1_disp_content}">
          <div class="parking-lot">
            <div class="parking-lines">
              <div class="parking-line"></div>
              <div class="parking-line"></div>
            </div>
            <div id="plaza1-car" class="plaza-car {p1_cls}">{CAR_SVG}</div>
          </div>
        </div>
      </div>
      <div id="plaza1-footer" class="plaza-footer {p1_cls}">
        <span class="plaza-footer-icon">{CHECK_SVG if p1_is_free else (CLOSE_SVG if p1_is_occ else '')}</span>
        <span id="plaza1-status" class="plaza-footer-text">{p1_text}</span>
      </div>
    </section>

    <section class="panel-plaza">
      <div id="plaza2-header" class="plaza-header {p2_cls}">PLAZA 2</div>
      <div class="plaza-body">
        <div id="plaza2-spinner" class="plaza-spinner" style="display:{p2_disp_spinner}">
          <div class="spinner"></div>
          <p>Esperando datos desde la ESP32 Gateway...</p>
        </div>
        <div id="plaza2-content" class="plaza-content" style="display:{p2_disp_content}">
          <div class="parking-lot">
            <div class="parking-lines">
              <div class="parking-line"></div>
              <div class="parking-line"></div>
            </div>
            <div id="plaza2-car" class="plaza-car {p2_cls}">{CAR_SVG}</div>
          </div>
        </div>
      </div>
      <div id="plaza2-footer" class="plaza-footer {p2_cls}">
        <span class="plaza-footer-icon">{CHECK_SVG if p2_is_free else (CLOSE_SVG if p2_is_occ else '')}</span>
        <span id="plaza2-status" class="plaza-footer-text">{p2_text}</span>
      </div>
    </section>
  </main>
</div>
<script id="dashboard-data" type="application/json">{data_json}</script>
<script>{js_code}</script>
</body>
</html>"""


def render(plaza1=None, plaza2=None, libres=0, ocupadas=0, conectado=False, hora="00:00:00"):
    html = _build_html(plaza1, plaza2, libres, ocupadas, conectado, hora)
    st.components.v1.html(html, height=680)
