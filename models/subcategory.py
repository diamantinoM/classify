from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship
from config.database import Base

subcategory_field_definition = Table(
    'Subcategory_FieldDefinition',
    Base.metadata,
    Column("subcategory_id", Integer, ForeignKey('Subcategory.id'), primary_key = True, nullable = False),
    Column("field_definition_id", Integer, ForeignKey('FieldDefinition.id'), primary_key = True, nullable = False)
)

class Subcategory(Base):
    __tablename__ = 'Subcategory'

    id: int = Column(Integer, primary_key = True, autoincrement = True)
    subcategory_name: str = Column(String(40), nullable = False, unique = True)
    category_id: int = Column(Integer, ForeignKey('Category.id', ondelete = 'CASCADE'), nullable = False)

    ads = relationship("Ad", back_populates = 'subcategory')
    category = relationship("Category", back_populates = 'subcategories')
    field_definitions = relationship('FieldDefinition', secondary = subcategory_field_definition, back_populates = 'subcategories')


