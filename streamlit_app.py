"""
AcousticShield 2.0 • Streamlit Community Cloud Canonical Entrypoint
Delegates execution directly to app.py
"""
import os
import sys
import runpy

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

APP_PATH = os.path.join(ROOT_DIR, "app.py")
runpy.run_path(APP_PATH, run_name="__main__")
