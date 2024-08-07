from pydantic.v1 import BaseSettings
from pydantic import Field
import pathlib
from functools import lru_cache
import os
from pathlib import Path

os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = "1"

# The __file__ attribute is a special attribute that contains the path of the current file.
DOT_ENV = pathlib.Path(__file__).resolve().parent.parent / '.env'
# print(DOT_ENV)


class Settings(BaseSettings):
    # Field function is used to define the additional metadata keyspace
    # ... means that the field is required
    # it will read from the .env file and set the value of the keyspace variable.
    # Key in env file can be KEYSPACE or keyspace
    keyspace: str = Field(...)
    secret_key: str = Field(...)
    jwt_algo: str = Field(...)
    base_dir: Path = Path(__file__).resolve().parent
    template_dir: Path = Path(__file__).resolve().parent / "templates"

    # Name Config is not arbitrary, it is a Pydantic class that defines the configuration
    # for the settings class. The env_file attribute is used to specify the name of the .env file.
    class Config:
        env_file = DOT_ENV


@lru_cache
def get_settings():
    return Settings()
