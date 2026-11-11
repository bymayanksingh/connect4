.PHONY: help install dev-install test run cli benchmark clean lint format

VENV ?= .venv
PYTHON ?= $(shell if [ -f $(VENV)/bin/python ]; then echo $(VENV)/bin/python; else echo python3; fi)
BIN = $(VENV)/bin

help:
	@echo "Connect 4 Developer Commands:"
	@echo "  make install       Install production dependencies"
	@echo "  make dev-install   Install dev and test dependencies"
	@echo "  make test          Run full automated pytest test suite"
	@echo "  make run           Launch graphical Pygame application"
	@echo "  make cli           Launch terminal interactive game"
	@echo "  make benchmark     Run headless AI tournament benchmark"
	@echo "  make sweep         Run MDP parameter sweep for DP Agent"
	@echo "  make clean         Remove build, cache, and test artifacts"

install:
	$(PYTHON) -m pip install -r requirements.txt

dev-install:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-dev.txt

test:
	$(PYTHON) -m pytest -v

run:
	$(PYTHON) game.py

cli:
	$(PYTHON) -m connect4

benchmark:
	$(PYTHON) -m connect4 --benchmark --ai1 hard --ai2 easy -n 5

sweep:
	$(PYTHON) scripts/param_sweep.py

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
