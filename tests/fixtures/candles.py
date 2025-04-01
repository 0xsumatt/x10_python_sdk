from typing import List

from x10.perpetual.candles import CandleModel
from x10.utils.http import WrappedStreamResponse


def create_candle_stream_message():
    return WrappedStreamResponse[List[CandleModel]](
        data=[
            CandleModel(
<<<<<<< HEAD
                open="3458.64", low="3399.07", high="3476.89", close="3414.85", volume="3.938", timestamp=1721106000000
=======
                open="3458.64",
                low="3399.07",
                high="3476.89",
                close="3414.85",
                volume="3.938",
                timestamp=1721106000000,
>>>>>>> change-to-ruff
            )
        ],
        ts=1721283121979,
        seq=1,
    )
