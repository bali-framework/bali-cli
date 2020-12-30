test:
	coverage run -m pytest -v
env:
	python3 -m venv venv
	. venv/bin/activate \
	&& pip3 install -r requirements.txt \
	&& pip3 install wheel \
	&& pip3 install coverage pytest pre-commit \
	&& pre-commit install
