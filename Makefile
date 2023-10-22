.PHONY: run
build:
	docker-compose up --build
run:
	docker-compose up --build
	docker-compose run my-python-app

# Makefile
check:
	docker-compose build my-python-app
	docker-compose run --rm my-python-app sh -c "flake8 && black --check . && mypy"
