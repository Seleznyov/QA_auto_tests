pipenv shell

pipenv sync
pipenv install

python api/run.py

pytest --alluredir=./my_allure_results
allure serve ./my_allure_results


pytest
pytest -v
pytest test_users.py
pytest test_users.py -v
pytest -k us -v
pytest -m my_unregistered_mark
pytest -v -m my_unregistered_mark
pytest -v -m custom_marker
pytest --markers
"""