
import pytest

@pytest.fixture(autouse=True)
def clean_event_loop():
    yield
    # Принудительная очистка
    import asyncio
    try:
        loop = asyncio.get_running_loop()
        loop.stop()
        loop.close()
    except:
        pass