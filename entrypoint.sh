#!/bin/bash
cd /wasd/
sleep 1
alembic upgrade head
sleep 1
python3 main.py
