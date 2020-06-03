export DB_HOST?=127.0.0.1
export DB_PASS?=admin123
export DB_USER?=admin123
export DB_NAME?=risk
export DB_PORT?=3306

run:
	python app.py

dev-run:
	adev runserver .

test:
	pytest -vv
