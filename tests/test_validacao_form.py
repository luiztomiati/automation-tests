import re, pytest, time
from playwright.sync_api import Page,expect

@pytest.mark.parametrize("url_fixture", ["site_url", "certificado_url"])
def test_nome_invalido(page: Page, request, url_fixture):
   url = request.getfixturevalue(url_fixture)
   page.goto(url)
   camp_tel = page.locator('input[name="pessoa.nome"]')
   camp_tel.press_sequentially("123456", delay=100)
   page.click('body') 
   mensagem = page.locator('span[name="validationMessage"]').filter(has_text=re.compile(r"\w"))
   quantidade = mensagem.count()
   assert quantidade > 0, f"ERRO: Não foi exibido mensagem de erro quando colocado um nome com apenas numeros"


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
def test_masc_telefone(page: Page, request, url_fixture):
    url = request.getfixturevalue(url_fixture)
    page.goto(url)
    camp_tel = page.locator('input[name="pessoa.telefonePrincipal"]')
    camp_tel.fill("99999999999")
    page.click('body')
    time.sleep(1)
    valor = camp_tel.input_value()

    assert re.match(r"\(\d{2}\) \d{5}-\d{4}", valor)


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
def test_campos_obrigatorios(page: Page, request, url_fixture):
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
def test_exibe_mensagem_erro(page: Page, request, url_fixture):
   url = request.getfixturevalue(url_fixture)
   page.goto(url)
   nome = page.locator('input[name="pessoa.nome"]')
   email = page.locator('input[name="pessoa.emailPrincipal"]')
   telefone = page.locator('input[name="pessoa.telefonePrincipal"]')

   nome.press_sequentially('Teste', delay=200)
   email.press_sequentially('teste@', delay=200)
   telefone.press_sequentially('(99) 99999', delay=200)
   mensagem = page.locator('span[name="validationMessage"]').filter(has_text=re.compile(r"\w"))
   quantidade = mensagem.count()

   if quantidade > 0:
      nome.fill('teste')
      telefone.fill('(99) 99999-9999')
      email.fill('teste@teste.com')
      page.click('body')
      quantidade = mensagem.count()
      assert quantidade == 0, "Erro: Mensagem de erro persiste mesmo após campos corretos."
   else:
      assert False, "Erro: Mensagens de erro não foram exibidas."