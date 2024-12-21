check: typecheck check_style

typecheck:
	pyright

check_style:
	black --check src

format:
	black src
