// src/pages/tables.js — 桌况一览

import { getTables } from '../api.js';

const STATUS_MAP = {
  0: { label: '空闲', cls: 'status-free' },
  1: { label: '占用', cls: 'status-busy' },
  2: { label: '清洁中', cls: 'status-cleaning' },
};

let _el;
let _pollTimer = null;

export async function renderTables(el) {
  _el = el;
  el.innerHTML = '<p class="loading">加载中...</p>';
  startPoll();

  try {
    const tables = await getTables();
    renderContent(el, tables);
  } catch (e) {
    el.innerHTML = `<p class="error">加载失败: ${e.message}</p>`;
  }
}

function startPoll() {
  stopPoll();
  _pollTimer = setInterval(async () => {
    if (!_el || !document.body.contains(_el)) { stopPoll(); return; }
    try {
      const tables = await getTables();
      renderContent(_el, tables);
    } catch (_) {}
  }, 15000);
}

function stopPoll() {
  if (_pollTimer) { clearInterval(_pollTimer); _pollTimer = null; }
}

function renderContent(el, tables) {
  el.innerHTML = '<h2>桌况一览</h2>';

  const zones = {};
  tables.forEach(t => {
    if (!zones[t.zone_name]) zones[t.zone_name] = [];
    zones[t.zone_name].push(t);
  });

  Object.entries(zones).forEach(([zoneName, zoneTables]) => {
    const surcharge = zoneTables[0].zone_surcharge;

    const zoneEl = document.createElement('div');
    zoneEl.className = 'zone-group';
    zoneEl.innerHTML = `
      <h3 class="zone-title">
        ${zoneName}
        ${surcharge > 0 ? `<span class="zone-surcharge">+¥${surcharge.toFixed(0)}</span>` : ''}
      </h3>
      <div class="table-grid"></div>
    `;

    const grid = zoneEl.querySelector('.table-grid');

    zoneTables.forEach(t => {
      const st = STATUS_MAP[t.table_status];
      const free = t.table_status === 0;

      const card = document.createElement('div');
      card.className = `table-card ${st.cls}`;
      if (t.table_status === 2) card.classList.add('disabled');

      card.innerHTML = `
        <div class="table-code">${t.table_code}</div>
        <div class="table-status">${st.label}</div>
        <div class="table-capacity">${t.capacity}座</div>
        ${!free ? `
          <div class="table-info">
            <div>编号: ${t.order_no || '-'}</div>
            <div>签子: ${t.total_count ?? '-'}根</div>
            <div>服务员: ${t.waiter_name || '-'}</div>
            <div class="table-time">${t.order_created_at ? formatTime(t.order_created_at) : ''}</div>
          </div>
        ` : ''}
      `;

      if (!(t.table_status === 2)) {
        card.style.cursor = 'pointer';
        card.onclick = () => {
          if (free) {
            window.location.hash = `#/orders/new?tableId=${t.table_id}`;
          } else if (t.order_id) {
            window.location.hash = `#/orders/${t.order_id}`;
          }
        };
      }

      grid.appendChild(card);
    });

    el.appendChild(zoneEl);
  });

  const refresh = document.createElement('button');
  refresh.className = 'btn btn-sm btn-fresh';
  refresh.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 4v6h6M23 20v-6h-6"/><path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4-4.64 4.36A9 9 0 0 1 3.51 15"/></svg> 刷新';
  refresh.onclick = () => renderTables(el);
  el.prepend(refresh);
}

function formatTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}
