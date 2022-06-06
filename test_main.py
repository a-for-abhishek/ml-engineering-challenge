import json
from fastapi.testclient import TestClient
from auth import AuthHandler
from main import app

client = TestClient(app)

auth_handler = AuthHandler()

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Linear Regression API!"}


def test_stream():
    # data = {"input": 0.52}
    token, _ = auth_handler.encode_token('abi')
    response = client.post("/stream/", headers={"Authorization": "Bearer " + str(token)}, json={"input": 0.52})
    output = json.loads(response.text)
    assert output['result'] == "640.2571140419432"
    assert response.status_code == 200