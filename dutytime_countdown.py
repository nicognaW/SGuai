from sguai import SG, TEXT_EFFECT_FIXED, SCREEN_TIMEOUT_5m
from datetime import datetime
import asyncio

def get_countdown() -> str:
    now = datetime.now()
    target = datetime.combine(now, datetime.strptime("18:00:00", "%H:%M:%S").time())
    delta = target - now

    if delta.days >= 0:
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    else:
        return "-1:-1:-1"

async def main():
    address = None
    s = SG()
    addresses = await s.discover()
    if len(addresses):
        print(f"found addresses: {addresses}")
        address = addresses[0]
    while True:
        try:
            await s.connect(address)
            #    await s.connect()
            await s.set_screen_timeout(SCREEN_TIMEOUT_5m)
            await s.set_text_animation(TEXT_EFFECT_FIXED)
            while True:
                await asyncio.sleep(0.3)
                # await s.draw_text("%.4f" % (time.time() % 1000))
                await s.draw_text(get_countdown())
        except Exception as e:
            print(e)
            print("retrying")
            pass


asyncio.run(main())
