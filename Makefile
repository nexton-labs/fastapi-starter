start:
	poetry run honcho start -f Procfile.dev

console:
	poetry run ipython -i ipython.py

test:
	poetry run python -m pytest -v tests

lint:
	poetry run python -m black . --check
	poetry run python -m pylint -j 0 app tests
	poetry run python -m flake8 app tests
	poetry run python -m mypy app tests

test-all:
	$(MAKE) test
	$(MAKE) lint

migrate:
	poetry run alembic upgrade head

gen_migration:
	poetry run alembic revision --autogenerate -m "$(m)"

undo_migration:
	poetry run alembic downgrade -1
