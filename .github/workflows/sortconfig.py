name: Sort variables

on:
  push:
    paths:
      - 'config.py'

jobs:
  sort-vars:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install black

      - name: Sort config.py variables
        run: |
          awk '/^#|^$/{print;next} {print | "sort"}' config.py > sorted_config.py
          mv sorted_config.py config.py

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add config.py
          git commit -m "Sorted variables in config.py"
          git push