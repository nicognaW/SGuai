# SGuai

## Basic Usage

```python
import asyncio
import time

from sguai import SG, SCREEN_TIMEOUT_30s, TEXT_EFFECT_FIXED


async def main():
    s = SG()
    await s.connect("2E:80:92:XX:XX:XX")
    await s.set_screen_timeout(SCREEN_TIMEOUT_30s)
    await s.set_text_animation(TEXT_EFFECT_FIXED)
    while True:
        await s.draw_text("%.4f" % (time.time() % 1000))

asyncio.run(main())
```

## Demos

1. Duty time countdown

```shell
python ./dutytime_countdown.py
```

[video demo](https://youtube.com/shorts/_W35yWU2yoM?feature=share)
