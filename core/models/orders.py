from core.database import webhook_db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func

class Orders(db.Base):
    """
    WH Orders table
    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_id = Column(String(256), unique=True)
    order_qtd = Column(Integer)
    order_value = Column(Float)
    date_created = Column(DateTime, server_default=func.now())

    def __init__(self, order_id, order_qtd, order_value):
        self.order_id = order_id
        self.order_qtd = order_qtd
        self.order_value = order_value
