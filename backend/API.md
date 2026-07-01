# Skewer Counter API

## 部署方式

后端仅在本地监听 `localhost:8000`，**不直接暴露到公网**。前端通过反向代理转发请求：

```
# 开发环境（Vite / CRA / Next.js dev server）
# vite.config.ts
server: {
  proxy: {
    "/api": "http://localhost:8000"
  }
}

# 生产环境（nginx）
location /api/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

前端请求时无需拼接域名，直接用 `/api/...` 路径即可。

---

## 认证说明

除 `POST /api/auth/login` 外，所有接口需在 Header 中携带 Token：

```
Authorization: Bearer <token>
```

Token 通过登录获取，有效期 24 小时。

---

## 通用接口

### POST /api/auth/login

登录。

**Body**

```json
{
  "username": "waiter01",
  "password": "123456"
}
```

**Response** `200`

```json
{
  "token": "eyJhbGci...",
  "username": "waiter01",
  "role": "waiter",
  "real_name": "小李"
}
```

| 状态码 | 说明 |
|:------:|------|
| `200` | 成功 |
| `401` | 用户名或密码错误 |

---

### GET /api/auth/me

当前登录用户信息。

**Response** `200`

```json
{
  "id": 2,
  "username": "waiter01",
  "real_name": "小李",
  "role": "waiter"
}
```

---

### GET /api/tables

桌况一览。所有登录用户均可查看。

**Response** `200`

```json
[
  {
    "zone_name": "大厅",
    "zone_surcharge": 0.00,
    "table_code": "A01",
    "capacity": 4,
    "table_status": 1,
    "order_id": 12,
    "order_no": "20260630140500-1",
    "total_count": 30,
    "total_price": 0.00,
    "waiter_name": "小李",
    "order_created_at": "2026-06-30T14:05:00"
  }
]
```

桌空闲时 `order_id` / `total_price` 等为 `null`。

| 字段 | 说明 |
|------|------|
| `table_status` | `0`=空闲 `1`=占用 `2`=清洁中 |

---

### GET /api/menu/categories

签子类别。

**Response** `200`

```json
[
  {"id": 1, "name": "肉类"},
  {"id": 2, "name": "蔬菜"},
  {"id": 3, "name": "海鲜"},
  {"id": 4, "name": "豆制品"},
  {"id": 5, "name": "主食"}
]
```

---

### GET /api/menu/skewers

当前可售菜品（含价格）。

**Response** `200`

```json
[
  {
    "id": 1,
    "skewer_name": "牛肉串",
    "category_name": "肉类",
    "unit_price": 3.00,
    "sort_order": 1
  }
]
```

---

## 服务员接口

### POST /api/orders

开单。选择桌号创建新订单，桌子状态变为 **占用**。

**Body**

```json
{ "table_id": 1 }
```

**Response** `200`

```json
{
  "id": 12,
  "order_no": "20260630140500-1",
  "table_id": 1,
  "zone_surcharge": 0.00,
  "status": 0,
  "created_at": "2026-06-30T14:05:00"
}
```

---

### GET /api/orders/{order_id}

订单详情，含所有菜品行。

**Response** `200`

```json
{
  "id": 12,
  "order_no": "20260630140500-1",
  "table_id": 1,
  "zone_surcharge": 0.00,
  "total_count": 30,
  "total_price": 0.00,
  "status": 0,
  "created_at": "2026-06-30T14:05:00",
  "items": [
    {
      "id": 5,
      "skewer_name": "牛肉串",
      "count": 20,
      "unit_price": 3.00,
      "subtotal": 60.00
    }
  ]
}
```

| 字段 | 说明 |
|------|------|
| `status` | `0`=进行中 `1`=已结账 |

| 状态码 | 说明 |
|:------:|------|
| `200` | 成功 |
| `404` | 订单不存在 |

---

### POST /api/orders/{order_id}/close

结账。汇总数量与金额，订单状态变为 **已结账**，桌子状态变为 **清洁中**。

```python
total_price = SUM(subtotal) + zone_surcharge
```

**Response** `200`

```json
{ "status": "ok" }
```

---

### POST /api/orders/{order_id}/items

向订单添加菜品行（初始数量为 0）。同一订单同一菜品只能一条记录，重复添加返回已有 ID。

**Body**

```json
{ "skewer_type_id": 1 }
```

**Response** `200`

```json
{ "id": 5, "count": 0 }
```

---

### PUT /api/orders/{order_id}/items/{item_id}

手动修改数量，`subtotal` 自动重算。

**Body**

```json
{ "count": 18 }
```

**Response** `200`

```json
{ "status": "ok" }
```

| 状态码 | 说明 |
|:------:|------|
| `200` | 成功 |
| `404` | 明细不存在 |

---

### DELETE /api/orders/{order_id}/items/{item_id}

删除菜品行。

**Response** `200`

```json
{ "status": "ok" }
```

---

### POST /api/orders/{order_id}/items/{item_id}/scan

拍照识别。上传图片，YOLO 自动计数并更新该菜品行。

**Body** `multipart/form-data`

| key | value |
|-----|-------|
| `image` | 图片文件 (PNG/JPEG) |

**Response** `200`

```json
{
  "detected_count": 20,
  "confidence_avg": 0.894
}
```

---

## 管理员接口

### GET /api/admin/users

用户列表。

**Response** `200`

```json
[
  {
    "id": 1,
    "username": "admin",
    "real_name": "张经理",
    "role": "admin",
    "role_id": 1,
    "status": 1,
    "created_at": "2026-06-30T12:00:00"
  }
]
```

---

### POST /api/admin/users

新增用户。

**Body**

```json
{
  "username": "waiter02",
  "password": "pass1234",
  "role_id": 2,
  "real_name": "小王"
}
```

| 字段 | 说明 |
|------|------|
| `username` | 唯一，不可后续修改 |
| `password` | 最少 4 位 |
| `role_id` | `1`=admin `2`=waiter |
| `real_name` | 可选 |

**Response** `200`

```json
{ "id": 3, "username": "waiter02" }
```

| 状态码 | 说明 |
|:------:|------|
| `200` | 成功 |
| `400` | 用户名已存在 / 参数校验失败 |

---

### PUT /api/admin/users/{user_id}

修改名称或密码。**不提供用户名修改**。

**Body**

```json
{
  "real_name": "大李",
  "password": "newpass123"
}
```

两个字段均可选，传哪个改哪个。密码传空字符串不生效。

**Response** `200`

```json
{ "status": "ok" }
```

| 状态码 | 说明 |
|:------:|------|
| `200` | 成功 |
| `404` | 用户不存在 |

---

### PUT /api/admin/skewers/{skewer_id}/price

调价。历史订单价格不受影响（`order_items.unit_price` 已快照）。

**Body**

```json
{ "price": 3.50 }
```

**Response** `200`

```json
{ "status": "ok" }
```

---

### GET /api/admin/reports/skewers

各品种销量排行。

**Query**

| 参数 | 类型 | 说明 |
|------|------|------|
| `date` | string | 可选，格式 `YYYY-MM-DD`，默认今天 |

**Response** `200`

```json
[
  {
    "sale_date": "2026-06-30",
    "skewer_name": "牛肉串",
    "total_count": 150,
    "total_amount": 450.00
  }
]
```

---

### GET /api/admin/reports/tables

各桌营业额。

**Query**

| 参数 | 类型 | 说明 |
|------|------|------|
| `date` | string | 可选，格式 `YYYY-MM-DD`，默认今天 |

**Response** `200`

```json
[
  {
    "sale_date": "2026-06-30",
    "zone_name": "大厅",
    "table_code": "A01",
    "order_count": 3,
    "total_skewers": 88,
    "total_amount": 260.00
  }
]
```

---

## 完整流程示例

```bash
# 1. 登录
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"waiter01","password":"123456"}' | jq -r .token)

H="Authorization: Bearer $TOKEN"

# 2. 看桌况
curl -s -H "$H" http://localhost:8000/api/tables | jq

# 3. 看菜单
curl -s -H "$H" http://localhost:8000/api/menu/skewers | jq

# 4. 开单（选 A01 桌）
ORDER=$(curl -s -X POST http://localhost:8000/api/orders \
  -H "Content-Type: application/json" -H "$H" \
  -d '{"table_id":1}')
ORDER_ID=$(echo $ORDER | jq -r .id)

# 5. 加菜品「牛肉串」
ITEM=$(curl -s -X POST http://localhost:8000/api/orders/$ORDER_ID/items \
  -H "Content-Type: application/json" -H "$H" \
  -d '{"skewer_type_id":1}')
ITEM_ID=$(echo $ITEM | jq -r .id)

# 6. 拍照识别
curl -s -X POST http://localhost:8000/api/orders/$ORDER_ID/items/$ITEM_ID/scan \
  -H "$H" \
  -F "image=@photo.jpg" | jq

# 7. 修改数量
curl -s -X PUT http://localhost:8000/api/orders/$ORDER_ID/items/$ITEM_ID \
  -H "Content-Type: application/json" -H "$H" \
  -d '{"count":18}' | jq

# 8. 结账
curl -s -X POST http://localhost:8000/api/orders/$ORDER_ID/close -H "$H" | jq
```
