from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(title="Tortoise ORM FastAPI example")


def initiate_db():

    register_tortoise(
        app,
        db_url="sqlite://db.sqlite3",
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


Tortoise.init_models(["models"], "models")