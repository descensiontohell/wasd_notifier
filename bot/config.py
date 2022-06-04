import os
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    host: str
    user: str
    password: str
    database: str


def setup_config() -> Config:
    with open(os.path.join(os.getcwd(), "docker-compose.yml")) as conf:
        raw_config = yaml.safe_load(conf)["services"]["db"]["environment"]

    if os.environ.get("IS_IN_DOCKER", False):
        db_host = "db"
    else:
        db_host = "localhost:6060"

    db_user = raw_config["POSTGRES_USER"]
    db_password = raw_config["POSTGRES_PASSWORD"]
    db_name = raw_config["POSTGRES_DB"]

    return Config(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
    )


config = setup_config()
