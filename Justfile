check: typecheck lint

typecheck:
	pyright

lint:
	black --check *.py
