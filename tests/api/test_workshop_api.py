def test_post_car_returns_201_and_json(client):
    payload = {
        "make": "Ford",
        "model": "Fiesta",
        "year": 2018,
        "color": "Black",
}
    response = client.post("/api/cars", json=payload)

    assert response.status_code == 201
    car = response.json()
    assert car["id"] > 0
    assert car["make"] == "Ford"
    assert car["model"] == "Fiesta"
    assert response.headers["location"] == f"/api/cars/{car['id']}"

def test_invalid_year_is_not_saved(client):
    # 1. 发送一个 year=1800 的非法数据（其他字段都合法）
    payload = {
        "make": "Toyota",
        "model": "Yaris",
        "year": 1800,
        "color": "Blue",
    }
    response = client.post("/api/cars", json=payload)

        # 2. 断言被验证层拒绝，返回 422 Unprocessable Entity
    assert response.status_code == 422

    # 3. 再查一次列表，确认这辆车没有被写入数据库
    response = client.get("/api/cars")
    assert response.status_code == 200
    assert response.json() == []