from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR  = Path(__file__).parent.parent

class AuthData(BaseModel):
    private_key: Path = BASE_DIR  / "src" / "auth" / "tokens" / "private_key.pem"
    public_key: Path = BASE_DIR  /  "src" / "auth"  / "tokens" / "public_key.pem"
    algorithm: str = "RS256"
    days: int = 31
    
class EnvData(BaseSettings):
    DB_URl: str
    DB_URl_ASYNC: str
    
class Config(BaseModel):
    env_data:EnvData = EnvData()
    auth_data:AuthData = AuthData()
    
config = Config()