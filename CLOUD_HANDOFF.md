# ESP32-DIV personal fork: cloud handoff

Repository: https://github.com/nicholasmagner/ESP32-DIV
Working branch: codex/personalized-startup
Hardware: ESP32-DIV v2 / ESP32-S3. User currently flashes upstream 1.7.2 via website.

Implemented:
- Approved sparse dotted skull bites dynamite while nodding downward, then
  disperses into particles. Ten exact approved GIF frames, 2,060 ms, plays once.
- User's Liberty artwork replaces only the static Cifertech logo area in color.
- Source artwork, deterministic conversion, pixel round-trip verification, and
  GitHub Actions asset checks are included. Preserve approved artwork.

Validation so far: asset pixels/timing/padding/color packing verified, generated
C++ asset file passes host syntax check. This is NOT a full ESP32 firmware build.
No device has been flashed or hardware-tested.

Next work: provision Arduino CLI with ESP32 core 2.0.10 and required libraries,
apply bundled TFT_eSPI configuration for v2 and Libraries/platform.txt, compile
baseline and modified firmware, resolve build setup issues without upgrading the
core blindly, and produce a flashable build plus recovery instructions. Verify
color byte order and placement on real hardware before release. Do not alter RF
features as part of the startup branding task.

The upstream contribution instructions list libraries that are not all bundled.
Do not claim the toolchain is complete without compiling. For asset-only setup:

    python3 -m pip install -r tools/startup-requirements.txt
    python3 tools/check_startup_assets.py

User also wants to fix occasional app crashes later; no reproducible app/steps or
serial trace supplied yet. Collect those when a crash occurs.
