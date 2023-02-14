import binascii
import bleak

SCREEN_TIMEOUT_NONE = 0
SCREEN_TIMEOUT_30s = 1
SCREEN_TIMEOUT_1m = 2
SCREEN_TIMEOUT_2m = 3
SCREEN_TIMEOUT_5m = 4

TEXT_EFFECT_FIXED = 0
TEXT_EFFECT_MARQUEE_LEFT = 1
TEXT_EFFECT_MARQUEE_RIGHT = 2
TEXT_EFFECT_TWINKLE = 3

UNIT_CELSIUS = 0
UNIT_FAHRENHEIT = 1


class SG:

    protocol_prefix = [0xff, 0x55]
    supported_devices = ['SGUAI-C3']
    char = "0000ff01-0000-1000-8000-00805f9b34fb"

    def __init__(self):
        self.bc = None

    @classmethod
    async def discover(cls):
        devices = []
        for d in await bleak.BleakScanner.discover(timeout=30.0):
            print(d, d.name)
            if d.name in cls.supported_devices:
                devices.append(d.address)
        return devices

    async def connect(self, address=None):
        if not address:
            addresses = await self.discover()
            if len(addresses):
                print(f"found addresses: {addresses}")
                address = addresses[0]
        assert address is not None
        self.bc = bleak.BleakClient(address, timeout=float('INF'))
        await self.bc.connect()

    async def send_raw(self, data):
        return await self.bc.write_gatt_char(self.char, data, True)

    async def send_cmd(self, cmd, *args, direction=2):
        payload = self.protocol_prefix + [0x6 + len(args), 0x0, direction, cmd] + list(args)
        return await self.send_raw(bytearray(payload))

    async def send_raw_hex(self, hex_data):
        return await self.send_raw(binascii.unhexlify(hex_data))

    async def set_temp_unit(self, unit):
        return await self.send_cmd(0xB, unit)

    async def draw_text(self, text):
        args = []
        for char in text:
            args += [(ord(char) >> 8) & 0xff, ord(char) & 0xff]
        return await self.send_cmd(0x17, 1, *args)

    async def set_text_animation(self, anim):
        return await self.send_cmd(0x23, anim)

    async def set_animation_speed(self, anim_speed):  # 设置动态速度, 0-100
        return await self.send_cmd(0x24, anim_speed)

    async def draw_bitmap(self, bitmap):
        return await self.send_cmd(0x25, *bitmap)

    async def draw_anim_bitmap(self, bitmaps):
        for idx, bitmap in enumerate(bitmaps):
            await self.send_cmd(0x26, idx, *bitmap)
        return await self.send_cmd(0x26, len(bitmaps))

    async def set_screen_timeout(self, screen_timeout_tier):  # 设置自动熄屏时长
        return await self.send_cmd(0x27, screen_timeout_tier)
