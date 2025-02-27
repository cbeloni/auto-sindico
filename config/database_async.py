from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv, dotenv_values

load_dotenv()
_config = dotenv_values(".env")

# Configuração do banco de dados
DATABASE_URL = f"mysql+aiomysql://{_config['USER']}:{_config['PASSWORD']}@{_config['HOST']}/{_config['DATABASE']}"

# Criando o engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Criando o SessionMaker
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self._session_maker = SessionLocal

    async def get_session(self) -> AsyncSession: # type: ignore
        async with self._session_maker() as session:
            yield session


db = Database()
