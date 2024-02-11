from pathlib import Path

from dotenv import dotenv_values

root_path = Path(__file__).resolve().parent.parent
dotenv_path = None

production_env_path = root_path / ".env.prod"
staging_env_path = root_path / ".env.stage"
local_env_path = root_path / ".env.local"

if production_env_path.is_file():
    dotenv_path = production_env_path
elif staging_env_path.is_file():
    dotenv_path = staging_env_path
elif local_env_path.is_file():
    dotenv_path = local_env_path

if not dotenv_path:
    raise EnvironmentError(
        "Please add .env.local or .env.stage or .env.prod file in project directory get reference from .env-EXAMPLE"
        "file"
    )

ENV_VARIABLES = dict(dotenv_values(dotenv_path=dotenv_path))
