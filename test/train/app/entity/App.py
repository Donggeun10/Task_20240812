import sqlalchemy
from sqlalchemy import Column, String, func, PrimaryKeyConstraint

from test.train.app.database import Base


class App(Base):
    __tablename__ = "tb_app"
    game_code = Column(String(20))
    device_os = Column(String(20))
    display_name = Column(String(100))
    package_name = Column(String(50))
    game_engine = Column(String(20), default='etc')
    market_country = Column(String(2), default='kr')
    schema_name = Column(String(10), nullable=True)
    sampling_rate = Column(sqlalchemy.Float, default=0.01)
    icon = Column(String(500), nullable=True)
    console_tracking_type = Column(String(1), default='N')
    insert_timestamp = Column(sqlalchemy.DateTime, server_default=func.now())
    insert_id = Column(String(50))
    update_timestamp = Column(sqlalchemy.DateTime, nullable=True)
    update_id = Column(String(50), nullable=True)
    public_yn = Column(String(1), default='N')
    use_yn = Column(String(1), default='Y')
    nw_sampling_rate = Column(sqlalchemy.Float, default=0.01)

    __table_args__ = (
        PrimaryKeyConstraint(game_code, device_os),
        {},
    )

