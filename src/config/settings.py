from pydantic import BaseSettings
import pathlib

base_path = pathlib.Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    model_file_name: str
    secure_model_file_name: str
    use_secure = False

    def get_model_file_name(self):
        if self.use_secure:
            return self.secure_model_file_name
        else:
            return self.model_file_name

    class Config:
        env_file = f"{base_path}/.env"


settings = Settings()
