// src/pages/register.js — 注册页

import { login } from '../api.js';

let captchaCode = '';

function generateCaptcha(canvas) {
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  ctx.fillStyle = '#1A1410';
  ctx.fillRect(0, 0, w, h);

  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  captchaCode = '';
  for (let i = 0; i < 4; i++) {
    captchaCode += chars[Math.floor(Math.random() * chars.length)];
  }

  for (let i = 0; i < 4; i++) {
    ctx.strokeStyle = 'rgba(245,158,11,0.15)';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(Math.random() * w, Math.random() * h);
    ctx.lineTo(Math.random() * w, Math.random() * h);
    ctx.stroke();
  }

  ctx.font = 'bold 24px "Courier New", monospace';
  ctx.textBaseline = 'middle';
  for (let i = 0; i < captchaCode.length; i++) {
    const x = 14 + i * 30 + (Math.random() - 0.5) * 6;
    const y = h / 2 + (Math.random() - 0.5) * 8;
    ctx.fillStyle = '#F59E0B';
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate((Math.random() - 0.5) * 0.4);
    ctx.fillText(captchaCode[i], 0, 0);
    ctx.restore();
  }
}

const BASE = '/api';

async function register(username, password, realName) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, real_name: realName }),
  });
  const body = await res.json();
  if (!res.ok) throw new Error(body.detail || '注册失败');
  return body;
}

export function renderRegister(el) {
  el.innerHTML = `
    <div class="login-split">
      <div class="login-left">
        <div class="login-left-inner">
          <div class="login-logo">SKEWER</div>
          <h1>创建账号</h1>
          <p class="login-desc">
            注册新服务员账号，<br />开始使用竹签识别计价系统
          </p>
          <div class="login-features">
            <div class="lf-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              注册即用，无需审核
            </div>
            <div class="lf-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              支持多人同时操作
            </div>
          </div>
        </div>
      </div>
      <div class="login-right">
        <div class="login-form-wrap">
          <h2>注册新账号</h2>
          <form autocomplete="off" onsubmit="return false">
            <input class="input" id="reg-user" placeholder="用户名" autocomplete="username" />
            <input class="input" id="reg-pass" type="password" placeholder="密码" autocomplete="new-password" />
            <input class="input" id="reg-name" placeholder="真实姓名" />
            <div class="captcha-row">
              <canvas id="captcha-canvas" width="140" height="48"></canvas>
              <span class="captcha-refresh" id="captcha-refresh">换一张</span>
            </div>
            <input class="input" id="reg-captcha" placeholder="验证码" maxlength="4" />
            <p class="login-error" id="reg-error"></p>
            <button class="btn btn-primary btn-block" id="reg-btn" type="submit">注 册</button>
          </form>
          <p style="text-align:center;margin-top:20px;color:var(--text-muted);font-size:13px">
            已有账号？<a href="#/login" style="color:var(--primary);text-decoration:none">去登录</a>
          </p>
        </div>
      </div>
    </div>
  `;

  const canvas = el.querySelector('#captcha-canvas');
  generateCaptcha(canvas);

  el.querySelector('#captcha-refresh').onclick = () => generateCaptcha(canvas);
  canvas.onclick = () => generateCaptcha(canvas);

  const doRegister = async () => {
    const username = el.querySelector('#reg-user').value.trim();
    const password = el.querySelector('#reg-pass').value;
    const realName = el.querySelector('#reg-name').value.trim();
    const inputCode = el.querySelector('#reg-captcha').value.trim().toUpperCase();
    const btn = el.querySelector('#reg-btn');
    const errEl = el.querySelector('#reg-error');

    if (!username || !password || !realName) {
      errEl.textContent = '请填写所有字段';
      errEl.style.display = 'block';
      return;
    }
    if (inputCode !== captchaCode) {
      errEl.textContent = '验证码错误';
      errEl.style.display = 'block';
      generateCaptcha(canvas);
      el.querySelector('#reg-captcha').value = '';
      return;
    }

    btn.disabled = true;
    btn.textContent = '注册中...';
    errEl.style.display = 'none';

    try {
      const data = await register(username, password, realName);
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify({
        username: data.username,
        real_name: data.real_name,
        role: data.role,
      }));
      window.location.hash = '#/';
    } catch (e) {
      errEl.textContent = e.message || '注册失败';
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.textContent = '注 册';
    }
  };

  el.querySelector('#reg-btn').onclick = doRegister;
  el.querySelectorAll('.input').forEach(input => {
    input.onkeydown = (e) => { if (e.key === 'Enter') doRegister(); };
  });
}
