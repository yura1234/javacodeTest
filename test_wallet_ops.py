import requests


def test_invalid_wallet():
    response = requests.get("http://127.0.0.1:8000/api/v1/wallets/b8ce64bc-968c-4104-9e6e-8b3fb10b0092")
    assert response.status_code == 404
    assert response.json() == {
                    "error_code": "WALLET_NOT_FOUND",
                    "msg": "Wallet not exist in database",
                    "input": {
                        "wallet_uuid": "b8ce64bc-968c-4104-9e6e-8b3fb10b0092"
                    }
                }

def test_get_zero_total():
    response = requests.get("http://127.0.0.1:8000/api/v1/wallets/b8ce64bc-968c-4104-9e6e-8b3fb10b0093")
    assert response.status_code == 200
    assert response.json() == {"Total": 0}

def test_add_zero_total():
    response = requests.post("http://127.0.0.1:8000/api/v1/wallets/b8ce64bc-968c-4104-9e6e-8b3fb10b0093/operation",
        json=
        {
            "operationType": "DEPOSIT",
            "amount": 0
        },
    )
    assert response.status_code == 400
    assert response.json() == {
                "error_code": "AMOUNT_BELOW_ZERO",
                "msg": "Amount of operation can't be below zero",
                "input": {
                    "wallet_uuid": "b8ce64bc-968c-4104-9e6e-8b3fb10b0093",
                    "amount": 0
                }
            }

def test_add_to_wallet():
    response = requests.post("http://127.0.0.1:8000/api/v1/wallets/b8ce64bc-968c-4104-9e6e-8b3fb10b0093/operation",
        json=
        {
            "operationType": "DEPOSIT",
            "amount": 100
        }
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Wallet was succesfull DEPOSIT"}

def test_withdrow_from_wallet():
    response = requests.post("http://127.0.0.1:8000/api/v1/wallets/b8ce64bc-968c-4104-9e6e-8b3fb10b0093/operation",
        json=
        {
            "operationType": "WITHDRAW",
            "amount": 100
        }
    )
    assert response.status_code == 200
    assert response.json() == {"msg": "Wallet was succesfull WITHDRAW"}
