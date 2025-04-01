#!/usr/bin/env python
import asyncio
import time
import statistics
import json
import os
import sys
import websockets
from picows import ws_create_server, WSListener, WSMsgType, ws_connect
import uvloop

# Number of iterations for benchmark
ITERATIONS = 20

# Test message to send
TEST_MESSAGE = json.dumps(
    {
        "type": "SNAPSHOT",
        "data": {
            "m": "BTC-USD",
            "b": [{"q": "0.008", "p": "43547.00"}, {"q": "0.007000", "p": "43548.00"}],
            "a": [{"q": "0.008", "p": "43546.00"}],
        },
        "error": None,
        "ts": 1704798222748,
        "seq": 570,
    }
)


async def benchmark_websockets():
    """Benchmark the websockets library directly"""
    times = []

    for i in range(ITERATIONS):
        # Set up the server
        async def handler(websocket):
            await websocket.send(TEST_MESSAGE)

        # Start server on random port
        server = await websockets.serve(handler, "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        url = f"ws://127.0.0.1:{port}"

        try:
            # Time the connection, message receipt, and disconnect
            start = time.perf_counter()

            # Connect to the server
            async with websockets.connect(url) as ws:
                # Receive the message
                message = await ws.recv()

            end = time.perf_counter()
            times.append(end - start)
            print(f"websockets test {i + 1}/{ITERATIONS}: {end - start:.6f}s")

        finally:
            # Clean up the server
            server.close()
            await server.wait_closed()

    return times


async def benchmark_picows():
    """Benchmark the PicoWS library directly"""
    # Set up uvloop for PicoWS
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    times = []
    received_message = None

    for i in range(ITERATIONS):
        # Set up message receipt event
        message_received = asyncio.Event()

        # Create listener class
        class ServerListener(WSListener):
            def on_ws_connected(self, transport):
                transport.send(WSMsgType.TEXT, TEST_MESSAGE.encode("utf-8"))

        class ClientListener(WSListener):
            def on_ws_frame(self, transport, frame):
                nonlocal received_message
                if frame.msg_type == WSMsgType.TEXT:
                    received_message = frame.get_payload_as_utf8_text()
                    message_received.set()

        # Create server
        server = await ws_create_server(lambda _: ServerListener(), "127.0.0.1", 0)
        port = server.sockets[0].getsockname()[1]
        url = f"ws://127.0.0.1:{port}"

        try:
            # Time the connection, message receipt, and disconnect
            start = time.perf_counter()

            # Connect to the server
            transport, _ = await ws_connect(lambda: ClientListener(), url)

            # Wait for message to be received
            await asyncio.wait_for(message_received.wait(), timeout=5.0)

            # Disconnect
            transport.disconnect()
            await transport.wait_disconnected()

            end = time.perf_counter()
            times.append(end - start)
            print(f"PicoWS test {i + 1}/{ITERATIONS}: {end - start:.6f}s")

        finally:
            # Clean up the server
            server.close()
            await server.wait_closed()

    return times


async def main():
    print("Running WebSocket implementation benchmarks...\n")

    # Run websockets benchmark
    print("Testing websockets library:")
    ws_times = await benchmark_websockets()

    # Run PicoWS benchmark
    print("\nTesting PicoWS library:")
    picows_times = await benchmark_picows()

    # Calculate statistics
    ws_avg = statistics.mean(ws_times)
    ws_min = min(ws_times)
    ws_max = max(ws_times)

    picows_avg = statistics.mean(picows_times)
    picows_min = min(picows_times)
    picows_max = max(picows_times)

    improvement = ((ws_avg - picows_avg) / ws_avg) * 100

    # Display results
    print("\n=== BENCHMARK RESULTS ===")
    print(f"websockets:")
    print(f"  Average: {ws_avg:.6f}s")
    print(f"  Min:     {ws_min:.6f}s")
    print(f"  Max:     {ws_max:.6f}s")
    print(f"PicoWS:")
    print(f"  Average: {picows_avg:.6f}s")
    print(f"  Min:     {picows_min:.6f}s")
    print(f"  Max:     {picows_max:.6f}s")
    print(f"\nPerformance improvement: {improvement:.2f}%")
    print(f"PicoWS is {'faster' if improvement > 0 else 'slower'} than websockets")


if __name__ == "__main__":
    asyncio.run(main())
