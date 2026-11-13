// Datos de demostración. En la integración final deben reemplazarse por respuestas de la API vía Jinja o formularios Flask.
const movies = [
  {id:1,title:'Órbita Perdida',genre:'Ciencia ficción',duration:128,rating:'+13',status:'En cartelera',tag:'ESTRENO',poster:'poster-red'},
  {id:2,title:'La Ciudad Sumergida',genre:'Thriller',duration:116,rating:'+16',status:'En cartelera',tag:'',poster:'poster-blue'},
  {id:3,title:'Cartas de Invierno',genre:'Drama',duration:109,rating:'ATP',status:'En cartelera',tag:'',poster:'poster-gold'},
  {id:4,title:'Ecos en la Oscuridad',genre:'Terror',duration:104,rating:'+18',status:'En cartelera',tag:'ESTRENO',poster:'poster-gray'},
  {id:5,title:'Código de Fuego',genre:'Acción',duration:122,rating:'+13',status:'En cartelera',tag:'',poster:'poster-purple'},
  {id:6,title:'El Secreto del Bosque',genre:'Animación',duration:98,rating:'ATP',status:'Próximamente',tag:'',poster:'poster-green'}
];

const snacks = [
  {id:'mega',name:'Combo Mega Pop',detail:'Pochoclos grandes + 2 bebidas',price:12900,emoji:'🍿'},
  {id:'pareja',name:'Combo Pareja',detail:'2 pochoclos + 2 gaseosas',price:18500,emoji:'🥤'},
  {id:'gaseosa',name:'Gaseosa grande',detail:'Bebida 750 ml',price:4900,emoji:'🥤'},
  {id:'mix',name:'Mix de golosinas',detail:'Selección de dulces',price:3500,emoji:'🍬'}
];

let tickets = [
  {id:'CP-48213',title:'Órbita Perdida',poster:'poster-red',status:'Activo',date:'Sáb, 18 abr 2026',time:'20:30 hs',room:'Sala 3 · 2D',seats:'C7, C8',total:14800},
  {id:'CP-48187',title:'Bajo la Misma Luna',poster:'poster-blue',status:'Activo',date:'Vie, 24 abr 2026',time:'22:15 hs',room:'Sala 2',seats:'D10',total:6200},
  {id:'CP-47009',title:'La Isla de los Sueños',poster:'poster-green',status:'Usado',date:'Dom, 12 abr 2026',time:'18:00 hs',room:'Sala 1',seats:'E5, E6',total:10500},
  {id:'CP-46331',title:'La Ciudad Sumergida',poster:'poster-purple',status:'Cancelado',date:'Lun, 06 abr 2026',time:'21:00 hs',room:'Sala 3',seats:'B4',total:6900}
];

let selectedSeats = JSON.parse(sessionStorage.getItem('cp_selected_seats') || '[]');
let quantities = Object.fromEntries(snacks.map(s => [s.id, 0]));
let currentTicketFilter = 'Todas';
let editingMovieId = null;

const money = n => '$' + Math.round(n).toLocaleString('es-AR');
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

function toast(message) {
  const el = $('#toast');
  if (!el) return;
  el.textContent = message;
  el.classList.add('show');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove('show'), 2600);
}

const loginBtn = $('#loginBtn');
if (loginBtn) {
  loginBtn.addEventListener('click', () => {
    const modal = $('#loginModal');
    if (modal) {
      modal.showModal();
    } else {
      toast('Inicio de sesión: conectar con el módulo de autenticación.');
    }
  });
}

// CARTELERA
function renderMovies() {
  const grid = $('#movieGrid');
  if (!grid) return;
  const visibles = movies.filter(m => m.status !== 'Inactiva');
  grid.innerHTML = visibles.map(m => `
    <article class="movie-card">
      <div class="poster ${m.poster}">
        ${m.tag ? `<span class="poster-tag">${m.tag}</span>` : ''}
        <span>${m.title.toUpperCase()}</span>
      </div>
      <div class="movie-card-body">
        <h3>${m.title}</h3>
        <div class="movie-meta">${m.genre} · ${m.rating} · ${Math.floor(m.duration / 60)} h ${m.duration % 60} min</div>
        <a class="button" href="/butacas" data-buy="${m.id}">COMPRAR</a>
      </div>
    </article>
  `).join('');

  $$('[data-buy]').forEach(b => b.addEventListener('click', () => {
    sessionStorage.setItem('cp_movie_id', b.dataset.buy);
    sessionStorage.removeItem('cp_selected_seats');
  }));

  updateMovieCount();
}

function updateMovieCount() {
  const countEl = $('#movieCount');
  if (!countEl) return;
  const visibles = movies.filter(m => m.status !== 'Inactiva');
  countEl.textContent = `${visibles.length} películas · ${$('#cinemaFilter').value} · ${$('#dateFilter').value}`;
}

if ($('#movieGrid')) {
  renderMovies();
  $('#cinemaFilter')?.addEventListener('change', updateMovieCount);
  $('#dateFilter')?.addEventListener('change', updateMovieCount);
}

// BUTACAS
// --- 2. BUTACAS (renderizadas desde Jinja) ---
const map = $('#seatMap');
if (map) {
  let seleccionadas = []; // [{ id: "613", label: "A1" }, ...]
  const precioUnitario = Number(map.dataset.precio || 6900);

  $$('#seatMap .seat:not(.occupied)').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.id;
      const label = btn.dataset.label;
      const existe = seleccionadas.some(s => s.id === id);

      if (existe) {
        seleccionadas = seleccionadas.filter(s => s.id !== id);
        btn.classList.remove('selected');
      } else if (seleccionadas.length < 8) {
        seleccionadas.push({ id, label });
        btn.classList.add('selected');
      } else {
        toast('Podés seleccionar hasta 8 butacas.');
      }

      $('#selectedSeatsText').textContent = seleccionadas.length
        ? seleccionadas.map(s => s.label).join(', ')
        : 'Ninguna seleccionada';
      $('#seatTotal').textContent = money(seleccionadas.length * precioUnitario);
      $('#toCheckout').disabled = seleccionadas.length === 0;

      $('#butacasIdsInput').value = seleccionadas.map(s => s.id).join(',');
      $('#butacasLabelsInput').value = seleccionadas.map(s => s.label).join(', ');
    });
  });

  $$('.time-button').forEach(b => b.addEventListener('click', () => {
    $$('.time-button').forEach(x => x.classList.remove('selected'));
    b.classList.add('selected');
  }));
}

// CHECKOUT
function renderSnacks() {
  const grid = $('#snackGrid');
  if (!grid) return;
  grid.innerHTML = snacks.map(s => `
    <div class="snack-item">
      <div class="snack-emoji">${s.emoji}</div>
      <div class="snack-info">
        <b>${s.name}</b>
        <small>${money(s.price)}</small>
      </div>
      <div class="qty">
        <button type="button" data-minus="${s.id}" aria-label="Quitar uno">−</button>
        <span>${quantities[s.id]}</span>
        <button type="button" class="plus" data-plus="${s.id}" aria-label="Agregar uno">+</button>
      </div>
    </div>
  `).join('');

  $$('[data-minus]').forEach(b => b.addEventListener('click', () => {
    quantities[b.dataset.minus] = Math.max(0, quantities[b.dataset.minus] - 1);
    renderCheckout();
  }));
  $$('[data-plus]').forEach(b => b.addEventListener('click', () => {
    quantities[b.dataset.plus]++;
    renderCheckout();
  }));
}

function getTotals() {
  const seatCount = selectedSeats.length || 2;
  const ticketsSubtotal = seatCount * 6900;
  const snacksSubtotal = snacks.reduce((sum, s) => sum + s.price * quantities[s.id], 0);
  const subtotal = ticketsSubtotal + snacksSubtotal;
  const service = Math.round(subtotal * 0.06);
  const iva = Math.round((subtotal + service) * 0.21);
  return { subtotal, service, iva, total: subtotal + service + iva, ticketsSubtotal, snacksSubtotal, seatCount };
}

function renderCheckout() {
  if (!$('#priceLines')) return;
  renderSnacks();
  const t = getTotals();
  const seatsLabel = selectedSeats.length ? selectedSeats.join(', ') : 'F7, F8';
  const checkoutSeatEl = $('#checkoutSeatNames');
  if (checkoutSeatEl) checkoutSeatEl.textContent = seatsLabel;

  const entries = [
    `<div><span>${t.seatCount} × Entrada general</span><b>${money(t.ticketsSubtotal)}</b></div>`
  ];
  snacks.filter(s => quantities[s.id] > 0).forEach(s => {
    entries.push(`<div><span>${quantities[s.id]} × ${s.name}</span><b>${money(s.price * quantities[s.id])}</b></div>`);
  });

  $('#priceLines').innerHTML = entries.join('');
  $('#subtotalAmount').textContent = money(t.subtotal);
  $('#serviceAmount').textContent = money(t.service);
  $('#ivaAmount').textContent = money(t.iva);
  $('#grandTotal').textContent = money(t.total);

  $$('.payment-option').forEach(o => o.addEventListener('click', () => {
    $$('.payment-option').forEach(x => x.classList.remove('selected'));
    o.classList.add('selected');
    o.querySelector('input').checked = true;
  }));
}

if ($('#view-checkout')) {
  renderCheckout();
  $('#confirmPurchase')?.addEventListener('click', () => {
    const payment = $('input[name="payment"]:checked')?.value || 'Visa';
    const totals = getTotals();
    sessionStorage.setItem('cp_receipt', JSON.stringify({
      seats: selectedSeats.length ? selectedSeats.join(', ') : 'F7, F8',
      payment,
      total: totals.total,
      code: 'CP-' + Math.floor(100000 + Math.random() * 899999)
    }));
    window.location.href = '/comprobante';
  });
}

// COMPROBANTE
function drawFakeQR() {
  const qr = $('#qrCode');
  if (!qr) return;
  qr.innerHTML = '';
  let seed = 17;
  const rand = () => { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
  const cells = Array.from({ length: 441 }, () => rand() > 0.52);

  function finder(x, y) {
    for (let r = 0; r < 7; r++) {
      for (let c = 0; c < 7; c++) {
        const edge = r === 0 || r === 6 || c === 0 || c === 6;
        const center = r >= 2 && r <= 4 && c >= 2 && c <= 4;
        cells[(y + r) * 21 + x + c] = edge || center;
      }
    }
  }
  finder(0, 0);
  finder(14, 0);
  finder(0, 14);

  cells.forEach(v => {
    const d = document.createElement('i');
    d.className = 'qr-cell' + (v ? ' dark' : '');
    qr.appendChild(d);
  });
}

if ($('#view-comprobante')) {
  drawFakeQR();
  const saved = JSON.parse(sessionStorage.getItem('cp_receipt') || 'null');
  if (saved) {
    if ($('#receiptSeats')) $('#receiptSeats').textContent = saved.seats;
    if ($('#receiptPayment')) $('#receiptPayment').textContent = saved.payment;
    if ($('#receiptTotal')) $('#receiptTotal').textContent = money(saved.total);
    if ($('#orderCode')) $('#orderCode').textContent = saved.code;
  }
  $('#downloadReceipt')?.addEventListener('click', () => window.print());
}

// MIS ENTRADAS
function renderTickets() {
  const list = $('#ticketList');
  if (!list) return;
  const visible = tickets.filter(t => currentTicketFilter === 'Todas' || t.status === currentTicketFilter);
  list.innerHTML = visible.map(t => `
    <article class="ticket-card">
      <div class="ticket-poster ${t.poster}">${t.title.toUpperCase()}</div>
      <div class="ticket-content">
        <div class="ticket-title-row">
          <h3>${t.title}</h3>
          <span class="status ${t.status}">${t.status}</span>
        </div>
        <div class="ticket-meta">
          <span>FECHA<b>${t.date}</b></span>
          <span>HORARIO<b>${t.time}</b></span>
          <span>SALA<b>${t.room}</b></span>
          <span>BUTACAS<b>${t.seats}</b></span>
        </div>
        <div class="ticket-actions">
          <small>Orden ${t.id} · Total ${money(t.total)}</small>
          <div>
            <a class="button" href="/comprobante" data-view-receipt="${t.id}">▦ Ver QR / Factura</a>
            ${t.status === 'Activo' ? `<button type="button" class="button button-ghost" data-cancel="${t.id}">Cancelar entrada</button>` : ''}
          </div>
        </div>
      </div>
    </article>
  `).join('') || '<div class="panel muted">No hay entradas en esta categoría.</div>';

  $$('[data-cancel]').forEach(b => b.addEventListener('click', () => {
    const t = tickets.find(x => x.id === b.dataset.cancel);
    if (confirm(`¿Solicitar la cancelación de ${t.title}? La operación es ilustrativa.`)) {
      t.status = 'Cancelado';
      renderTickets();
      toast('Solicitud de cancelación registrada en la demo.');
    }
  }));

  $$('[data-view-receipt]').forEach(b => b.addEventListener('click', () => {
    const t = tickets.find(x => x.id === b.dataset.viewReceipt);
    sessionStorage.setItem('cp_receipt', JSON.stringify({
      seats: t.seats,
      payment: 'Visa •••• 4242',
      total: t.total,
      code: t.id
    }));
  }));
}

if ($('#ticketList')) {
  renderTickets();
  $$('#ticketTabs .tab').forEach(b => b.addEventListener('click', () => {
    $$('#ticketTabs .tab').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
    currentTicketFilter = b.dataset.filter;
    renderTickets();
  }));
}

// GESTIÓN (BACKOFFICE) 
function renderAdminMovies() {
  const tbody = $('#adminMovieRows');
  if (!tbody) return;
  const q = $('#movieSearch').value.toLowerCase();
  const state = $('#statusFilter').value;
  const rows = movies.filter(m => (state === 'Todos' || m.status === state) && (`${m.title} ${m.genre}`).toLowerCase().includes(q));
  $('#adminCount').textContent = `${rows.length} películas`;

  tbody.innerHTML = rows.map(m => `
    <tr>
      <td>
        <div class="movie-cell">
          <i class="mini-poster ${m.poster}"></i>
          <span><b>${m.title}</b><small>2026 · Cine Paradiso</small></span>
        </div>
      </td>
      <td>${m.genre}</td>
      <td>${m.duration} min</td>
      <td>${m.rating}</td>
      <td><span class="state-dot ${m.status}">${m.status}</span></td>
      <td>
        <div class="table-actions">
          <button type="button" title="Editar" data-edit="${m.id}">✎</button>
          <button type="button" title="Dar de baja" data-delete="${m.id}">⌫</button>
        </div>
      </td>
    </tr>
  `).join('');

  $$('[data-edit]').forEach(b => b.addEventListener('click', () => openMovieDialog(Number(b.dataset.edit))));
  $$('[data-delete]').forEach(b => b.addEventListener('click', () => {
    const m = movies.find(x => x.id === Number(b.dataset.delete));
    if (confirm(`¿Dar de baja (inactivar) "${m.title}"?`)) {
      m.status = 'Inactiva';
      renderAdminMovies();
      toast('Película dada de baja lógica.');
    }
  }));
}

function openMovieDialog(id = null) {
  editingMovieId = id;
  const form = $('#movieForm');
  form.reset();
  $('#movieDialogTitle').textContent = id ? 'Editar película' : 'Nueva película';
  if (id) {
    const m = movies.find(x => x.id === id);
    form.elements.title.value = m.title;
    form.elements.genre.value = m.genre;
    form.elements.duration.value = m.duration;
    form.elements.rating.value = m.rating;
    form.elements.status.value = m.status;
  }
  $('#movieDialog').showModal();
}

if ($('#view-gestion')) {
  renderAdminMovies();
  $('#movieSearch')?.addEventListener('input', renderAdminMovies);
  $('#statusFilter')?.addEventListener('change', renderAdminMovies);
  $('#addMovie')?.addEventListener('click', () => openMovieDialog());
  $('#movieForm')?.addEventListener('submit', e => {
    e.preventDefault();
    const form = e.currentTarget;
    const data = {
      title: form.elements.title.value.trim(),
      genre: form.elements.genre.value.trim(),
      duration: Number(form.elements.duration.value),
      rating: form.elements.rating.value,
      status: form.elements.status.value
    };
    if (editingMovieId) {
      Object.assign(movies.find(x => x.id === editingMovieId), data);
      toast('Película actualizada en la demo.');
    } else {
      movies.push({ id: Math.max(...movies.map(m => m.id)) + 1, ...data, tag: '', poster: 'poster-purple' });
      toast('Película creada en la demo.');
    }
    $('#movieDialog').close();
    renderAdminMovies();
  });
  $('#importMovies')?.addEventListener('click', () => toast('La importación requiere conectar GET /api/peliculas/externas.'));
  $('#cameraBtn')?.addEventListener('click', () => toast('La lectura por cámara debe implementarse con permisos y acceso al dispositivo.'));
  $('#validateQr')?.addEventListener('click', () => {
    const code = $('#qrInput').value.trim();
    const ok = /^CP-\d{5,6}$/.test(code);
    const box = $('#validationResult');
    box.className = 'validation-result ' + (ok ? 'valid' : 'invalid');
    box.textContent = ok
      ? `✓ Código ${code}: formato válido (demo). La autorización real debe confirmarse con POST /api/entradas/validar.`
      : '✕ Código inválido. Revisá el identificador e intentá nuevamente.';
  });
}

// DASHBOARD
if ($('#view-dashboard')) {
  const hourValues = [30, 45, 60, 82, 96, 112, 140, 165, 230, 190, 155];
  const hourLabels = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'];
  if ($('#hourChart')) {
    $('#hourChart').innerHTML = hourValues.map((v, i) => `
      <div class="bar-item ${i === 8 ? 'highlight' : ''}">
        <b>${v}</b>
        <i style="height:${(v / 240) * 100}%"></i>
        <small>${hourLabels[i]}:00</small>
      </div>
    `).join('');
  }

  const occup = [
    ['Órbita Perdida', 94],
    ['Código de Fuego', 79],
    ['Ecos en la Oscuridad', 68],
    ['La Ciudad Sumergida', 53],
    ['Cartas de Invierno', 42]
  ];
  if ($('#occupancyList')) {
    $('#occupancyList').innerHTML = occup.map(([name, p]) => `
      <div class="occupancy-row">
        <span>${name}</span>
        <div class="progress"><i style="width:${p}%"></i></div>
        <b>${p}%</b>
      </div>
    `).join('');
  }

  $('#exportReport')?.addEventListener('click', () => {
    const rows = [
      ['Indicador', 'Valor'],
      ['Ventas totales', '$186.480'],
      ['Tasa de ocupación', '72,4%'],
      ['Funciones activas', '24'],
      ['Cancelaciones', '18']
    ];
    const csv = rows.map(r => r.join(';')).join('\n');
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'reporte-cine-paradiso.csv';
    a.click();
    URL.revokeObjectURL(a.href);
  });
}