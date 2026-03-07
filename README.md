# Automation Tests

Testes automatizados de formulários, links e botões usando **Playwright** e **Pytest**.

## Cobertura dos testes

Os testes automatizados verificam:

- campos obrigatórios do formulário
- formato válido de e-mail
- máscara do telefone
- exibição correta de mensagens de erro
- envio do formulário para a API
- verificação de links da página

## Instalação

```
git clone https://github.com/luiztomiati/automation-tests.git
cd automation-tests
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install
```
## Tecnologias Utilizadas
- Python
- Playwright
- Pytest

## Executar Teste

```bash
pytest
pytest -k nome
```

## Estrutura
<pre>
  .
  ├── tests
  │   ├── test_envio_form.py
  │   ├── test_links.py
  │   └── test_validacao_form.py
  ├── conftest.py
  ├── pytest.ini
  ├── requirements.txt
  ├── README.md
  └── .gitignore
</pre>
## Observações

Prints são capturados apenas em falhas.
