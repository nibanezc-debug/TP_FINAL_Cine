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

// Selección interactiva de butacas (sin llamadas HTTP; el envío lo hace el <form> POST de Flask)
const map = $('#seatMap');
if (map) {
  let seleccionadas = [];
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
}