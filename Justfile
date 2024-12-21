check: typecheck check_style

typecheck:
	pyright

check_style:
	black --check src

build: check
	pyproject-build

format:
	black src

clean:
	rm -rf dist
