# Personalized startup

The approved 100 × 120 monochrome animation plays once for 2,060 ms, then the
Liberty artwork replaces the 150 × 150 Cifertech bitmap area. Liberty retains its
aspect ratio, is centered on black, and uses RGB565 color. Existing startup text,
version, and serial credits remain. The generic loading animation is unchanged.

Both assets are embedded in flash; no SD card or network is needed. The new pixel
payload is 60,600 bytes (15,600 animation + 45,000 logo), plus small metadata.

Sources:
- `skull.gif`: user-approved generated animation; preserve exact pixels and timing.
- `liberty.png`: artwork supplied by the user.

Regenerate and verify from the repository root:

```sh
python3 -m pip install -r tools/startup-requirements.txt
python3 tools/generate_startup_assets.py
python3 tools/check_startup_assets.py
```

Generated files are committed, so building firmware does not require Python.
Full ESP32-S3 compilation and real-device testing are still required before
calling the firmware flash-ready. See CONTRIBUTING.md for the upstream Arduino
2.0.10 core and board settings. Its platform.txt path is stale: the file is actually
`Libraries/platform.txt`. Configure TFT_eSPI using `Libraries/User_Setup v2.h`.
