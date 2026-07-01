"""Integration tests for skewer-counting API."""

import os, sys, bcrypt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

TEST_DB = os.path.join(os.path.dirname(__file__), "..", "runtime", "test.db")

# remove old test db
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)

# both seed and server need to use test.db
os.environ["DB_PATH"] = TEST_DB

from db import init_db, get_session, close_db
init_db(TEST_DB)

from server import app
from fastapi.testclient import TestClient

client = TestClient(app)


def _set_password(username: str, password: str):
    db = get_session()
    from db.models import User
    u = db.query(User).filter(User.username == username).first()
    u.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    db.commit()


_set_password("admin", "123456")
_set_password("waiter01", "123456")


def _auth(token: str):
    return {"Authorization": f"Bearer {token}"}


# ── tests ─────────────────────────────────────

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "skewer-counter"


def test_login_wrong_password():
    r = client.post("/api/auth/login", json={"username": "waiter01", "password": "wrong"})
    assert r.status_code == 401


def test_login_and_auth():
    r = client.post("/api/auth/login", json={"username": "waiter01", "password": "123456"})
    assert r.status_code == 200
    data = r.json()
    assert "token" in data
    assert data["role"] == "waiter"
    return data["token"]


def test_me():
    token = test_login_and_auth()
    r = client.get("/api/auth/me", headers=_auth(token))
    assert r.status_code == 200
    assert r.json()["role"] == "waiter"


def test_tables():
    token = test_login_and_auth()
    r = client.get("/api/tables", headers=_auth(token))
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 7


def test_menu():
    token = test_login_and_auth()
    r = client.get("/api/menu/skewers", headers=_auth(token))
    assert r.status_code == 200
    assert len(r.json()) == 20


def test_order_lifecycle():
    token = test_login_and_auth()
    hdrs = _auth(token)

    r = client.post("/api/orders", json={"table_id": 1}, headers=hdrs)
    assert r.status_code == 200
    order_id = r.json()["id"]

    r = client.post(f"/api/orders/{order_id}/items", json={"skewer_type_id": 1}, headers=hdrs)
    assert r.status_code == 200
    item_id = r.json()["id"]

    r = client.put(f"/api/orders/{order_id}/items/{item_id}", json={"count": 20}, headers=hdrs)
    assert r.status_code == 200

    r = client.get(f"/api/orders/{order_id}", headers=hdrs)
    assert r.status_code == 200
    assert r.json()["items"][0]["count"] == 20

    r = client.post(f"/api/orders/{order_id}/close", headers=hdrs)
    assert r.status_code == 200

    r = client.get(f"/api/orders/{order_id}", headers=hdrs)
    assert r.json()["status"] == 1
    assert r.json()["total_price"] == 60.0


def test_admin_access_denied():
    token = test_login_and_auth()
    r = client.get("/api/admin/reports/skewers", headers=_auth(token))
    assert r.status_code == 403


def test_admin_reports():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "123456"})
    token = r.json()["token"]
    hdrs = _auth(token)

    r = client.get("/api/admin/reports/skewers", headers=hdrs)
    assert r.status_code == 200

    r = client.get("/api/admin/reports/tables", headers=hdrs)
    assert r.status_code == 200


def test_admin_update_price():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "123456"})
    token = r.json()["token"]
    hdrs = _auth(token)

    r = client.put("/api/admin/skewers/1/price", json={"price": 3.50}, headers=hdrs)
    assert r.status_code == 200

    r = client.get("/api/menu/skewers", headers=hdrs)
    prices = {item["id"]: item["unit_price"] for item in r.json()}
    assert prices[1] == 3.5


def test_admin_user_create():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "123456"})
    token = r.json()["token"]
    hdrs = _auth(token)

    r = client.post("/api/admin/users", json={
        "username": "waiter02",
        "password": "pass1234",
        "role_id": 2,
        "real_name": "小王",
    }, headers=hdrs)
    assert r.status_code == 200
    assert r.json()["username"] == "waiter02"

    # duplicate should fail
    r = client.post("/api/admin/users", json={
        "username": "waiter02",
        "password": "pass1234",
        "role_id": 2,
    }, headers=hdrs)
    assert r.status_code == 400


def test_admin_user_list():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "123456"})
    token = r.json()["token"]
    hdrs = _auth(token)

    r = client.get("/api/admin/users", headers=hdrs)
    assert r.status_code == 200
    assert len(r.json()) >= 2


def test_admin_user_update():
    r = client.post("/api/auth/login", json={"username": "admin", "password": "123456"})
    token = r.json()["token"]
    hdrs = _auth(token)

    # update name and password
    r = client.put("/api/admin/users/2", json={
        "real_name": "大李",
        "password": "newpass123",
    }, headers=hdrs)
    assert r.status_code == 200

    # login with old password should fail
    r = client.post("/api/auth/login", json={"username": "waiter01", "password": "123456"})
    assert r.status_code == 401

    # login with new password should work
    r = client.post("/api/auth/login", json={"username": "waiter01", "password": "newpass123"})
    assert r.status_code == 200
    assert r.json()["real_name"] == "大李"

    # update only name, password unchanged
    r = client.put("/api/admin/users/2", json={"real_name": "小李"}, headers=hdrs)
    r = client.post("/api/auth/login", json={"username": "waiter01", "password": "newpass123"})
    assert r.status_code == 200
    assert r.json()["real_name"] == "小李"

    # username cannot be changed (no field in body)
    # waiter cannot access admin endpoints
    waiter_token = r.json()["token"]
    r = client.get("/api/admin/users", headers=_auth(waiter_token))
    assert r.status_code == 403


# ── runner ────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_root,
        test_login_wrong_password,
        test_me,
        test_tables,
        test_menu,
        test_order_lifecycle,
        test_admin_access_denied,
        test_admin_reports,
        test_admin_update_price,
        test_admin_user_create,
        test_admin_user_list,
        test_admin_user_update,
    ]
    for t in tests:
        name = t.__name__
        try:
            t()
            print(f"  PASS  {name}")
        except Exception as e:
            print(f"  FAIL  {name}: {e}")

    close_db()
    try:
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
    except PermissionError:
        pass
