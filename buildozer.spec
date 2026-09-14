[app]

# (str) Title of your application
title = VisionAid

# (str) Package name
package.name = visionaid

# (str) Package domain (needed for android/ios packaging)
package.domain = org.visionaid

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,json

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, .venv, .git, .github, scratch, backend, __pycache__

# (list) List of exclusions using pattern matching
source.exclude_patterns = *.pt, *.zip, vision_app*.py, *test*.py, *.txt, server.py

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,requests,pillow,certifi

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = CAMERA, RECORD_AUDIO, INTERNET, ACCESS_NETWORK_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android SDK
android.skip_update = False

# (bool) If True, then accept all SDK licenses
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (str) Presplash of the application
# android.presplash_color = #1A0F28

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icons/icon_status.png

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
