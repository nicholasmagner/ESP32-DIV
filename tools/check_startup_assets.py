#!/usr/bin/env python3
"""Round-trip embedded pixels against the approved source artwork."""
import re
from pathlib import Path
from PIL import Image, ImageOps, ImageSequence

root = Path(__file__).resolve().parents[1]
s = (root / 'ESP32-DIV/StartupAssets.cpp').read_text()
def values(name):
    m = re.search(r'\b' + name + r'\[\].*?=\s*\{(.*?)\};', s, re.S)
    assert m, name
    return [int(v, 16) for v in re.findall(r'0x([0-9a-f]+)', m[1])]
source = Image.open(root / 'assets/startup/skull.gif')
durations = []
for i, frame in enumerate(ImageSequence.Iterator(source)):
    durations.append(frame.info['duration'])
    data = values(f'skullFrame{i}')
    assert len(data) == 1560
    original = frame.convert('L')
    for y in range(120):
        assert data[y*13+12] & 15 == 0, 'row padding must stay zero'
        for x in range(100):
            actual = bool(data[y*13+x//8] & (128 >> (x % 8)))
            assert actual == (original.getpixel((x,y)) >= 128), (i,x,y)
assert len(durations) == 10 and sum(durations) == 2060
stored = re.search(r'skullDurations\[10\] = \{(.*?)\}', s)[1]
assert list(map(int, stored.split(','))) == durations
logo = Image.open(root / 'assets/startup/liberty.png').convert('RGBA')
bg = Image.new('RGBA', logo.size, (0,0,0,255)); bg.alpha_composite(logo)
logo = ImageOps.contain(bg.convert('RGB'), (150,150), Image.Resampling.LANCZOS)
canvas = Image.new('RGB', (150,150)); canvas.paste(logo, ((150-logo.width)//2,(150-logo.height)//2))
encoded = values('libertyLogo'); assert len(encoded) == 22500
for index, (r,g,b) in enumerate(canvas.getdata()):
    assert encoded[index] == ((r>>3)<<11 | (g>>2)<<5 | b>>3)
print('PASS: every animation pixel, timing, row padding and RGB565 logo pixel matches source.')
