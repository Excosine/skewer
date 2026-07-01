-- ============================================================
-- 竹签识别计价系统 — 数据库设计
-- 开发环境：SQLite  |  线上环境：PostgreSQL
-- BCNF 验证通过，8 张表
-- ============================================================

-- ============================================================
-- 1. 角色表
-- ============================================================
CREATE TABLE roles (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32) NOT NULL UNIQUE             -- admin / waiter
);

INSERT INTO roles (name) VALUES ('admin'), ('waiter');

-- ============================================================
-- 2. 用户表（管理员 + 服务员）
-- ============================================================
CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,           -- bcrypt 哈希
    role_id       INTEGER NOT NULL REFERENCES roles(id),
    real_name     VARCHAR(64) NOT NULL DEFAULT '',
    status        SMALLINT NOT NULL DEFAULT 1,     -- 1=启用 0=禁用
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password_hash, role_id, real_name) VALUES
('admin',    '$2b$12$hash', 1, '张经理'),
('waiter01', '$2b$12$hash', 2, '小李');

-- ============================================================
-- 3. 桌子区域
-- 不同区域不同加价：大厅 +0 / 包间 +10 / 露台 +5
-- 加价是固定的，不拆历史表
-- ============================================================
CREATE TABLE table_zones (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       VARCHAR(64) NOT NULL UNIQUE,        -- 区域名称
    surcharge  DECIMAL(10, 2) NOT NULL DEFAULT 0.00,  -- 区域固定加价（元）
    sort_order INTEGER NOT NULL DEFAULT 0
);

INSERT INTO table_zones (name, surcharge, sort_order) VALUES
('大厅',  0.00, 1),
('包间', 10.00, 2),
('露台',  5.00, 3);

-- ============================================================
-- 4. 桌子表
-- ============================================================
CREATE TABLE tables (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_id    INTEGER NOT NULL REFERENCES table_zones(id),
    table_code VARCHAR(16) NOT NULL UNIQUE,         -- 桌号 A01/B12
    capacity   INTEGER NOT NULL DEFAULT 4,          -- 座位数
    status     SMALLINT NOT NULL DEFAULT 0,         -- 0=空闲 1=占用 2=清洁中
    sort_order INTEGER NOT NULL DEFAULT 0
);

-- 大厅 A01-A03 包间 B01-B02 露台 C01-C02
INSERT INTO tables (zone_id, table_code, capacity, sort_order) VALUES
(1, 'A01', 4, 1), (1, 'A02', 4, 2), (1, 'A03', 6, 3),
(2, 'B01', 8, 4), (2, 'B02', 8, 5),
(3, 'C01', 4, 6), (3, 'C02', 4, 7);

-- ============================================================
-- 5. 签子类别
-- ============================================================
CREATE TABLE categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(64) NOT NULL UNIQUE                -- 肉类 / 蔬菜 / 海鲜
);

INSERT INTO categories (name) VALUES ('肉类'), ('蔬菜'), ('海鲜');

-- ============================================================
-- 6. 签子类型（菜单）
-- price 写死在表上，调价直接 UPDATE
-- 历史订单由 order_items.unit_price 快照保护，不受调价影响
-- ============================================================
CREATE TABLE skewer_types (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    name        VARCHAR(64) NOT NULL UNIQUE,        -- 菜品名称
    price       DECIMAL(10, 2) NOT NULL,            -- 当前单价（元/支）
    status      SMALLINT NOT NULL DEFAULT 1,        -- 1=在售 0=停售
    sort_order  INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO skewer_types (category_id, name, price, sort_order) VALUES
(1, '牛肉串', 3.00, 1),
(1, '羊肉串', 3.50, 2),
(2, '韭菜',   1.00, 3),
(2, '金针菇', 1.50, 4),
(3, '鱿鱼串', 4.00, 5);

-- ============================================================
-- 7. 订单表
-- zone_surcharge 存放下单时的区域加价快照，后续调区域价不影响历史
-- total_price = SUM(order_items.subtotal) + zone_surcharge
-- ============================================================
CREATE TABLE orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_no        VARCHAR(32) NOT NULL UNIQUE,     -- 订单编号（时间戳 + 桌号）
    table_id        INTEGER NOT NULL REFERENCES tables(id),
    waiter_id       INTEGER NOT NULL REFERENCES users(id),
    zone_surcharge  DECIMAL(10, 2) NOT NULL DEFAULT 0.00,  -- 区域加价快照
    total_count     INTEGER NOT NULL DEFAULT 0,      -- 签子总数
    total_price     DECIMAL(10, 2) NOT NULL DEFAULT 0.00,  -- 应付合计
    status          SMALLINT NOT NULL DEFAULT 0,     -- 0=进行中 1=已结账
    paid_at         TIMESTAMP,                       -- 结账时间
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 8. 订单明细表
-- 同一订单同一种签子只有一条记录，count 可修改
-- unit_price 是下单时快照，后续调价不影响此记录
-- ============================================================
CREATE TABLE order_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    skewer_type_id  INTEGER NOT NULL REFERENCES skewer_types(id),
    count           INTEGER NOT NULL,                -- 最终确认数量
    unit_price      DECIMAL(10, 2) NOT NULL,         -- 下单时单价快照
    subtotal        DECIMAL(10, 2) NOT NULL,         -- count × unit_price
    created_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (order_id, skewer_type_id)
);

-- ============================================================
-- 索引
-- ============================================================
CREATE INDEX idx_orders_table  ON orders(table_id, status);
CREATE INDEX idx_orders_waiter ON orders(waiter_id, created_at);


-- ============================================================
-- 视图（开发 SQLite / 上线 PostgreSQL）
-- 日期函数差异：SQLite 用 DATE('now')，PostgreSQL 用 CURRENT_DATE
-- ============================================================

-- ----------------------------------------------------------
-- v_tables_status  桌况一览（服务员端 + 管理端共用）
-- ----------------------------------------------------------
CREATE VIEW v_tables_status AS
SELECT tz.name           AS zone_name,
       tz.surcharge      AS zone_surcharge,
       t.table_code,
       t.capacity,
       t.status          AS table_status,
       o.id              AS order_id,
       o.order_no,
       o.total_count,
       o.total_price,
       o.created_at      AS order_created_at,
       w.real_name       AS waiter_name
FROM tables t
JOIN table_zones tz ON tz.id = t.zone_id
LEFT JOIN orders o ON o.table_id = t.id AND o.status = 0
LEFT JOIN users  w ON w.id = o.waiter_id
ORDER BY tz.sort_order, t.sort_order;

-- ----------------------------------------------------------
-- v_menu  当前可售菜单（服务员端选菜用）
-- ----------------------------------------------------------
CREATE VIEW v_menu AS
SELECT st.id,
       st.name         AS skewer_name,
       c.name          AS category_name,
       st.price        AS unit_price,
       st.sort_order
FROM skewer_types st
JOIN categories c ON c.id = st.category_id
WHERE st.status = 1
ORDER BY c.id, st.sort_order;

-- ----------------------------------------------------------
-- v_order_detail  订单明细（结账打印 / 订单详情）
-- ----------------------------------------------------------
CREATE VIEW v_order_detail AS
SELECT o.id            AS order_id,
       o.order_no,
       t.table_code,
       tz.name         AS zone_name,
       o.zone_surcharge,
       o.total_count,
       o.total_price,
       o.status        AS order_status,
       o.paid_at,
       oi.id           AS item_id,
       st.name         AS skewer_name,
       oi.count,
       oi.unit_price,
       oi.subtotal
FROM orders o
JOIN tables t       ON t.id = o.table_id
JOIN table_zones tz ON tz.id = t.zone_id
JOIN order_items oi ON oi.order_id = o.id
JOIN skewer_types st ON st.id = oi.skewer_type_id;

-- ----------------------------------------------------------
-- v_daily_skewer_sales  今日品种销量排行（管理端报表）
-- PostgreSQL: 将 DATE('now') 替换为 CURRENT_DATE
-- ----------------------------------------------------------
CREATE VIEW v_daily_skewer_sales AS
SELECT DATE(o.paid_at)     AS sale_date,
       st.name             AS skewer_name,
       SUM(oi.count)       AS total_count,
       SUM(oi.subtotal)    AS total_amount
FROM orders o
JOIN order_items oi  ON oi.order_id = o.id
JOIN skewer_types st ON st.id = oi.skewer_type_id
WHERE o.status = 1
GROUP BY DATE(o.paid_at), st.name
ORDER BY sale_date DESC, total_amount DESC;

-- ----------------------------------------------------------
-- v_daily_table_sales  今日各桌营业额（管理端报表）
-- PostgreSQL: 将 DATE('now') 替换为 CURRENT_DATE
-- ----------------------------------------------------------
CREATE VIEW v_daily_table_sales AS
SELECT DATE(o.paid_at)     AS sale_date,
       tz.name             AS zone_name,
       t.table_code,
       COUNT(DISTINCT o.id) AS order_count,
       SUM(o.total_count)   AS total_skewers,
       SUM(o.total_price)   AS total_amount
FROM orders o
JOIN tables t       ON t.id = o.table_id
JOIN table_zones tz ON tz.id = t.zone_id
WHERE o.status = 1
GROUP BY DATE(o.paid_at), tz.name, t.table_code
ORDER BY sale_date DESC, total_amount DESC;


-- ============================================================
-- 视图查询示例（对照上面视图直接 SELECT）
-- ============================================================

-- 桌况一览
-- SELECT * FROM v_tables_status;

-- 选菜列表
-- SELECT * FROM v_menu;

-- 某桌账单打印
-- SELECT table_code, skewer_name, count, unit_price, subtotal
-- FROM v_order_detail WHERE order_id = ?;

-- 今日品种销量前十
-- SELECT * FROM v_daily_skewer_sales
-- WHERE sale_date = DATE('now') LIMIT 10;

-- 今日各桌营业额
-- SELECT * FROM v_daily_table_sales
-- WHERE sale_date = DATE('now');

-- 调价
-- UPDATE skewer_types SET price = 3.50, updated_at = CURRENT_TIMESTAMP WHERE name = '牛肉串';


-- ============================================================
-- 计价逻辑（参考，由应用层实现）
-- ============================================================
-- 开单：
--   zone_surcharge = table.zone.surcharge   # 快照
-- 加菜品：
--   unit_price = skewer_type.price           # 快照
--   subtotal   = count × unit_price
-- 结账：
--   total_count = SUM(order_items.count)
--   total_price = SUM(order_items.subtotal) + zone_surcharge
--   table.status → 清洁中
