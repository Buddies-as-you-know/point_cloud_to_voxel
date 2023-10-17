.PHONY: run
build:
	docker-compose up --build
run:
	docker-compose up --build
	docker-compose run my-python-app