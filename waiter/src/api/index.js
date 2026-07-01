const BASE = "/api";

function hdrs() {
  const t = localStorage.getItem("token");
  const h = { "Content-Type": "application/json" };
  if (t) h.Authorization = `Bearer ${t}`;
  return h;
}

async function request(path, opts = {}) {
  const res = await fetch(BASE + path, { ...opts, headers: hdrs() });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || "请求失败");
  return data;
}

export const api = {
  login: (b) => request("/auth/login", { method: "POST", body: JSON.stringify(b) }),
  register: (b) => request("/auth/register", { method: "POST", body: JSON.stringify(b) }),
  me: () => request("/auth/me"),
  getCaptcha: () => request("/auth/captcha"),
  getCaptchaImageUrl: (key) => `${BASE}/auth/captcha/image/${key}`,
  tables: () => request("/tables"),
  tableDetail: (id) => request(`/tables/${id}`),
  updateTable: (id, b) => request(`/tables/${id}`, { method: "PUT", body: JSON.stringify(b) }),
  categories: () => request("/menu/categories"),
  skewers: () => request("/menu/skewers"),
  createOrder: (b) => request("/orders", { method: "POST", body: JSON.stringify(b) }),
  getOrder: (id) => request(`/orders/${id}`),
  closeOrder: (id) => request(`/orders/${id}/close`, { method: "POST" }),
  addItem: (oid, b) => request(`/orders/${oid}/items`, { method: "POST", body: JSON.stringify(b) }),
  updateItem: (oid, iid, b) => request(`/orders/${oid}/items/${iid}`, { method: "PUT", body: JSON.stringify(b) }),
  deleteItem: (oid, iid) => request(`/orders/${oid}/items/${iid}`, { method: "DELETE" }),
  scanItem: async (oid, iid, file) => {
    const f = new FormData();
    f.append("image", file);
    const t = localStorage.getItem("token");
    const res = await fetch(`${BASE}/orders/${oid}/items/${iid}/scan`, {
      method: "POST",
      headers: t ? { Authorization: `Bearer ${t}` } : {},
      body: f,
    });
    const d = await res.json();
    if (!res.ok) throw new Error(d.detail || "识别失败");
    return d;
  },
};
