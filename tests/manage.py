import pytest

@manager.command
def test():
    """Runs the tests."""
    pytest.main(["-s", "non-hc-api/tests"])
