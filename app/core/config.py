from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


TEST_MODE = True # если не поставить True, то тесты не будут запускаться


class Settings(BaseSettings):
    """Настройки проекта"""

    project_name: str = Field(title='Название проекта')
    api_v1_prefix: str = Field(title='Префикс первой версии API', default='/api/v1')
    base_url: str = Field(default='http://127.0.0.1:8000')

    # region Настройки БД
    db_user: str = Field(title='Пользователь БД')
    db_password: str = Field(title='Пароль БД')
    db_host: str = Field(title='Хост БД')
    db_port: int = Field(title='Порт ДБ', default='5432')
    db_name: str = Field(title='Название БД')
    metadata_naming_convention: dict[str, str] = Field(
        default={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s'
        })
    # endregion

    container_wiring_modules: list = Field(
        title='Модули контейнера',
        default=[
            'app.api.v1.endpoints.product',
            'app.api.v1.endpoints.order'
        ]
    )

    
    database_url: str = Field(
        title='Ссылка БД',
        default='sqlite+aiosqlite:///./db.sqlite3' if not TEST_MODE\
            else 'sqlite+aiosqlite:///./test.sqlite3'
    )

    @property
    def db_url(self) -> PostgresDsn:
        if self.database_url:
            return self.database_url
        return PostgresDsn.build(
            scheme='postgresql',
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=f'{self.db_name}',
        )

    class Config:
        if TEST_MODE:
            env_file = '.test.env'
        else:
            env_file = '.env'


settings = Settings()
