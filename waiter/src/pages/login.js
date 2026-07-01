// src/pages/login.js — 登录页（左右结构 + 验证码）

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
    ctx.strokeStyle = `rgba(245,158,11,0.15)`;
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

export function renderLogin(el) {
  el.innerHTML = `
    <div class="login-split">
      <div class="login-left">
        <div class="login-left-inner">
          <div class="login-logo">SKEWER</div>
          <h1>竹签识别<br />计价系统</h1>
          <p class="login-desc">
            基于 YOLO 深度学习模型的智能竹签计数与计价解决方案
          </p>
          <div class="login-features">
            <div class="lf-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              AI 拍照识别，秒级计数
            </div>
            <div class="lf-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              实时桌况一览，高效管理
            </div>
            <div class="lf-item">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              一键结账，自动计价汇总
            </div>
          </div>
        </div>
      </div>
      <div class="login-right">
        <div class="login-form-wrap">
          <h2>服务员登录</h2>
          <form autocomplete="off" onsubmit="return false">
            <input class="input" id="login-user" placeholder="用户名" autocomplete="username" />
            <input class="input" id="login-pass" type="password" placeholder="密码" autocomplete="current-password" />
            <div class="captcha-row">
              <canvas id="captcha-canvas" width="140" height="48"></canvas>
              <span class="captcha-refresh" id="captcha-refresh">换一张</span>
            </div>
            <input class="input" id="login-captcha" placeholder="验证码" maxlength="4" />
            <p class="login-error" id="login-error"></p>
            <button class="btn btn-primary btn-block" id="login-btn" type="submit">登 录</button>
          </form>
          <p style="text-align:center;margin-top:20px;color:var(--text-muted);font-size:13px">
            没有账号？<a href="#/register" style="color:var(--primary);text-decoration:none">去注册</a>
          </p>
        </div>
      </div>
    </div>
  `;

  const canvas = el.querySelector('#captcha-canvas');
  generateCaptcha(canvas);

  el.querySelector('#captcha-refresh').onclick = () => generateCaptcha(canvas);
  canvas.onclick = () => generateCaptcha(canvas);

  const doLogin = async () => {
    const username = el.querySelector('#login-user').value.trim();
    const password = el.querySelector('#login-pass').value;
    const inputCode = el.querySelector('#login-captcha').value.trim().toUpperCase();
    const btn = el.querySelector('#login-btn');
    const errEl = el.querySelector('#login-error');

    if (!username || !password) {
      errEl.textContent = '请输入用户名和密码';
      errEl.style.display = 'block';
      return;
    }
    if (inputCode !== captchaCode) {
      errEl.textContent = '验证码错误';
      errEl.style.display = 'block';
      generateCaptcha(canvas);
      el.querySelector('#login-captcha').value = '';
      return;
    }

    btn.disabled = true;
    btn.textContent = '登录中...';
    errEl.style.display = 'none';

    try {
      const data = await login(username, password);
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify({
        username: data.username,
        real_name: data.real_name,
        role: data.role,
      }));
      window.location.hash = '#/';
    } catch (e) {
      errEl.textContent = e.message || '登录失败';
      errEl.style.display = 'block';
      btn.disabled = false;
      btn.textContent = '登 录';
    }
  };

  el.querySelector('#login-btn').onclick = doLogin;
  el.querySelectorAll('.input').forEach(input => {
    input.onkeydown = (e) => { if (e.key === 'Enter') doLogin(); };
  });
}
