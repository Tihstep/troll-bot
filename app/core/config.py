from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    DEEPSEEK_BASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str
    
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    
    def get_model_config(self, model_name: str) -> dict[str, str]:
        """Возвращает конфигурацию для текущей модели."""
        config = {}
        if model_name == 'deepseek':
            config['api_key'] = self.DEEPSEEK_API_KEY
            config['base_url'] = self.DEEPSEEK_BASE_URL
        elif model_name == 'openai':
            config['api_key'] = self.OPENAI_API_KEY
            config['base_url'] = self.OPENAI_BASE_URL
        return config

settings = Settings()
print(settings.get_model_config('openai'))