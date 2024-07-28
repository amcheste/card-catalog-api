PROGRAM = card-catalog-api
LABEL   = $(shell git rev-parse --abbrev-ref HEAD)

.PHONY: build remove-image run-docker get-shell run-local test

build:
	docker build -t $(PROGRAM):$(LABEL) .

remove-image:
	docker image rm $(PROGRAM):$(LABEL)

run-docker:
	docker run -it --rm -p 8000:8000 $(PROGRAM):$(LABEL)

get-shell:
	docker run -it --rm --entrypoint sh $(PROGRAM):$(LABEL)

run-local:
	fastapi dev app/main.py

test:
	pytest