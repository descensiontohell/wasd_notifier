import os
from dataclasses import dataclass

import yaml
from envyaml import EnvYAML


@dataclass
class Config:
    host: str
    user: str
    password: str
    database: str


def setup_config() -> Config:
    raw_config = EnvYAML(os.path.join(os.getcwd(), "docker-compose.yml"))

    if os.environ.get("IS_IN_DOCKER", False):
        db_host = "db"
    else:
        db_host = "localhost:6060"

    db_user = raw_config["services.db.environment.POSTGRES_USER"]
    db_password = raw_config["services.db.environment.POSTGRES_PASSWORD"]
    db_name = raw_config["services.db.environment.POSTGRES_DB"]

    return Config(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
    )


config = setup_config()
