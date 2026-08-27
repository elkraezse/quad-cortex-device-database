# Quad Cortex Device Database

A community-maintained list of every device (block) on the Neural DSP Quad Cortex, with the **exact control names, ranges and defaults** as they appear in the parameter editor.

Neural DSP publishes an official [device list](https://neuraldsp.com/device-list) with names and "based on" models, and the community [Quad Cortex Wiki](https://quadcortex.wiki) documents a handful of amps, but as of August 2026 there is no complete, machine-readable reference of what controls each block actually has. This repository is that reference.

Maintained by **elkraezse**. Contributions welcome, see below.

## What's here

| Path | What it is |
|---|---|
| `data/qc_catalogue.json` | The source of truth. One entry per device. |
| `data/qc_catalogue.csv` | Flat spreadsheet-friendly export, generated. |
| `docs/devices.md` | Human-readable tables by category, generated. |
| `scripts/build_tables.py` | Regenerates the CSV and Markdown from the JSON. |

Browse the tables here: [docs/devices.md](docs/devices.md).

## Coverage

Every device from the official list is present (stock devices plus plugin devices). Controls are being added device by device from screenshots of the Cortex Control parameter editor. Each device carries a status:

- **verified**: controls transcribed from the parameter editor and checked.
- **unverified**: controls taken from the Quad Cortex Wiki and not yet checked against the device.
- **missing**: no control data yet.

The current counts are at the top of `docs/devices.md`.

## JSON fields

```
{
  "id":                  "brit_2203",             stable slug, unique
  "name":                "Brit 2203",             exact name shown on the Quad Cortex
  "category":            "Guitar amps",           category from the official device list
  "based_on":            "Marshall JCM800",       real-world reference (null for plugin devices)
  "plugin":              null,                    e.g. "Archetype: Nolly X" for plugin devices
  "added_in_coros":      "1.0.0",
  "coros_verified_on":   "4.1.0",                 CorOS version the controls were captured on
  "controls": [                                   null until verified
    {"name": "Gain", "type": "knob", "range": "0-10", "default": 5, "page": 1},
    {"name": "Bright", "type": "switch", "range": "off/on", "default": "off", "page": 1}
  ],
  "controls_unverified": ["Gain", "Bass", ...],  wiki-sourced names, kept until verified
  "pages":               2,                       number of parameter pages
  "verified":            true,
  "source":              "Cortex Control 4.1.0 screenshot",
  "notes":               null
}
```

Control `type` is one of `knob`, `switch`, `select` (multi-position), `button`, `time` (ms/note value), `bypass`.

## Contributing

Corrections and additions are welcome. The easiest way:

1. Open the device in Cortex Control (or on the Quad Cortex) and open its parameter editor.
2. Take a screenshot of **every page** of parameters, ideally at default values, with the device name visible.
3. Open an issue with the screenshots attached and the device name in the title, or edit `data/qc_catalogue.json` directly and open a pull request.

If you edit the JSON, run `python3 scripts/build_tables.py` before committing so the CSV and Markdown stay in sync.

Please only record what the device actually shows. Do not fill in controls from the real amp or pedal a block is based on; the whole point of this database is that the block and the hardware often differ.

## Licence

Data and documentation are released under [CC BY 4.0](LICENSE). Use it freely, credit "Quad Cortex Device Database (elkraezse)".

Quad Cortex, Cortex Control and CorOS are trademarks of Neural DSP Technologies. All amp and pedal names referenced are trademarks of their respective owners and are used here only to identify the device each block is modelled on. This project is not affiliated with Neural DSP.
