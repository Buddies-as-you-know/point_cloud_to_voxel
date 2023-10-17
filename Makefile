.PHONY: run
build:
	docker build -t my-python-app .
run:
	docker build -t my-python-app .
	docker-compose run my-python-app