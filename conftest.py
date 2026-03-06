import pytest
import os

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if item.get_closest_marker("no_screenshot"):
        return
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)

        if page:
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path=f"screenshots/erro_{item.name}.png")

@pytest.fixture
def certificado_url():
    return "https://qualidade.apprbs.com.br/certificacao"

@pytest.fixture
def site_url():
    return "https://qualidade.apprbs.com.br/site"
