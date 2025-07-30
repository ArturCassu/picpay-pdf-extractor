#!/usr/bin/env bash
PYTHONPATH=$(pwd) uvicorn app.main:app --host 0.0.0.0 --port 8000