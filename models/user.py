from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey,
    Table,
    text,
)
from sqlalchemy.dialects.mysql import BIT
from sqlalchemy.orm import relationship
from config.database import Base
from models.ad import Ad

class UserAccount(Base):
    __tablename__ = 'UserAccount'

    user_id: int = Column(Integer, primary_key = True, autoincrement = True)
    username: str = Column(String(100), nullable = False)
    phone_number: str = Column(String(12), nullable = True)
    birth_date: datetime = Column(Date, nullable = True)
    last_login: datetime = Column(DateTime, server_default = text('NOW()'))
    profile_image_url: str = Column(String(100))
    is_active: int = Column(BIT, nullable = False)

    created_at: datetime = Column(DateTime, server_default = text('NOW()'))

    ads = relationship('Ad', back_populates = 'user', cascade = "delete")
    user_address = relationship('UserAddress', back_populates = 'user', cascade = "delete", uselist = False)
    user_login_data = relationship('UserLoginData', back_populates = 'user', uselist = False)
    user_login_data_ext = relationship('UserLoginDataExt', back_populates = 'user')

    @property
    def email_addrs(self) -> str:
        return self.user_login_data.email_addr

class UserLoginData(Base):
    __tablename__ = 'UserLoginData'

    user_id: int = Column(Integer, ForeignKey('UserAccount.user_id'), primary_key = True)
    password_hash: str = Column(String(300), nullable = False)
    password_salt: str = Column(String(300), nullable = False)
    email_addr: str = Column(String(320), nullable = False, unique = True)
    confirm_token: str = Column(String(200), nullable = True)
    confirm_token_time: str = Column(String(50), nullable = True)
    recovery_token: str = Column(String(200), nullable = True)
    recovery_token_time: str = Column(String(50), nullable = True)

    hash_algo_id: int = Column(Integer, ForeignKey('HashAlgo.id'), nullable = False)
    email_validation_status_id: int = Column(Integer, ForeignKey('EmailValidationStatus.id'), nullable = False)

    user = relationship('UserAccount', back_populates = 'user_login_data', uselist = False, lazy = 'joined')
    hash = relationship('HashAlgo', back_populates = 'users', uselist = False)
    email_status = relationship('EmailValidationStatus', back_populates = 'users', uselist = False)

    @property
    def is_active(self) -> int:
        return self.user.is_active

class UserAddress(Base):
    __tablename__ = "UserAddress"

    id: int = Column(Integer, primary_key = True, autoincrement = True)
    country: str = Column(String(50), nullable = False)
    city: str = Column(String(50), nullable = False, index = True)
    street: str = Column(String(200), nullable = False)
    num: str = Column(String(20), nullable = False)
    postal_code: str = Column(String(50), nullable = False)
    user_id: int = Column(Integer, ForeignKey("UserAccount.user_id", ondelete = 'CASCADE'), nullable = False)
    address_date: datetime = Column(DateTime, server_default = text('NOW()'))
    updated_at: datetime = Column(DateTime, onupdate = datetime.now())

    user = relationship("UserAccount", back_populates = "user_address")

class ExternalProvider(Base):
    __tablename__ = 'ExternalProvider'

    id: int = Column(Integer, primary_key = True, autoincrement = True)
    ext_provider_name: str = Column(String(50), nullable = False)
    end_point_url: str = Column(String(100), nullable = False)

    user_login_data_ext = relationship('UserLoginDataExt', back_populates = 'ext_provider')

class UserLoginDataExt(Base):
    __tablename__ = 'UserLoginDataExt'
    
    id: int = Column(Integer, primary_key = True, autoincrement = True)
    external_provider_token: str = Column(String(200), nullable = False)
    external_provider_id: int = Column(Integer, ForeignKey('ExternalProvider.id'), nullable = False)
    user_id: int = Column(Integer, ForeignKey('UserAccount.user_id'), nullable = False)

    ext_provider = relationship('ExternalProvider', back_populates = 'user_login_data_ext')
    user = relationship('UserAccount', back_populates = 'user_login_data_ext')

class HashAlgo(Base):
    __tablename__ = 'HashAlgo'

    id: int = Column(Integer, primary_key = True, autoincrement = True)
    hash_name: str = Column(String(50), nullable = False)
    created_at: datetime = Column(DateTime, server_default = text('NOW()'))

    users = relationship('UserLoginData', back_populates = 'hash')

class EmailValidationStatus(Base):
    __tablename__ = 'EmailValidationStatus'

    id: int = Column(Integer, primary_key = True, autoincrement = True)
    status_name: str = Column(String(30))

    users = relationship('UserLoginData', back_populates = 'email_status')