import re, pytest
from playwright.sync_api import Page,expect

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

@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_telefone_invalido(page: Page, request, url_fixture):
   url = request.getfixturevalue(url_fixture)
   page.goto(url)
   camp_tel = page.locator('input[name="pessoa.telefonePrincipal"]')
   camp_tel.press_sequentially("aa999999999", delay=100)
   page.click('body') 
   mensagem = page.locator('span[name="validationMessage"]').filter(has_text=re.compile(r"\w"))
   quantidade = mensagem.count()
   assert quantidade > 0, f"ERRO: Não foi exibido erro quando colocado um telefone com letra no lugar do DDD."

@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_masc_telefone(page: Page,request, url_fixture ):
   url = request.getfixturevalue(url_fixture)
   page.goto(url)
   camp_tel = page.locator('input[name="pessoa.telefonePrincipal"]')
   camp_tel.press_sequentially("99999999999", delay=100)
   valor = camp_tel.input_value()
   regex = r"^\(?99\)?\s?99999-9999$"
   if not re.match(regex,valor):
      assert "Campo não possui formatação."

@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_email(page: Page,request, url_fixture):
   url = request.getfixturevalue(url_fixture)
   page.goto(url)
   email = page.locator('input[name="pessoa.emailPrincipal"]')
   email.press_sequentially("alicia-almada97bitco.cc", delay=200)
   mensagem = page.locator('span[name="validationMessage"]').filter(has_text=re.compile(r"\w"))
   page.locator("body").click()
   quantidade = mensagem.count()
   assert quantidade > 0, f"ERRO: Email invalido, a mensagem de erro não foi exibida."

@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_botao_campos_obrigatorios(page: Page, request, url_fixture):
    url = request.getfixturevalue(url_fixture)
    page.goto(url)
    button = page.locator("#rbBtnNext")
    campos = [
    'input[name="pessoa.nome"]',
    'input[name="pessoa.emailPrincipal"]',
    'input[name="pessoa.telefonePrincipal"]'
    ]
    valores = {
    'input[name="pessoa.nome"]': 'teste',
    'input[name="pessoa.emailPrincipal"]': 'teste@teste.com',
    'input[name="pessoa.telefonePrincipal"]': '(99) 99999-9999'
    }
    for seletor in campos:
     campo = page.locator(seletor)
     if campo.get_attribute("required") is not None:
      campo.fill(valores[seletor])

    expect(button).to_be_enabled()

    for seletor in campos:
     campo = page.locator(seletor)
     if campo.get_attribute("required") is not None:
      campo.fill("")
      page.click('body')

    expect(button).to_be_disabled()

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
    