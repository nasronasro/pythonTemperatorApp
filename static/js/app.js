/* static/js/app.js */
const LATEST_URL = "/latest/";

const tempEl = document.getElementById('temp');
const humEl  = document.getElementById('hum');
const timeEl = document.getElementById('time');
const statusEl = document.getElementById('status');
const refreshBtn = document.getElementById('refresh');
const spinner = refreshBtn.querySelector('.spinner-border');

let isFetching = false;

function formatDate(iso) {
  return new Date(iso).toLocaleString('fr-MA', {
    timeZone: 'Africa/Casablanca',
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
}

async function fetchLatest() {
  if (isFetching) return;
  isFetching = true;

  spinner.classList.remove('d-none');
  refreshBtn.disabled = true;

  try {
    const res = await fetch(LATEST_URL, { cache: 'no-store' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const d = await res.json();
    tempEl.textContent = parseFloat(d.temperature).toFixed(1);
    humEl.textContent  = parseFloat(d.humidity).toFixed(1);
    timeEl.textContent = formatDate(d.timestamp);

    statusEl.textContent = "En ligne";
    statusEl.className = "badge bg-success fs-6";
  } catch (e) {
    statusEl.textContent = "Hors ligne";
    statusEl.className = "badge bg-danger fs-6";
    console.warn("Fetch failed:", e.message);
  } finally {
    spinner.classList.add('d-none');
    refreshBtn.disabled = false;
    isFetching = false;
  }
}

// Auto-refresh every 20 seconds
function startAutoRefresh() {
  fetchLatest();
  setInterval(() => {
    if (!document.hidden) fetchLatest();
  }, 20000);
}

// Events
refreshBtn.addEventListener('click', fetchLatest);

// Start
startAutoRefresh();

// Pause when tab is hidden
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    // No action – interval keeps running but skips fetch
  }
});