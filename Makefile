.PHONY: lint test build

inittest:	
	pip install flake8 pytest

lint:
	flake8

test:
	pytest -sv

initbuild:
	pip install setuptools wheel twine

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*

clean:
	rm -rf dist/ build/ .foo* .pytest* *.egg-info
	find . -name __pycache__ -exec rm -rf {} +