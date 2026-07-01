import request from './request'

// ========== 用户管理 ==========
export function getUsers() {
  return request.get('/admin/users')
}

export function createUser(data) {
  return request.post('/admin/users', data)
}

export function updateUser(userId, data) {
  return request.put(`/admin/users/${userId}`, data)
}

// ========== 签子价格 ==========
export function getSkewers() {
  return request.get('/menu/skewers')
}

export function adjustPrice(skewerId, price) {
  return request.put(`/admin/skewers/${skewerId}/price`, { price })
}

// ========== 报表 ==========
export function getSkewerSales(date) {
  return request.get('/admin/reports/skewers', { params: { date } })
}

export function getTableRevenue(date) {
  return request.get('/admin/reports/tables', { params: { date } })
}

// ========== 订单 ==========
export function getOrderDetail(orderId) {
  return request.get(`/orders/${orderId}`)
}

export function closeOrder(orderId) {
  return request.post(`/orders/${orderId}/close`)
}

// ========== 桌况 ==========
export function getTables() {
  return request.get('/tables')
}

export function resetTable(tableCode) {
  return request.put(`/tables/${tableCode}/reset`)
}
