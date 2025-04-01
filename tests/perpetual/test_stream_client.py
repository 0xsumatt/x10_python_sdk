<<<<<<< HEAD
import pytest
import websockets
from hamcrest import assert_that, equal_to
from websockets import WebSocketServer


def get_url_from_server(server: WebSocketServer):
    host, port = server.sockets[0].getsockname()  # type: ignore[index]
    return f"ws://{host}:{port}"


def serve_message(message):
    async def _serve_message(websocket):
        await websocket.send(message)

    return _serve_message


@pytest.mark.asyncio
async def test_orderbook_stream(create_orderbook_message):
=======
import asyncio
import pytest
import uvloop
from hamcrest import assert_that, equal_to
from picows import ws_create_server, WSListener, WSUpgradeRequest

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class TestWSServer:
    def __init__(self, host="127.0.0.1", port=0):
        self.host = host
        self.port = port
        self.server = None
        self.message = None

    async def start(self, message):
        self.message = message

        def listener_factory(request: WSUpgradeRequest):
            return MessageSender(self.message)

        self.server = await ws_create_server(listener_factory, self.host, self.port)

        # Get the actual port assigned
        self.port = self.server.sockets[0].getsockname()[1]

    async def stop(self):
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    def get_url(self):
        return f"ws://{self.host}:{self.port}"


class MessageSender(WSListener):
    def __init__(self, message):
        self.message = message

    def on_ws_connected(self, transport):
        transport.send(1, self.message.encode("utf8"))


@pytest.fixture
async def ws_server():
    server = TestWSServer()
    yield server
    await server.stop()


@pytest.mark.asyncio
async def test_orderbook_stream(create_orderbook_message, ws_server):
>>>>>>> change-to-ruff
    from x10.perpetual.stream_client import PerpetualStreamClient

    message_model = create_orderbook_message()

<<<<<<< HEAD
    async with websockets.serve(serve_message(message_model.model_dump_json()), "127.0.0.1", 0) as server:
        stream_client = PerpetualStreamClient(api_url=get_url_from_server(server))
        stream = await stream_client.subscribe_to_orderbooks()
        msg = await stream.recv()
        await stream.close()

        assert_that(
            msg.to_api_request_json(),
            equal_to(
                {
                    "type": "SNAPSHOT",
                    "data": {
                        "m": message_model.data.market,
                        "b": [{"q": "0.008", "p": "43547.00"}, {"q": "0.007000", "p": "43548.00"}],
                        "a": [{"q": "0.008", "p": "43546.00"}],
                    },
                    "error": None,
                    "ts": 1704798222748,
                    "seq": 570,
                }
            ),
        )


@pytest.mark.asyncio
async def test_account_update_trade_stream(create_account_update_trade_message):
=======
    # Start server with the message
    await ws_server.start(message_model.model_dump_json())

    # Create client and connect
    stream_client = PerpetualStreamClient(api_url=ws_server.get_url())
    stream = await stream_client.subscribe_to_orderbooks()
    msg = await stream.recv()
    await stream.close()

    assert_that(
        msg.to_api_request_json(),
        equal_to(
            {
                "type": "SNAPSHOT",
                "data": {
                    "m": message_model.data.market,
                    "b": [
                        {"q": "0.008", "p": "43547.00"},
                        {"q": "0.007000", "p": "43548.00"},
                    ],
                    "a": [{"q": "0.008", "p": "43546.00"}],
                },
                "error": None,
                "ts": 1704798222748,
                "seq": 570,
            }
        ),
    )


@pytest.mark.asyncio
async def test_account_update_trade_stream(
    create_account_update_trade_message, ws_server
):
>>>>>>> change-to-ruff
    from x10.perpetual.stream_client import PerpetualStreamClient

    api_key = "dummy_api_key"
    message_model = create_account_update_trade_message()

<<<<<<< HEAD
    async with websockets.serve(serve_message(message_model.model_dump_json()), "127.0.0.1", 0) as server:
        stream_client = PerpetualStreamClient(api_url=get_url_from_server(server))
        stream = await stream_client.subscribe_to_account_updates(api_key)
        msg = await stream.recv()
        await stream.close()

        assert_that(
            msg.to_api_request_json(),
            equal_to(
                {
                    "type": "TRADE",
                    "data": {
                        "orders": None,
                        "positions": None,
                        "trades": [
                            {
                                "id": 1811328331296018432,
                                "accountId": 3004,
                                "market": "BTC-USD",
                                "orderId": 1811328331287359488,
                                "side": "BUY",
                                "price": "58249.8000000000000000",
                                "qty": "0.0010000000000000",
                                "value": "58.2498000000000000",
                                "fee": "0.0291240000000000",
                                "isTaker": True,
                                "tradeType": "TRADE",
                                "createdTime": 1720689301691,
                            }
                        ],
                        "balance": None,
                    },
                    "error": None,
                    "ts": 1704798222748,
                    "seq": 570,
                }
            ),
        )


@pytest.mark.asyncio
async def test_account_update_stream_with_unexpected_type(create_account_update_unknown_message):
=======
    # Start server with the message
    await ws_server.start(message_model.model_dump_json())

    # Create client and connect
    stream_client = PerpetualStreamClient(api_url=ws_server.get_url())
    stream = await stream_client.subscribe_to_account_updates(api_key)
    msg = await stream.recv()
    await stream.close()

    assert_that(
        msg.to_api_request_json(),
        equal_to(
            {
                "type": "TRADE",
                "data": {
                    "orders": None,
                    "positions": None,
                    "trades": [
                        {
                            "id": 1811328331296018432,
                            "accountId": 3004,
                            "market": "BTC-USD",
                            "orderId": 1811328331287359488,
                            "side": "BUY",
                            "price": "58249.8000000000000000",
                            "qty": "0.0010000000000000",
                            "value": "58.2498000000000000",
                            "fee": "0.0291240000000000",
                            "isTaker": True,
                            "tradeType": "TRADE",
                            "createdTime": 1720689301691,
                        }
                    ],
                    "balance": None,
                },
                "error": None,
                "ts": 1704798222748,
                "seq": 570,
            }
        ),
    )


@pytest.mark.asyncio
async def test_account_update_stream_with_unexpected_type(
    create_account_update_unknown_message, ws_server
):
>>>>>>> change-to-ruff
    from x10.perpetual.stream_client import PerpetualStreamClient

    api_key = "dummy_api_key"
    message_model = create_account_update_unknown_message()

<<<<<<< HEAD
    async with websockets.serve(serve_message(message_model.model_dump_json()), "127.0.0.1", 0) as server:
        stream_client = PerpetualStreamClient(api_url=get_url_from_server(server))
        stream = await stream_client.subscribe_to_account_updates(api_key)
        msg = await stream.recv()
        await stream.close()

        assert_that(
            msg.to_api_request_json(),
            equal_to(
                {
                    "type": "UNKNOWN",
                    "data": None,
                    "error": None,
                    "ts": 1704798222748,
                    "seq": 570,
                }
            ),
        )


@pytest.mark.asyncio
async def test_candle_stream():
=======
    # Start server with the message
    await ws_server.start(message_model.model_dump_json())

    # Create client and connect
    stream_client = PerpetualStreamClient(api_url=ws_server.get_url())
    stream = await stream_client.subscribe_to_account_updates(api_key)
    msg = await stream.recv()
    await stream.close()

    assert_that(
        msg.to_api_request_json(),
        equal_to(
            {
                "type": "UNKNOWN",
                "data": None,
                "error": None,
                "ts": 1704798222748,
                "seq": 570,
            }
        ),
    )


@pytest.mark.asyncio
async def test_candle_stream(ws_server):
>>>>>>> change-to-ruff
    from tests.fixtures.candles import create_candle_stream_message
    from x10.perpetual.stream_client import PerpetualStreamClient

    message_model = create_candle_stream_message()

<<<<<<< HEAD
    async with websockets.serve(serve_message(message_model.model_dump_json()), "127.0.0.1", 0) as server:
        stream_client = PerpetualStreamClient(api_url=get_url_from_server(server))
        stream = await stream_client.subscribe_to_candles("ETH-USD", "trades", "PT1M")
        msg = await stream.recv()
        await stream.close()

        assert_that(
            msg.to_api_request_json(),
            equal_to(
                {
                    "type": None,
                    "data": [
                        {
                            "o": "3458.64",
                            "l": "3399.07",
                            "h": "3476.89",
                            "c": "3414.85",
                            "v": "3.938",
                            "T": 1721106000000,
                        }
                    ],
                    "error": None,
                    "ts": 1721283121979,
                    "seq": 1,
                }
            ),
        )
=======
    # Start server with the message
    await ws_server.start(message_model.model_dump_json())

    # Create client and connect
    stream_client = PerpetualStreamClient(api_url=ws_server.get_url())
    stream = await stream_client.subscribe_to_candles("ETH-USD", "trades", "PT1M")
    msg = await stream.recv()
    await stream.close()

    assert_that(
        msg.to_api_request_json(),
        equal_to(
            {
                "type": None,
                "data": [
                    {
                        "o": "3458.64",
                        "l": "3399.07",
                        "h": "3476.89",
                        "c": "3414.85",
                        "v": "3.938",
                        "T": 1721106000000,
                    }
                ],
                "error": None,
                "ts": 1721283121979,
                "seq": 1,
            }
        ),
    )
>>>>>>> change-to-ruff
