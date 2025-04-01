from types import TracebackType
<<<<<<< HEAD
from typing import AsyncIterator, Generic, Optional, Type, TypeVar

import websockets
from websockets import WebSocketClientProtocol

=======
from typing import AsyncIterator, Generic, Optional, Type, TypeVar, List
import asyncio
from picows import ws_connect, WSListener, WSTransport, WSFrame, WSMsgType
>>>>>>> change-to-ruff
from x10.config import USER_AGENT
from x10.utils.http import RequestHeader
from x10.utils.log import get_logger
from x10.utils.model import X10BaseModel

LOGGER = get_logger(__name__)

StreamMsgResponseType = TypeVar("StreamMsgResponseType", bound=X10BaseModel)

<<<<<<< HEAD
=======
class X10WSListener(WSListener):
    def __init__(self, msg_queue: asyncio.Queue):
        self.msg_queue = msg_queue
        
    def on_ws_connected(self, transport: WSTransport):
        LOGGER.debug("Connected to stream: %s", transport.request.path)
        
    def on_ws_disconnected(self, transport: WSTransport):
        LOGGER.debug("Stream closed: %s", transport.request.path)
        self.msg_queue.put_nowait(None)
        
    def on_ws_frame(self, transport: WSTransport, frame: WSFrame):
        if frame.msg_type == WSMsgType.TEXT:
            payload = frame.get_payload_as_utf8_text()
            self.msg_queue.put_nowait(payload)

>>>>>>> change-to-ruff

class PerpetualStreamConnection(Generic[StreamMsgResponseType]):
    __stream_url: str
    __msg_model_class: Type[StreamMsgResponseType]
    __api_key: Optional[str]
    __msgs_count: int
<<<<<<< HEAD
    __websocket: Optional[WebSocketClientProtocol]

=======
    __transport: Optional[WSTransport]
    __listener: Optional[X10WSListener]
    __msg_queue: asyncio.Queue
    
>>>>>>> change-to-ruff
    def __init__(
        self,
        stream_url: str,
        msg_model_class: Type[StreamMsgResponseType],
        api_key: Optional[str],
    ):
        super().__init__()
<<<<<<< HEAD

=======
>>>>>>> change-to-ruff
        self.__stream_url = stream_url
        self.__msg_model_class = msg_model_class
        self.__api_key = api_key
        self.__msgs_count = 0
<<<<<<< HEAD
        self.__websocket = None

    async def send(self, data):
        await self.__websocket.send(data)

    async def recv(self) -> StreamMsgResponseType:
        return await self.__receive()

    async def close(self):
        assert self.__websocket is not None
        assert not self.__websocket.closed

        await self.__websocket.close()

        LOGGER.debug("Stream closed: %s", self.__stream_url)

    @property
    def msgs_count(self):
        return self.__msgs_count

    @property
    def closed(self):
        assert self.__websocket is not None

        return self.__websocket.closed

    def __aiter__(self) -> AsyncIterator[StreamMsgResponseType]:
        return self

    async def __anext__(self) -> StreamMsgResponseType:
        assert self.__websocket is not None

        if self.__websocket.closed:
            raise StopAsyncIteration

        return await self.__receive()

    async def __receive(self) -> StreamMsgResponseType:
        assert self.__websocket is not None

        data = await self.__websocket.recv()
        self.__msgs_count += 1

        return self.__msg_model_class.model_validate_json(data)

    def __await__(self):
        return self.__await_impl__().__await__()

    async def __aenter__(self):
        # Calls `self.__await__()` implicitly
        return await self

=======
        self.__transport = None
        self.__listener = None
        self.__msg_queue = asyncio.Queue()
        
    async def send(self, data):
        assert self.__transport is not None
        self.__transport.send(WSMsgType.TEXT, data)
        
    async def recv(self) -> StreamMsgResponseType:
        return await self.__receive()
        
    async def close(self):
        assert self.__transport is not None
        self.__transport.disconnect(graceful=True)
        await self.__transport.wait_disconnected()
        LOGGER.debug("Stream closed: %s", self.__stream_url)
        
    @property
    def msgs_count(self):
        return self.__msgs_count
        
    @property
    def closed(self):
        if self.__transport is None:
            return True
        return self.__transport.underlying_transport.is_closing()
        
    def __aiter__(self) -> AsyncIterator[StreamMsgResponseType]:
        return self
        
    async def __anext__(self) -> StreamMsgResponseType:
        if self.closed:
            raise StopAsyncIteration
        return await self.__receive()
        
    async def __receive(self) -> StreamMsgResponseType:
        data = await self.__msg_queue.get()
        if data is None: 
            raise StopAsyncIteration
        self.__msgs_count += 1
        return self.__msg_model_class.model_validate_json(data)
        
    def __await__(self):
        return self.__await_impl__().__await__()
        
    async def __aenter__(self):
        return await self
        
>>>>>>> change-to-ruff
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ):
        await self.close()
<<<<<<< HEAD

=======
        
>>>>>>> change-to-ruff
    async def __await_impl__(self):
        extra_headers = {
            RequestHeader.USER_AGENT.value: USER_AGENT,
        }
<<<<<<< HEAD

        if self.__api_key is not None:
            extra_headers[RequestHeader.API_KEY.value] = self.__api_key

        self.__websocket = await websockets.connect(self.__stream_url, extra_headers=extra_headers)

        LOGGER.debug("Connected to stream: %s", self.__stream_url)

        return self
=======
        if self.__api_key is not None:
            extra_headers[RequestHeader.API_KEY.value] = self.__api_key
            
        def create_listener():
            self.__listener = X10WSListener(self.__msg_queue)
            return self.__listener
            
        # Connect to WebSocket
        self.__transport, _ = await ws_connect(
            create_listener,
            self.__stream_url,
            extra_headers=extra_headers,
            enable_auto_ping=True,
            enable_auto_pong=True
        )
        
        LOGGER.debug("Connected to stream: %s", self.__stream_url)
        return self
>>>>>>> change-to-ruff
