import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, SessionLocal
from app import models, auth

client = TestClient(app)

@pytest.fixture(autouse=True)
def prepare_db():
    init_db()
    # очищаем после каждого теста
    yield
    db = SessionLocal()
    for tbl in (models.BMIRecord, models.Profile, models.User):
        db.query(tbl).delete()
    db.commit()
    db.close()

def test_register_and_login():
    resp = client.post("/auth/register", json={"username":"u","email":"u@e","password":"pass"})
    assert resp.status_code == 200
    token = client.post("/auth/login", json={"username":"u","password":"pass"})
    assert token.status_code == 200
    assert "access_token" in token.json()

def test_calc_bmi_requires_auth():
    r = client.post("/bmi/calculate", json={"weight":70,"height":1.75})
    assert r.status_code == 401

def test_full_bmi_flow():
    client.post("/auth/register", json={"username":"u","email":"u@e","password":"pass"})
    login = client.post("/auth/login", json={"username":"u","password":"pass"}).json()
    headers = {"Authorization": f"Bearer {login['access_token']}"}
    # расчёт и сохранение
    rec = client.post("/records/", json={"weight":80,"height":1.8}, headers=headers).json()
    assert rec["bmi"] == pytest.approx(80/1.8**2)
    # список
    lst = client.get("/records/", headers=headers).json()
    assert len(lst) == 1
    # получение по id
    got = client.get(f"/records/{rec['id']}", headers=headers).json()
    assert got["id"] == rec["id"]
    # обновление
    updated = client.put(f"/records/{rec['id']}", json={"weight":60,"height":1.8}, headers=headers).json()
    assert updated["bmi"] == pytest.approx(60/1.8**2)
    # удаление
    assert client.delete(f"/records/{rec['id']}", headers=headers).status_code == 204