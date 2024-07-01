PY_DIRS=pagetree
VE ?= ./ve
REQUIREMENTS ?= test_reqs.txt
SYS_PYTHON ?= python3
PY_SENTINAL ?= $(VE)/sentinal
WHEEL_VERSION ?= 0.43.0
PIP_VERSION ?= 24.1.1
MAX_COMPLEXITY ?= 8
PY_DIRS ?= $(APP)
DJANGO ?= "Django==4.2.13"

FLAKE8 ?= $(VE)/bin/flake8
PIP ?= $(VE)/bin/pip
JS_FILES=pagetree/static/pagetree/js/src

all: flake8 eslint

include *.mk

clean:
	rm -rf $(VE)
	find . -name '*.pyc' -exec rm {} \;
	rm -rf node_modules

$(PY_SENTINAL):
	rm -rf $(VE)
	$(SYS_PYTHON) -m venv $(VE)
	$(PIP) install pip==$(PIP_VERSION)
	$(PIP) install --upgrade setuptools
	$(PIP) install wheel==$(WHEEL_VERSION)
	$(PIP) install --requirement $(REQUIREMENTS) --no-binary cryptography
	$(PIP) install "$(DJANGO)"
	touch $@

flake8: $(PY_SENTINAL)
	$(FLAKE8) $(PY_DIRS) --max-complexity=$(MAX_COMPLEXITY)

.PHONY: flake8 test eslint clean
