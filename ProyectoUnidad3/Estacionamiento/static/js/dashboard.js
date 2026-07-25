(function () {
  'use strict';

  var dataEl = document.getElementById('dashboard-data');
  if (!dataEl) return;

  function readData() {
    try { return JSON.parse(dataEl.textContent); }
    catch (e) { return null; }
  }

  function setState(el, cls, add) {
    if (!el) return;
    if (add) el.classList.add(cls);
    else el.classList.remove(cls);
  }

  function show(el) {
    if (el) el.style.display = '';
  }

  function hide(el) {
    if (el) el.style.display = 'none';
  }

  var CHECK_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
  var CLOSE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
  var WIFI_ON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/><path d="M8.53 16.11a6 6 0 0 1 6.95 0"/><circle cx="12" cy="20" r="1"/></svg>';
  var WIFI_OFF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="1" y1="1" x2="23" y2="23"/><path d="M5 12.55a11 11 0 0 1 14.08 0"/><path d="M1.42 9a16 16 0 0 1 21.16 0"/></svg>';

  function updatePlaza(plazaId, estado) {
    var spinner = document.getElementById(plazaId + '-spinner');
    var content = document.getElementById(plazaId + '-content');
    var header = document.getElementById(plazaId + '-header');
    var car = document.getElementById(plazaId + '-car');
    var statusEl = document.getElementById(plazaId + '-status');
    var footer = document.getElementById(plazaId + '-footer');
    var footerIcon = footer ? footer.querySelector('.plaza-footer-icon') : null;

    var hasData = (estado === 'LIBRE' || estado === 'OCUPADA');

    if (hasData) {
      hide(spinner);
      show(content);

      var isFree = estado === 'LIBRE';
      setState(header, 'occupied', !isFree);
      setState(car, 'free', isFree);
      setState(car, 'occupied', !isFree);
      setState(statusEl, 'free', isFree);
      setState(statusEl, 'occupied', !isFree);
      if (statusEl) statusEl.textContent = estado;

      if (footer) {
        setState(footer, 'free', isFree);
        setState(footer, 'occupied', !isFree);
      }
      if (footerIcon) {
        footerIcon.innerHTML = isFree ? CHECK_SVG : CLOSE_SVG;
      }
    } else {
      show(spinner);
      hide(content);
      setState(header, 'occupied', false);
      if (statusEl) statusEl.textContent = '';
      if (footer) {
        setState(footer, 'free', false);
        setState(footer, 'occupied', false);
      }
      if (footerIcon) {
        footerIcon.innerHTML = '';
      }
    }
  }

  function updateSummary(libres, ocupadas) {
    var libresEl = document.getElementById('count-libres');
    var ocupadasEl = document.getElementById('count-ocupadas');
    if (libresEl) {
      libresEl.textContent = libres;
      setState(libresEl, 'green', true);
    }
    if (ocupadasEl) {
      ocupadasEl.textContent = ocupadas;
      setState(ocupadasEl, 'red', true);
    }
  }

  function updateConnection(conexion) {
    var el = document.getElementById('conn-status');
    if (!el) return;
    setState(el, 'connected', conexion === 'CONECTADO');
    setState(el, 'disconnected', conexion !== 'CONECTADO');

    var textEl = el.querySelector('.conexion-text');
    if (textEl) textEl.textContent = conexion;

    var iconEl = el.querySelector('.conexion-icon');
    if (iconEl) {
      iconEl.innerHTML = conexion === 'CONECTADO' ? WIFI_ON : WIFI_OFF;
    }
  }

  function render(data) {
    if (!data) return;
    updatePlaza('plaza1', data.plaza1);
    updatePlaza('plaza2', data.plaza2);
    updateSummary(data.libres, data.ocupadas);
    updateConnection(data.conexion);
  }

  function updateClock() {
    var now = new Date();
    var h = String(now.getHours()).padStart(2, '0');
    var m = String(now.getMinutes()).padStart(2, '0');
    var s = String(now.getSeconds()).padStart(2, '0');
    var el = document.getElementById('clock-time');
    if (el) el.textContent = h + ':' + m + ':' + s;
  }

  var data = readData();
  render(data);
  updateClock();
  setInterval(updateClock, 1000);

  dataEl.parentNode.removeChild(dataEl);
})();
