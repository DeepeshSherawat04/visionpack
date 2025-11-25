import pytest
from pathlib import Path
import importlib.util

DASHBOARD_PATH = Path("src/dashboard/app.py")


def test_dashboard_file_exists():
    assert DASHBOARD_PATH.exists(), "Dashboard file not found at src/dashboard/app.py"


def test_dashboard_imports_without_errors():
    """
    Smoke test: ensure the dashboard imports successfully.
    We do NOT run AppTest here because Streamlit apps often
    depend on external API calls, models, threads, or timeouts.
    """
    spec = importlib.util.spec_from_file_location("dashboard_app", str(DASHBOARD_PATH))
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"Dashboard import failed with exception: {e}")
