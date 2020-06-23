export DB_HOST?=127.0.0.1
export DB_PASS?=risk123
export DB_USER?=risk123
export DB_NAME?=risk
export DB_PORT?=3306

run:
	python app.py

test:
	pytest -vv

build: 
	docker build \
		--build-arg DB_HOST=${DB_HOST} \
		--build-arg DB_PORT=${DB_PORT} \
		--build-arg DB_NAME=${DB_NAME} \
		--build-arg DB_PASS=${DB_PASS} \
		--build-arg DB_USER=${DB_USER} \
		-t board-api-dev \
		.
	docker run -d \
		-it \
		--name dev-board \
		--mount type=bind,source="$(shell pwd)"/board,target=/app \
		--network=host \
		board-api-dev

dev-run:
	adev runserver board/.

make install: install-test
	pip install -r requirements

make install-test:
	pip install -r requirements-test
