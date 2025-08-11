#!/bin/sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
while IFS= read -r line; do
  # Skip empty lines and comments
  if [[ -z "$line" || "$line" =~ ^# ]]; then
    continue
  fi
  export "$line"
done < .env
uvicorn app.main:app --reload