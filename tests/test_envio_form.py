import pytest
from playwright.sync_api import Page,expect

@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_inscricao_form(page: Page, request, url_fixture):
    url = request.getfixturevalue(url_fixture)
    page.goto(url)

    page.locator('input[name="pessoa.nome"]').press_sequentially('Teste', delay=100)
    page.locator('input[name="pessoa.emailPrincipal"]').press_sequentially('teste@teste.com', delay=100)
    page.locator('input[name="pessoa.telefonePrincipal"]').press_sequentially('(99) 99999-9999', delay=100)

    button = page.locator('#rbBtnNext')
    expect(button).to_be_enabled()
    with page.expect_response(lambda r: "sendData" in r.url) as response_info:
        button.click(force=True)
    response = response_info.value
    assert response.status == 200 , (
    f"ERRO: Falha ao enviar formulário.\n"
    f"Status: {response.status}\n"
    f"URL: {response.url}\n"
    f"Resposta: {response.text()}"
)
    toast = page.locator(".rbToasterError")
    expect(toast).not_to_be_visible()

      
      
