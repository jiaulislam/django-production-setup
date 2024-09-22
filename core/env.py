from pathlib import Path
import environ

__all__ = ["env", "BASE_DIR"]

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent