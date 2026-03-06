# Automation Tests

Testes automatizados de formulários, links e botões usando **Playwright** e **Pytest**.

## Instalação

```bash
git clone https://github.com/luiztomiati/automation-tests.git
cd automation-tests
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install

pytest
pytest -k nome

conftest.py
test_arquivo.py
requirements.txt
screenshot/

Observações

Prints são capturados apenas em falhas.
```
