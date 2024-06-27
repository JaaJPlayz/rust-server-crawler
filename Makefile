run:
	python3 src/crawler.py

install:
	python3 -m venv .venv
	python3 -m pip install -r dev-requirements.txt

clean:
	rm -rf .venv

.PHONY: run install clean
