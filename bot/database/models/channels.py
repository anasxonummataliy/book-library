from bot.database.base import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import String, BigInteger


class Channel(Base):
    __tablename__: 'channels_id'

    ch_id: Mapped[int] = Mapped[BigInteger]
