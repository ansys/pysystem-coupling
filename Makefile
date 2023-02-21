# Makefile to simplify repetitive build env management tasks under posix

docker-pull:
	@python -m pip install docker
	@bash .ci/pull_syc_image.sh

build-install:
	@python -m pip install .[build]
	@python -m build
	@python -m pip install -q --force-reinstall dist/*.whl

test-import:
	@python -c "import ansys.systemcoupling.core as pysystemcoupling"

generate-api:
	@echo "Generate API classes"
	@python -m venv env_generate
	@. env_generate/bin/activate
	@python -m pip install -e .
	@python -m pip install .[classesgen]
	@python scripts/generate_datamodel.py
	@rm -rf env_generate
