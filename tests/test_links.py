import pytest
from playwright.sync_api import Page

@pytest.mark.no_screenshot
@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_verifica_links(page: Page, request, url_fixture):
    url = request.getfixturevalue(url_fixture)
    page.goto(url)
    page.wait_for_selector("a", timeout=10000)
    links = page.locator("a").all()
    erros = []
    for i, link in enumerate(links):
        href = link.get_attribute("href")
        onclick = link.get_attribute("onclick")
        texto = link.inner_text().strip()
        role = link.get_attribute("role")
        if not href and not onclick and role != "button":
          erros.append(f"Link '{texto if texto else i}' não possui href")
          continue
        if href in ["#", "javascript:void(0)", "javascript:;"]:
          erros.append(f"Link '{texto or i}' não possui ação válida")
           
    assert not erros, "Links inoperantes encontrados:\n" + "\n".join(erros)