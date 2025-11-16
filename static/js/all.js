/* static/js/all.js */
const API_URL = "/api";
const refreshBtn = document.getElementById('refresh');
const spinner = refreshBtn.querySelector('.spinner-border');

let isFetching = false;
let tempChart, humChart;

// Initialize Charts
function initCharts() {
  const tempCtx = document.getElementById('tempChart').getContext('2d');
  const humCtx = document.getElementById('humChart').getContext('2d');

  tempChart = new Chart(tempCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Température', data: [], borderColor: '#dc3545', backgroundColor: 'rgba(220,53,69,0.1)', fill: true, tension: 0.3 }] },
    options: { responsive: true, scales: { x: { display: true }, y: { beginAtZero: false } }, plugins: { legend: { display: false } } }
  });

  humChart = new Chart(humCtx, {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Humidité', data: [], borderColor: '#0dcaf0', backgroundColor: 'rgba(13,202,240,0.1)', fill: true, tension: 0.3 }] },
    options: { responsive: true, scales: { x: { display: true }, y: { beginAtZero: true, suggestedMax: 100 } }, plugins: { legend: { display: false } } }
  });
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString('fr-MA', {
    timeZone: 'Africa/Casablanca',
    hour: '2-digit',
    minute: '2-digit'
  });
}

async function loadAll() {
  if (isFetching) return;
  isFetching = true;

  spinner.classList.remove('d-none');
  refreshBtn.disabled = true;

  try {
    const res = await fetch(API_URL, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    let payload = await res.json();

    // Handle your exact format: data.data
    let data = payload;
    if (payload && payload.data) data = payload.data;

    let records = [];

    // Case 1: { results: [...] }
    if (data && Array.isArray(data.results)) {
      records = data.results;
    }
    // Case 2: direct array
    else if (Array.isArray(data)) {
      records = data;
    }
    else {
      throw new Error("Aucune donnée valide trouvée");
    }

    if (records.length === 0) {
      alert("Aucune donnée à afficher");
      return;
    }

    // Sort by date (newest last)
    records.sort((a, b) => new Date(a.dt) - new Date(b.dt));

    const labels = records.map(r => formatTime(r.dt));
    const temps = records.map(r => parseFloat(r.temp).toFixed(1));
    const hums = records.map(r => parseFloat(r.hum).toFixed(1));

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

// Auto-refresh
function startAutoRefresh() {
  initCharts();
  loadAll();
  setInterval(() => {
    if (!document.hidden) loadAll();
  }, 30000);
}

// Events
refreshBtn.addEventListener('click', loadAll);

// Start
startAutoRefresh();