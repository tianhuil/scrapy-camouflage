SHELL := /bin/bash

create:
	python3 -m venv env

install:
	source env/bin/activate && pip3 install -r requirements.txt

pylint:
	source env/bin/activate && pylint scrapy_camouflage
