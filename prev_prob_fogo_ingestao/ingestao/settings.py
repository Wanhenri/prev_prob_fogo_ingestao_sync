from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Encontra o caminho do .env de forma robusta
# Isso evita depender do diretório de execução do script
dotenv_path = Path(__file__).resolve().parent.parent / '.env'

# Defina a classe de configurações
class Settings(BaseSettings):
    # A biblioteca Pydantic Settings vai procurar por um arquivo .env automaticamente
    # Isso resolve o problema de path que você estava tendo
    model_config = SettingsConfigDict(
        env_file=dotenv_path, 
        env_file_encoding='utf-8',
        env_nested_delimiter='__' # Útil para variáveis aninhadas
    )

   
    # Variáveis de caminho
    PATH_DOCUMENTS: Path
    PATH_PROJETO: Path

    # Variáveis de conexão com o banco de dados
    db_url_neon: str
    db_url_aiven: str
    
    db_host: str
    db_port: int  # O Pydantic irá converter a string '12121' para um inteiro
    db_name: str
    db_user: str
    db_password: str
    db_sslmode: str

    @property
    def caminho_completo_env(self) -> Path:
        return self.PATH_DOCUMENTS / self.PATH_PROJETO / '.env'


# Instancie a classe para carregar as configurações
settings = Settings()


