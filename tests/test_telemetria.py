from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API de Telemetria Energética Ativa"}


def test_create_medicao(client: TestClient) -> None:
    response = client.post(
        "/medicoes/",
        json={"maquina_id": 1, "consumo_kwh": 12.5, "status": "operando"},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["maquina_id"] == 1
    assert response.json()["consumo_kwh"] == 12.5
    assert response.json()["status"] == "operando"
    assert response.json()["data_hora"]


def test_read_medicoes(client: TestClient) -> None:
    client.post(
        "/medicoes/",
        json={"maquina_id": 1, "consumo_kwh": 12.5, "status": "operando"},
    )

    response = client.get("/medicoes/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["maquina_id"] == 1


def test_update_medicao(client: TestClient) -> None:
    created = client.post(
        "/medicoes/",
        json={"maquina_id": 1, "consumo_kwh": 12.5, "status": "operando"},
    )

    response = client.put(
        f"/medicoes/{created.json()['id']}",
        json={"maquina_id": 2, "consumo_kwh": 18.75, "status": "manutencao"},
    )

    assert response.status_code == 200
    assert response.json()["id"] == created.json()["id"]
    assert response.json()["maquina_id"] == 2
    assert response.json()["consumo_kwh"] == 18.75
    assert response.json()["status"] == "manutencao"


def test_update_medicao_not_found(client: TestClient) -> None:
    response = client.put(
        "/medicoes/999",
        json={"maquina_id": 2, "consumo_kwh": 18.75, "status": "manutencao"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Medição não encontrada"}


def test_delete_medicao(client: TestClient) -> None:
    created = client.post(
        "/medicoes/",
        json={"maquina_id": 1, "consumo_kwh": 12.5, "status": "operando"},
    )

    response = client.delete(f"/medicoes/{created.json()['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Medição removida com sucesso"}
    assert client.get("/medicoes/").json() == []


def test_delete_medicao_not_found(client: TestClient) -> None:
    response = client.delete("/medicoes/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Medição não encontrada"}


def test_get_kpis(client: TestClient) -> None:
    client.post(
        "/medicoes/",
        json={"maquina_id": 1, "consumo_kwh": 10.0, "status": "operando"},
    )
    client.post(
        "/medicoes/",
        json={"maquina_id": 2, "consumo_kwh": 20.0, "status": "manutencao"},
    )

    response = client.get("/medicoes/kpis")

    assert response.status_code == 200
    assert response.json() == {
        "consumo_total_kwh": 30.0,
        "consumo_medio_kwh": 15.0,
        "maquinas_operando": 1,
    }
