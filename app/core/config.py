from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    API_ID: str
    API_HASH: str
    PHONE_NUMBER:str

    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    def get_model_config(self, model_name: str  = '') -> dict[str, str]:
        """Возвращает конфигурацию для текущей модели."""
        config = {}
        if model_name == 'deepseek':
            config['api_key'] = self.DEEPSEEK_API_KEY
            config['base_url'] = self.DEEPSEEK_BASE_URL
        elif model_name == 'gpt-4o':
            config['api_key'] = self.OPENAI_API_KEY
            config['base_url'] = self.OPENAI_BASE_URL

        config['API_ID'] = self.API_ID
        config['API_HASH'] = self.API_HASH
        config['PHONE_NUMBER'] = self.PHONE_NUMBER
        return config

settings = Settings()
