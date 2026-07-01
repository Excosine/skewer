import { getOrder, scanOrder, closeOrder } from '../api.js';
import { toast } from '../toast.js';

let orderId;
let _el;

export async function renderOrderDetail(el, _orderId) {
  orderId = parseInt(_orderId);
  _el = el;
  el.innerHTML = '<p class="loading">加载中...</p>';

  try {
    const order = await getOrder(orderId);
    render(el, order);
  } catch (e) {
    el.innerHTML = `<p class="error">${e.message}</p>`;
  }
}

async function refresh() {
  try {
    const order = await getOrder(orderId);
    render(_el, order);
  } catch (e) {
    toast(e.message, 'error');
  }
}

function render(el, order) {
  const closed = order.status === 1;
  const pps = order.price_per_skewer;

  const skewerAmt = order.total_count * pps;
  const total = +(skewerAmt + order.zone_surcharge).toFixed(2);

  el.innerHTML = `
    <h2>订单详情 ${closed ? '<span class="badge-closed">已结账</span>' : ''}</h2>

    <div class="order-info">
      <div><span class="label">订单号</span> ${order.order_no}</div>
      <div><span class="label">桌号</span> ${order.table_id}</div>
      <div><span class="label">单价</span> ¥${pps.toFixed(2)} / 根</div>
      <div><span class="label">区域加价</span> ¥${order.zone_surcharge.toFixed(2)}</div>
      <div><span class="label">签子数</span> ${order.total_count} 根</div>
      <div><span class="label">签子金额</span> ¥${skewerAmt.toFixed(2)}</div>
      <div><span class="label">应付金额</span> <strong>¥${total.toFixed(2)}</strong></div>
      <div><span class="label">状态</span> ${closed ? '已结账' : '进行中'}</div>
      <div><span class="label">开单时间</span> ${order.created_at?.replace('T', ' ').slice(0, 19) || '-'}</div>
    </div>

    ${!closed ? `
      <div class="scan-section">
        <button class="btn btn-primary btn-scan-big" id="btn-scan">拍照识别</button>
        <p class="scan-hint">拍摄所有签子合照，自动计数</p>
      </div>
      <div class="order-footer">
        <button class="btn btn-danger" id="btn-close-order">结 账</button>
      </div>
    ` : `
      <button class="btn" onclick="window.location.hash='#/'">返回桌况</button>
    `}

    <div class="modal-overlay" id="scan-modal" style="display:none">
      <div class="modal-box camera-modal">
        <h3>拍照识别签子</h3>
        <div id="camera-view"></div>
        <p id="camera-status"></p>
        <div class="btn-group">
          <button class="btn btn-primary" id="btn-capture">拍照</button>
          <input type="file" id="file-upload" accept="image/*" style="display:none" />
          <button class="btn" id="btn-upload">相册</button>
          <button class="btn" id="btn-camera-close">关闭</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay" id="confirm-close-modal" style="display:none">
      <div class="modal-box">
        <h3>确认结账</h3>
        <div id="close-summary"></div>
        <div class="btn-group">
          <button class="btn btn-danger" id="btn-confirm-close">确认结账</button>
          <button class="btn" id="btn-cancel-close">取消</button>
        </div>
      </div>
    </div>
  `;

  if (closed) return;

  el.querySelector('#btn-scan').onclick = () => openCamera(el);

  const confirmModal = el.querySelector('#confirm-close-modal');
  el.querySelector('#btn-close-order').onclick = () => {
    el.querySelector('#close-summary').innerHTML = `
      <p><span>签子数</span> <strong>${order.total_count} 根</strong></p>
      <p><span>单价</span> <strong>¥${pps.toFixed(2)} / 根</strong></p>
      <p><span>签子金额</span> <strong>¥${skewerAmt.toFixed(2)}</strong></p>
      <p><span>区域加价</span> <strong>¥${order.zone_surcharge.toFixed(2)}</strong></p>
      <hr />
      <p style="font-size:18px;font-weight:700"><span>合计</span> <strong style="color:#F59E0B">¥${total.toFixed(2)}</strong></p>
    `;
    confirmModal.style.display = 'flex';
  };

  el.querySelector('#btn-cancel-close').onclick = () => {
    confirmModal.style.display = 'none';
  };

  el.querySelector('#btn-confirm-close').onclick = async () => {
    const btn = el.querySelector('#btn-confirm-close');
    btn.disabled = true;
    btn.textContent = '结账中...';
    try {
      await closeOrder(orderId);
      toast('结账成功', 'success');
      setTimeout(() => { window.location.hash = '#/'; }, 600);
    } catch (e) {
      toast(e.message, 'error');
      btn.disabled = false;
      btn.textContent = '确认结账';
    }
  };

  confirmModal.onclick = (e) => {
    if (e.target === confirmModal) confirmModal.style.display = 'none';
  };
}

function openCamera(el) {
  const modal = el.querySelector('#scan-modal');
  const view = modal.querySelector('#camera-view');
  const status = modal.querySelector('#camera-status');

  modal.style.display = 'flex';
  view.innerHTML = '';
  status.textContent = '';

  const video = document.createElement('video');
  video.autoplay = true;
  video.playsInline = true;
  video.style.width = '100%';
  video.style.maxWidth = '400px';
  view.appendChild(video);

  const canvas = document.createElement('canvas');
  canvas.style.display = 'none';
  view.appendChild(canvas);

  let stream = null;

  navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    .then(s => {
      stream = s;
      video.srcObject = s;
    })
    .catch(() => {
      status.textContent = '无法打开摄像头，请使用"相册"上传';
    });

  modal.querySelector('#btn-capture').onclick = () => {
    if (!stream) {
      status.textContent = '摄像头不可用';
      return;
    }
    const w = video.videoWidth || 640;
    const h = video.videoHeight || 480;
    canvas.width = w;
    canvas.height = h;
    canvas.getContext('2d').drawImage(video, 0, 0, w, h);
    canvas.toBlob(blob => {
      stopCamera();
      doScan(blob, modal, status);
    }, 'image/jpeg');
  };

  modal.querySelector('#btn-upload').onclick = () => {
    modal.querySelector('#file-upload').click();
  };
  modal.querySelector('#file-upload').onchange = (e) => {
    const file = e.target.files[0];
    if (file) {
      stopCamera();
      doScan(file, modal, status);
    }
  };

  modal.querySelector('#btn-camera-close').onclick = () => {
    stopCamera();
    modal.style.display = 'none';
  };

  modal.onclick = (e) => {
    if (e.target === modal) {
      stopCamera();
      modal.style.display = 'none';
    }
  };

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(t => t.stop());
      stream = null;
    }
  }
}

async function doScan(file, modal, status) {
  status.innerHTML = '识别中...请稍候';
  modal.querySelectorAll('button').forEach(b => b.disabled = true);

  try {
    const result = await scanOrder(orderId, file);
    status.innerHTML = `<span style="color:#22C55E">识别完成: ${result.detected_count} 根签子 (置信度 ${result.confidence_avg.toFixed(2)})</span>`;
    setTimeout(() => {
      modal.style.display = 'none';
      toast('识别完成，数量已更新', 'success');
      refresh();
    }, 1200);
  } catch (e) {
    status.innerHTML = `<span style="color:#EF4444">识别失败: ${e.message}</span>`;
    modal.querySelectorAll('button').forEach(b => b.disabled = false);
  }
}