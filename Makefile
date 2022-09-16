# Simple makefile to simplify repetitive build env management tasks under posix

CODESPELL_DIRS ?= ./pyaedt
CODESPELL_SKIP ?= "*.pyc,*.xml,*.txt,*.gif,*.png,*.jpg,*.js,*.html,*.doctree,*.ttf,*.woff,*.woff2,*.eot,*.mp4,*.inv,*.pickle,*.ipynb,flycheck*,./.git/*,./.hypothesis/*,*.yml,./docs/build/*,./docs/images/*,./dist/*,*~,.hypothesis*,./docs/source/examples/*,*cover,*.dat,*.mac,\#*,PKG-INFO,*.mypy_cache/*,*.xml,*.aedt,*.svg"
CODESPELL_IGNORE ?= "ignore_words.txt"

all: doctest flake8

doctest: codespell

codespell:
	@echo "Running codespell"
	@codespell $(CODESPELL_DIRS) -S $(CODESPELL_SKIP) # -I $(CODESPELL_IGNORE)

flake8:
	@echo "Running flake8"
	@flake8 .

docker-pull:
	@pip install docker
	@bash .ci/pull_syc_image.sh

unittest:
	@echo "Running unit tests (including coverage)"
	@pip install -r requirements/requirements_test.txt
	@pytest -v --cov=ansys.systemcoupling --cov-report html:cov_html --cov-config=.coveragerc
