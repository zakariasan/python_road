install:
    uv sync

run:
    uv run python -m src \
        --functions_definition data/input/functions_definition.json \
        --input data/input/function_calling_tests.json \
        --output data/output/function_calls.json

debug:
    uv run python -m pdb -m src

clean:
    rm -rf __pycache__ .mypy_cache src/__pycache__

lint:
    uv run flake8 .
    uv run mypy . --warn-return-any --warn-unused-ignores \
        --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
    uv run flake8 .
    uv run mypy . --strict
