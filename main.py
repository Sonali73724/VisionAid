"""
VisionAid - Mobile Application Entry Point for Buildozer / Android
"""

import sys
import os
import traceback

def run():
    try:
        from mobile_app import VisionAidMobileApp
        VisionAidMobileApp().run()
    except Exception as e:
        err = traceback.format_exc()
        print("CRITICAL CRASH IN VISIONAID:", err)
        for log_dir in ["/sdcard/Download", os.path.expanduser("~"), "."]:
            try:
                with open(os.path.join(log_dir, "visionaid_crash.log"), "w", encoding="utf-8") as f:
                    f.write(err)
                break
            except Exception:
                pass
        raise

if __name__ == "__main__":
    run()