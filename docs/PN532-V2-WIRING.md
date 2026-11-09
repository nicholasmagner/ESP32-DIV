# PN532 wiring and detection on ESP32-DIV V2

The firmware uses an **Adafruit PN532-compatible reader in SPI mode**.
RC522/MFRC522 readers are not supported by this driver. I2C and UART modes
will not respond to this firmware's software-SPI commands.

## Wiring

Disconnect USB and battery power before changing wiring. These are ESP32-S3
GPIO numbers, not connector positions. Check the board silkscreen/schematic
to locate the GPIOs; the software cannot establish a connector's orientation.

| PN532 signal | V2 connection |
| --- | --- |
| SCK / SCLK | GPIO12 |
| MISO | GPIO11 |
| MOSI | GPIO13 |
| SS / SSEL / CS | GPIO5 |
| GND | GND |
| VCC / VIN | Supply required by your specific PN532 breakout |

ESP32-S3 GPIOs use **3.3 V logic**. Do not put 5 V signals on these pins.
Use the 3.3 V supply only if your breakout supports a 3.3 V input; check its
documentation rather than assuming every board's VIN pin is equivalent.
IRQ and reset are not used by this SPI constructor.

Set the module's switches/jumpers to **SPI**, following the markings or manual
for that exact breakout, then power-cycle it. Switch positions vary by module.
Connect MISO to MISO and MOSI to MOSI as listed above, without crossing them.
The V2 SD bus uses the opposite data-pin assignment (MOSI11/MISO13), so do not
copy SD wiring for the PN532. Defaults are in `ESP32-DIV/shared.h`.

## CC1101 conflict

The default CC1101 CS is also GPIO5. Do not connect both chip selects to GPIO5:
both devices would be selected together. The reversed PN532 data wiring can
also put two outputs on one line when both modules are connected.
For an initial PN532 test, disconnect the CC1101 module with power removed.
To retain both modules, plan separate chip selects and compatible bus wiring
and override the pin definitions accordingly; this change does not invent a
new pin assignment for an unknown physical shield.

## Detection troubleshooting

1. Confirm the module actually says PN532, and confirm SPI mode.
2. Check supply, common ground, short wires, and the four GPIO connections.
3. Test with CC1101 disconnected. An SD card may remain inserted: the firmware
   releases the SD peripheral before V2 PN532 software SPI, then restores SD.
4. Open the RFID/NFC feature. `PN532 init failed` means either the firmware-version
   query or reader configuration failed; a card is not required for detection.
5. Once the reader initializes, test Card Reader with a supported 13.56 MHz
   ISO14443A card. A 125 kHz RFID tag will not work with PN532.
6. Leave RFID, verify the SD file manager still works, and reopen RFID to check
   that repeated bus handoffs work.

If detection still fails, provide a photo of the module's front/back, switch
positions, the six wire connections, and the exact on-screen message.

## Firmware change and validation limits

V2 now unmounts SD, releases hardware SPI, and resets the PN532 data GPIOs before
starting software SPI. Previously RFID changed GPIO directions while the SD
peripheral could still own those pins. Initialization also checks `SAMConfig()`
instead of treating any successful version response as a fully configured reader.
Pin defaults and personalized startup artwork remain unchanged.

A compile check does not establish detection on physical hardware. Verify the
reader, SD restoration, and repeated entry/exit on the actual V2 before relying
on the fix. Incorrect mode, module type, power, or a shared-CS hardware conflict
cannot be repaired by this software change.
