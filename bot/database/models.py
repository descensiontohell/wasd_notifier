from sqlalchemy import MetaData, Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base(MetaData())


class SubModel(base):
    __tablename__ = "subscriptions"
    vk_id = Column(ForeignKey("users.vk_id"), primary_key=True)
    channel_name = Column(ForeignKey("channels.name", ondelete="CASCADE"), primary_key=True)
    subs = relationship("UserModel", back_populates="channels")
    channels = relationship("ChannelModel", back_populates="subs")


class UserModel(base):
    __tablename__ = "users"
    vk_id = Column(Integer(), primary_key=True)
    is_active = Column(Boolean(), nullable=False, server_default="true")
    channels = relationship("SubModel", back_populates="subs")


class ChannelModel(base):
    __tablename__ = "channels"
    name = Column(String(), primary_key=True)
    state = Column(Boolean(), nullable=False, server_default="false")
    subs = relationship("SubModel", back_populates="channels")


