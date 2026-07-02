# FaceOnLive — ID Liveness Detection SDK for Linux

Server-side **ID document liveness / spoof detection** for Linux, exposed through a Python interface with ready-to-run **Flask** and **Gradio** demos. Determines whether a presented ID is a genuine physical card or a spoof (screen capture, printed copy, or photocopy).

> Part of the [FaceOnLive](https://faceonlive.com) on-premises biometric SDK suite.

## Features
- Detect screen-replay, print, and photocopy ID spoofing.
- On-premises and offline; REST (Flask) and web-UI (Gradio) demos included.
- Online (env-var key) and offline (`license.txt`) activation.

## Requirements
| | |
|---|---|
| OS | Linux x86-64 |
| Runtime | Python 3.8+ |
| Engine | native ID-liveness engine (included) |

## Setup
1. Get a license key — free trial at **https://faceonlive.com**.
2. Provide the key via the `LICENSE_KEY` environment variable (online) or `license.txt` (offline).
3. Install requirements, then run a demo:
   ```bash
   python flask/app.py      # REST API
   python gradio/app.py     # web UI
   ```

## Quick start (Python)
```python
import os
from engine.header import *

# Online activation from an environment variable
set_activation(os.environ["LICENSE_KEY"].encode("utf-8"))   # setLicenseKey
init_sdk()                                                   # initSDK
```

## API reference (Python bindings → native)
| Binding | Native | Description |
|---|---|---|
| `get_deviceid()` | `getHWID` | Machine hardware ID (for offline licensing). |
| `set_activation(key)` | `setLicenseKey` | Activate the SDK. |
| `init_sdk()` | `initSDK` | Initialize the engine. |

## License & support
Requires a valid license key — get one at **[faceonlive.com](https://faceonlive.com)**. Keep `license.txt` out of version control. Questions: contact@faceonlive.com

## 📦 Full SDK download
This repository contains the source/demo code only. Download the complete SDK — engine libraries and models, with full project structure — from the [Releases](../../releases) page and extract it over this project.
