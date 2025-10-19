# DRAGON_EYE_termux
CLI location tracking software for termux. Lightweight and fast.
<p align="center">
  <img src="https://github.com/user-attachments/assets/500b69d0-9be4-46ee-b527-4878419a6ee0" alt="DRAGON_EYE Logo" width="500"/>
  <br>
  <em>CLI location tracking software for termux. Lightweight and fast.</em>
</p>

Lightweight threaded HTTP server for logging client data and geolocation.  
Designed for Termux / Linux.

---

## Features
- Logs IP, ISP, Browser, Device, Platform, Language, Screen resolution, Timezone
- Logs geolocation: Latitude, Longitude, Accuracy
- Threaded for multiple clients
- Clean colored terminal logs
- Stores logs in `logs/client_data.json` & `logs/location_data.json`

---

## Instalation
```bash
git clone https://github.com/webdragon63/DRAGON_EYE_termux
cd DRAGON_EYE_termux
```
## Usage
```bash
python3 server.py
````

* POST `/client-data` → JSON client info
* POST `/location` → JSON location info

---

## Notes

* Default port: `8000` (change in `server.py`)

---


  # Created by
### ***INDIAN CYBER ARMY***
#### ***YT CHANNEL: [INDIAN CYBER ARMY](https://www.youtube.com/@webdragon63)***
```
