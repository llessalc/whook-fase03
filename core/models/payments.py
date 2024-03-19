from core.database import webhook_db as db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import DateTime
from sqlalchemy.sql import func


class Payments(db.Base):
    """
    WH Payments table
    """
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    payment_id = Column(String(256), unique=True)
    type = Column(String(256))
    user_id = Column(Integer)
    api_version = Column(String(256))
    action = Column(String(256))
    date_created = Column(DateTime, server_default=func.now())
    qr_code = Column(String(512))

    def __init__(self, payment_id, type, user_id, api_version, action, qr_code):
        self.payment_id = payment_id
        self.type = type
        self.user_id = user_id
        self.api_version = api_version
        self.action = action
        self.qr_code = qr_code