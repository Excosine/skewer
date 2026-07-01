// src/api.js — fetch 封装，自动带 Token，401 跳登录

const BASE = '/api';

async function request(method, path, data = null) {
  const headers = {};
  const token = localStorage.getItem('token');
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers };

  if (data instanceof FormData) {
    opts.body = data;
  } else if (data) {
    headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(data);
  }

  const res = await fetch(`${BASE}${path}`, opts);
  const body = await res.json().catch(() => null);

  if (res.status === 401) {
    localStorage.clear();
    window.location.hash = '#/login';
    throw new Error(body?.detail || '未登录');
  }

  if (!res.ok) {
    throw new Error(body?.detail || `请求失败 (${res.status})`);
  }

  return body;
}

// ---------- Auth ----------
export function login(username, password) {
  return request('POST', '/auth/login', { username, password });
}

// ---------- Tables ----------
export function getTables() {
  return request('GET', '/tables');
}

// ---------- Orders ----------
export function createOrder(table_id) {
  return request('POST', '/orders', { table_id });
}

export function getOrder(order_id) {
  return request('GET', `/orders/${order_id}`);
}

export function scanOrder(order_id, file) {
  const fd = new FormData();
  fd.append('image', file);
  return request('POST', `/orders/${order_id}/scan`, fd);
}

export function closeOrder(order_id) {
  return request('POST', `/orders/${order_id}/close`);
}
