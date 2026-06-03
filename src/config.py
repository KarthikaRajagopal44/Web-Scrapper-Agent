from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    MODEL_NAME: str = "gemini-3.5-flash"
    MAX_TEXT_LENGTH: int = 12000  # Safely limits context length to avoid model crashes
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()