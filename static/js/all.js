/* static/js/all.js */
const API_URL = "/api";
const refreshBtn = document.getElementById('refresh');
const spinner = refreshBtn.querySelector('.spinner-border');
const rangeButtons = document.querySelectorAll('[data-range]');

let isFetching = false;
let tempChart, humChart;
let currentRange = 'today'; // default

// Time helpers (Morocco time)
const now = () => new Date().toLocaleString('sv', { timeZone: 'Africa/Casablanca' });
const startOfDay = () => new Date(now().split(' ')[0] + ' 00:00:00');
const daysAgo = (days) => {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d;
};

function filterByRange(records, range) {
  const cutoff = range === 'today' ? startOfDay() :
                 range === '7days' ? daysAgo(7) :
                 daysAgo(30);

  return records.filter(r => new Date(r.dt) >= cutoff);
}

function formatTime(iso) {
  const date = new Date(iso);
  const options = { timeZone: 'Africa/Casablanca' };
  if (currentRange === 'today') {
    return date.toLocaleTimeString('fr-MA', { ...options, hour: '2-digit', minute: '2-digit' });
  }
  return date.toLocaleString('fr-MA', { ...options, month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function initCharts() {
  const tempCtx = document.getElementById('tempChart').getContext('2d');
  const humCtx = document.getElementById('humChart').getContext('2d');

  tempChart = new Chart(tempCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Temp', data: [], borderColor: '#dc3545', backgroundColor: 'rgba(220,53,69,0.1)', fill: true, tension: 0.3 }] },
    options: { responsive: true, scales: { x: { ticks: { maxTicksLimit: 10 } }, y: { beginAtZero: false } }, plugins: { legend: { display: false } } }
  });

  humChart = new Chart(humCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Hum', data: [], borderColor: '#0dcaf0', backgroundColor: 'rgba(13,202,240,0.1)', fill: true, tension: 0.3 }] },
    options: { responsive: true, scales: { x: { ticks: { maxTicksLimit: 10 } }, y: { beginAtZero: true, suggestedMax: 100 } }, plugins: { legend: { display: false } } }
  });
}

async function loadData() {
  if (isFetching) return;
  isFetching = true;

  spinner.classList.remove('d-none');
  refreshBtn.disabled = true;

  try {
    const res = await fetch(API_URL, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    let payload = await res.json();

    let data = payload;
    if (payload && payload.data) data = payload.data;

    let records = [];
    if (data && Array.isArray(data.results)) records = data.results;
    else if (Array.isArray(data)) records = data;
    else throw new Error("Aucune donnée");

    // Sort by date
    records.sort((a, b) => new Date(a.dt) - new Date(b.dt));

    // Filter by selected range
    const filtered = filterByRange(records, currentRange);

    if (filtered.length === 0) {
      alert(`Aucune donnée pour: ${currentRange === 'today' ? "aujourd'hui" : currentRange === '7days' ? 'les 7 derniers jours' : 'les 30 derniers jours'}`);
      return;
    }

    const labels = filtered.map(r => formatTime(r.dt));
    const temps = filtered.map(r => parseFloat(r.temp).toFixed(1));
    const hums = filtered.map(r => parseFloat(r.hum).toFixed(1));

    // Update charts
    tempChart.data.labels = labels;
    tempChart.data.datasets[0].data = temps;
    tempChart.update('quiet');

    humChart.data.labels = labels;
    humChart.data.datasets[0].data = hums;
    humChart.update('quiet');

  } catch (e) {
    alert("Erreur: " + e.message);
    console.error(e);
  } finally {
    spinner.classList.add('d-none');
    refreshBtn.disabled = false;
    isFetching = false;
  }
}

// Button handlers
rangeButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    rangeButtons.forEach(b => b.classList.remove('btn-primary', 'active'));
    rangeButtons.forEach(b => b.classList.add('btn-outline-primary'));
    btn.classList.remove('btn-outline-primary');
    btn.classList.add('btn-primary', 'active');
    currentRange = btn.dataset.range;
    loadData();
  });
});

refreshBtn.addEventListener('click', loadData);

// Auto-refresh
function startAutoRefresh() {
  initCharts();
  loadData();
  setInterval(() => {
    if (!document.hidden) loadData();
  }, 30000);
}

startAutoRefresh();