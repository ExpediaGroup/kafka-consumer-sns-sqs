.DEFAULT_GOAL := build 

clean :
	pipenv --rm

install :
	pipenv install --dev --skip-lock 

test :
	pipenv run pytest tests --verbose

style :
	pipenv run black kafka_consumer --check

.PHONY: build
build :
	pipenv lock --requirements > requirements.txt
	pipenv install --dev
	pipenv run pipenv-setup sync
	pipenv check
