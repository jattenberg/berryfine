#!/bin/bash

PG_UN=$(op item get render_postgres --vault nba_app --fields username)\
     PG_PW=$(op item get render_postgres --vault nba_app --fields password)\
     PG_URL=$(op item get render_postgres --vault nba_app --fields server)\
     PG_DB=$(op item get render_postgres --vault nba_app --fields database)\
     venv/bin/alembic revision -m "initialize postgres db" --autogenerate
