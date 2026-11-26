VENV=.venv
PY=$(VENV)/bin/python

.PHONY: setup build test proof reference clean

setup:
	python3 -m venv $(VENV)
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -e .

build:
	$(PY) -m computerfont.build

test:
	$(PY) -m pytest -q

proof:
	$(PY) -m computerfont.proof

reference:
	bash scripts/fetch_reference.sh

clean:
	rm -rf build fonts sources/generated proofs
