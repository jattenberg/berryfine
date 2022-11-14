# berryfine
### underpinnings:
- fastapi
- strawberry
- sqlalchemy
- [render](dashboard.render.com)
- [strawberry-sqlalchemy-mapper](https://github.com/expedock/strawberry-sqlalchemy-mapper)
- next.js
- [nba_api](https://github.com/swar/nba_api)
- [openblocks](https://github.com/openblocks-dev/openblocks)

and maybe some others. 

also considering NBA data from [balldontlie](https://www.balldontlie.io/#get-all-players) because who doesn't love Rasheed?


## GIST:
1. enable postgres db
2. find useful dataset
3. define sqlalchemy Models
4. alembic schema changes
5. strawberry mappings


## Usage:

```
# makes the virtualenv in ./venv
./scripts/build.sh

# inits the alembic stuff
venv/bin/alembic init alembic

# make the appropriate database migration, auto-genned
# for the sqlalchamy models
# note that this uses onepassword (op) to manage local secrets
./scripts/init_alembic.sh

# commit changes to remote postgres
./scripts/init_postgres.sh


```
### Revert DB Migration
At this point, you can revert the migrations using, for instance:
```
PG_UN=$(op item get render_postgres --vault nba_app --fields username)\
     PG_PW=$(op item get render_postgres --vault nba_app --fields password)\
     PG_URL=$(op item get render_postgres --vault nba_app --fields server)\
     PG_DB=$(op item get render_postgres --vault nba_app --fields database)\
     venv/bin/alembic downgrade -1
```



# TODO:
1. secret management for cloud
