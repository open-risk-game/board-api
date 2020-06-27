export DB_HOST?=127.0.0.1
export DB_PASS?=root
export DB_USER?=root
export DB_NAME?=tiles
export DB_PORT?=3306

run:
	python app.py

test:
	pytest -vv

build: 
	docker build -t board-api .

dev-run:
	adev runserver .

make install: install-test
	pip install -r requirements

make install-test:
	pip install -r requirements-test
