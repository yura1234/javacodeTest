import uvicorn
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from sqlalchemy import select

from database.session import get_session
from database.tables import Wallet
from schemas import WalletOperationSchema as WOS
from settings import ApiSettings

app = FastAPI()


@app.post("/api/v1/wallets/{wallet_uuid}/operation")
async def post_wallet_operation(
    wallet_uuid: str,
    wallet_operation: WOS = Body()
) -> JSONResponse:
    """
    Обрабатывает POST запросы к указанному кошельку
    args:
        wallet_uuid (str) - Уникальный идентификатор кошелька
        wallet_operation (WalletOperationSchema) - Детали операции с кошельком, 
        переданные в теле запроса.
    return:
        JSONResponse: Ответ в формате JSON
    """
    if wallet_operation.amount <= 0:
        return JSONResponse(
            status_code=400,
            content={
                "error_code": "AMOUNT_BELOW_ZERO",
                "msg": "Amount of operation can't be below zero",
                "input": {
                    "wallet_uuid": wallet_uuid,
                    "amount": float(wallet_operation.amount)
                }
            }
        )
    async with get_session() as session:
        query = await session.execute(
            select(Wallet).filter(Wallet.wallet_uuid == wallet_uuid).with_for_update()
        )
        res = query.scalars().first()
        if res is None:
            return JSONResponse(
                status_code=404,
                content={
                    "error_code": "WALLET_NOT_FOUND",
                    "msg": "Wallet not exist in database",
                    "input": {
                        "wallet_uuid": wallet_uuid
                    }
                }
            )
        if wallet_operation.operationType == WOS.OperationType.DEPOSIT:
            res.total += wallet_operation.amount
        else:
            res.total -= wallet_operation.amount
            if res.total < 0:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error_code": "AMOUNT_BELOW_ZERO",
                        "msg": "Total amount of wallet below zero",
                        "input": {
                            "wallet_uuid": wallet_uuid,
                            "amount": float(wallet_operation.amount)
                        }
                    }
                )
        await session.commit()
        return JSONResponse(
            status_code=200,
            content={"msg": f"Wallet was succesfull {wallet_operation.operationType}"}
        )


@app.get("/api/v1/wallets/{wallet_uuid}")
async def get_wallet_total(wallet_uuid: str) -> JSONResponse:
    """
    Обрабатывает GET-запрос для получения баланса указанного кошелька
    args:
        wallet_uuid (str) - Уникальный идентификатор кошелька
    return:
        JSONResponse: Ответ в формате JSON
    """
    async with get_session() as session:
        query = await session.execute(
            select(Wallet).filter(Wallet.wallet_uuid == wallet_uuid)
        )
        res = query.scalars().first()
        if res is None:
            return JSONResponse(
                status_code=404,
                content={
                    "error_code": "WALLET_NOT_FOUND",
                    "msg": "Wallet not exist in database",
                    "input": {
                        "wallet_uuid": wallet_uuid
                    }
                }
            )
        return JSONResponse(
            status_code=200,
            content={"Total": float(res.total)}
        )


if __name__ == "__main__":
    from settings import get_db_url
    print(get_db_url())
    api_setting = ApiSettings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        access_log=api_setting.access_log,
        proxy_headers=api_setting.proxy_headers,
        server_header=api_setting.server_header,
        reload=True
    )
