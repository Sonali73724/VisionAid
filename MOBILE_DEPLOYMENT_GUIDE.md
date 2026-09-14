# VisionAid Mobile App & Cloud Backend Deployment Guide

This guide explains how to run and deploy the **VisionAid** mobile application and AI backend server.

---

## Architecture Summary

- **VisionAid Server (`server.py`)**: Runs the heavy AI models (**YOLO11**, **EasyOCR**, **FaceAnalyzer**) using **FastAPI** on your PC or cloud server.
- **VisionAid Mobile App (`mobile_app.py`)**: Lightweight client app (~15 MB) containing the **Lilac & Pink** mobile UI, language selection, authentication, and spatial audio radar. Has **zero heavy PyTorch dependencies** on the mobile device.
- **Automated Android APK Build (`buildozer.spec` & `.github/workflows/build_apk.yml`)**: Compiles the Android `.apk` for free via GitHub Actions.

---

## 1. Running Locally (Testing on Your Computer)

### Step 1: Start the AI Server
Open a terminal and run:
```powershell
.venv\Scripts\python.exe server.py
```
*The server will start on `http://127.0.0.1:8000` with YOLO11, EasyOCR, and FaceAnalyzer loaded.*

### Step 2: Start the Mobile Client
Open a second terminal and run:
```powershell
.venv\Scripts\python.exe mobile_app.py
```
*The mobile app window will open in portrait mobile aspect ratio (420x780), stream camera frames to the local server, and provide real-time audio guidance.*

---

## 2. Connecting Your Android Phone to Your PC (Over WiFi)

If your PC and Android phone are connected to the same WiFi router:
1. Find your PC's local IP address:
   ```powershell
   ipconfig
   ```
   *(Look for `IPv4 Address`, e.g., `192.168.1.15`)*
2. In the VisionAid Mobile App on your phone:
   - Tap **SETTINGS** (top-right pill).
   - Change Server URL to `http://192.168.1.15:8000`.
   - Your phone will now stream camera frames to your PC and receive real-time guidance!

---

## 3. Connecting Over the Internet (Anywhere in the World)

### Option A: Free ngrok Tunnel (Easiest - 2 minutes)
1. Download [ngrok](https://ngrok.com/) (free).
2. Run your server on your PC:
   ```powershell
   .venv\Scripts\python.exe server.py
   ```
3. In another terminal, expose port 8000:
   ```powershell
   ngrok http 8000
   ```
4. ngrok will give you a public URL (e.g. `https://a1b2-c3d4.ngrok-free.app`).
5. In your mobile app settings, set Server URL to that ngrok address. Anyone with the APK anywhere in the world can now use your app!

### Option B: Free Cloud Hosting (Render / Hugging Face Spaces)
You can deploy `server.py` to:
- **Render.com** (Free Web Service)
- **Hugging Face Spaces** (Free Docker / Python Space)

---

## 4. Building the Android APK (Free via GitHub Actions)

We have already configured `.github/workflows/build_apk.yml` and `buildozer.spec` in this project!

To get your downloadable `.apk` file:
1. Create a GitHub repository and push your project:
   ```bash
   git init
   git add .
   git commit -m "Add VisionAid Mobile App and AI Server"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/VisionAid.git
   git push -u origin main
   ```
2. Go to your repository on GitHub.
3. Click on the **Actions** tab.
4. You will see the **Build VisionAid Android APK** workflow running.
5. Once completed (~10-15 minutes), click on the workflow run.
6. Under **Artifacts**, download `VisionAid-Mobile-APK` (which contains your installable `VisionAid-1.0.0-arm64-v8a_armeabi-v7a-debug.apk`).
7. Transfer the `.apk` to your phone via WhatsApp or Google Drive and tap **Install**!
