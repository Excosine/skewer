// src/main.js — 路由 + 主入口

import './style.css';
import { getOrder, createOrder } from './api.js';
import { renderLogin } from './pages/login.js';
import { renderRegister } from './pages/register.js';
import { renderTables } from './pages/tables.js';
import { renderOrderDetail } from './pages/order-detail.js';

const app = document.getElementById('app');

function parseRoute() {
  const hash = window.location.hash.slice(1) || '/';
  const [path, qs] = hash.split('?');
  const params = {};
  if (qs) {
    qs.split('&').forEach(p => {
      const [k, v] = p.split('=');
      params[decodeURIComponent(k)] = decodeURIComponent(v);
    });
  }
  return { path, params };
}

function isLoggedIn() {
  return !!localStorage.getItem('token');
}

// 渲染 Header 栏
function renderHeader() {
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  const el = document.createElement('div');
  el.className = 'header';
  el.innerHTML = `
    <span class="header-title">竹签识别计价系统</span>
    <span class="header-user">${user.real_name || ''}</span>
    <button class="btn btn-sm" id="btn-logout">退出</button>
  `;
  el.querySelector('#btn-logout').onclick = () => {
    localStorage.clear();
    window.location.hash = '#/login';
  };
  return el;
}

async function router() {
  const { path, params } = parseRoute();

  // 未登录 → 跳登录页
  if (!isLoggedIn()) {
    window.location.hash = '#/login';
    await renderPage('login', params);
    return;
  }

  switch (path) {
    case '/login':
      if (isLoggedIn()) { window.location.hash = '#/'; return; }
      await renderPage('login', params);
      break;
    case '/register':
      if (isLoggedIn()) { window.location.hash = '#/'; return; }
      await renderPage('register', params);
      break;
    case '/':
      await renderPage('tables', params);
      break;
    case '/orders/new':
      await renderPage('order-create', params);
      break;
    default:
      if (path.startsWith('/orders/')) {
        await renderPage('order-detail', {
          orderId: path.split('/')[2],
          ...params,
        });
      } else {
        app.innerHTML = '<div class="page"><h2>404 页面不存在</h2></div>';
      }
  }
}

async function renderPage(page, params) {
  app.innerHTML = '';

  if (page === 'login') {
    const container = document.createElement('div');
    container.className = 'login-page';
    await renderLogin(container);
    app.appendChild(container);
    return;
  }

  if (page !== 'login') {
    app.appendChild(renderHeader());
  }

  const container = document.createElement('div');
  container.className = 'page';

  switch (page) {
    case 'login':
      await renderLogin(container);
      break;
    case 'register':
      await renderRegister(container);
      break;
    case 'tables':
      await renderTables(container);
      break;
    case 'order-create':
      await renderOrderCreate(container, params);
      break;
    case 'order-detail':
      await renderOrderDetail(container, params.orderId);
      break;
  }

  app.appendChild(container);
}

// 开单：确认 → 调接口 → 跳详情页
async function renderOrderCreate(el, params) {
  const tableId = parseInt(params.tableId);
  if (!tableId) {
    el.innerHTML = '<p>缺少桌号参数</p>';
    return;
  }

  el.innerHTML = `
    <h2>确认开单</h2>
    <p>桌号: <strong id="oc-table"></strong></p>
    <p id="oc-error" style="color:red;display:none"></p>
    <div class="btn-group">
      <button class="btn btn-primary" id="oc-confirm">确认开单</button>
      <button class="btn" id="oc-cancel">取消</button>
    </div>
  `;

  el.querySelector('#oc-table').textContent = tableId;

  el.querySelector('#oc-cancel').onclick = () => {
    window.location.hash = '#/';
  };

  el.querySelector('#oc-confirm').onclick = async () => {
    const btn = el.querySelector('#oc-confirm');
    const err = el.querySelector('#oc-error');
    btn.disabled = true;
    btn.textContent = '开单中...';
    try {
      const order = await createOrder(tableId);
      window.location.hash = `#/orders/${order.id}`;
    } catch (e) {
      err.textContent = e.message;
      err.style.display = 'block';
      btn.disabled = false;
      btn.textContent = '确认开单';
    }
  };
}

// 监听 hash 变化
window.addEventListener('hashchange', router);
window.addEventListener('load', router);
