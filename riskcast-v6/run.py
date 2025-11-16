import subprocess
import sys
import os

if __name__ == "__main__":
    # Ensure we're running from the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py"])