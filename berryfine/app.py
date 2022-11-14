import strawberry
from typing import Optional

from fastapi import FastAPI
from sqlalchemy import select
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from strawberry.dataloader import DataLoader

from berryfine import models


@strawberry.type
class Player:
    id: strawberry.ID
    full_name: str
    first_name: str
    last_name: str
    is_active: bool

    @classmethod
    def marshal(cls, model: models.Player) -> "Player":
        return cls(
            id=strawberry.ID(str(model.id)),
            full_name=model.full_name,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
        )


@strawberry.type
class Team:
    id: strawberry.ID
    full_name: str
    abbreviation: str
    nickname: str
    city: str
    state: str
    year_founded: int

    @classmethod
    def marshal(cls, model: models.Team) -> "Team":
        return cls(
            id=strawberry.ID(str(model.id)),
            full_name=model.full_name,
            abbreviation=model.abbreviation,
            nickname=model.nickname,
            city=model.city,
            state=model.state,
            year_founded=model.year_founded,
        )


@strawberry.type
class PlayerExists:
    message: str = "Author with this name already exist"


@strawberry.type
class PlayerNotFound:
    message: str = "Couldn't find an player with the supplied name"


@strawberry.type
class PlayerNameMissing:
    message: str = "Please supply an author name"


AddTeamResponse = strawberry.union(
    "AddBookResponse", (Team, PlayerNotFound, PlayerNameMissing)
)
AddPlayerResponse = strawberry.union("AddAuthorResponse", (Player, PlayerExists))


all_tasks: list = []


@strawberry.type
class Query:
    @strawberry.field
    async def teams(self) -> list[Team]:
        async with models.get_session() as s:
            sql = select(models.Team).order_by(models.Team.full_name)
            db_teams = (await s.execute(sql)).scalars().unique().all()
        return [Team.marshal(team) for team in db_teams]

    @strawberry.field
    async def players(self) -> list[Player]:
        async with models.get_session() as s:
            sql = select(models.Player).order_by(models.Player.full_name)
            db_players = (await s.execute(sql)).scalars().unique().all()
        return [Player.marshal(pl) for pl in db_players]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_team(
        self,
        id: strawberry.ID,
        full_name: str,
        abbreviation: str,
        nickname: str,
        city: str,
        state: str,
        year_founded: int,
    ) -> AddTeamResponse:
        async with models.get_session() as s:
            db_team = models.Team(
                id=id,
                full_name=full_name,
                abbreviation=abbreviation,
                nickname=nickname,
                city=city,
                state=state,
                year_founded=year_founded,
            )
            s.add(db_team)
            await s.commit()
        return Team.marshal(db_team)

    @strawberry.mutation
    async def add_player(
        self,
        id: strawberry.ID,
        full_name: str,
        first_name: str,
        last_name: str,
        is_active: bool,
    ) -> AddPlayerResponse:
        async with models.get_session() as s:
            sql = select(models.Player).where(models.Player.id == kwargs["id"])
            existing_db_player = (await s.execute(sql)).first()
            if existing_db_player is not None:
                return PlayerExists()
            db_player = models.Player(
                id=strawberry.ID(str(id)),
                full_name=full_name,
                first_name=first_name,
                last_name=last_name,
                is_active=is_active,
            )
            s.add(db_player)
            await s.commit()
        return Player.marshal(db_player)


"""
async def load_books_by_author(keys: list) -> list[Book]:
    async with models.get_session() as s:
        all_queries = [
            select(models.Book).where(models.Book.author_id == key) for key in keys
        ]
        data = [(await s.execute(sql)).scalars().unique().all() for sql in all_queries]
        print(keys, data)
    return data


async def load_author_by_book(keys: list) -> list[Book]:
    async with models.get_session() as s:
        sql = select(models.Author).where(models.Author.id in keys)
        data = (await s.execute(sql)).scalars().unique().all()
    if not data:
        data.append([])
    return data
"""


async def get_context() -> dict:
    return {
        # "author_by_book": DataLoader(load_fn=load_author_by_book),
        # "books_by_author": DataLoader(load_fn=load_books_by_author),
    }


schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
