import datetime
import logging
import uuid

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from sqlalchemy import func
from sqlalchemy import ForeignKey, Column
from sqlalchemy import DateTime, Float, String, Text

from sqlalchemy_utils import UUIDType, aggregated


logger = logging.getLogger(__name__)


Base = declarative_base()


class Request(Base):
    __tablename__ = 'request'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    dt = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    ds = Column(Float, nullable=True)

    executions = relationship('Execution', back_populates='request')


class Execution(Base):
    __tablename__ = "execution"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    dt = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    ds = Column(Float, nullable=True)

    request_id = Column(UUIDType, ForeignKey('request.id'))
    request = relationship('Request', back_populates='executions')

    operations = relationship('Operation', back_populates='execution')

    @classmethod
    def from_document(cls, document, variable_values, **kwargs):

        operations = [
            Operation.from_definition(definition) for definition in document.definitions
        ]

        return cls(operations=operations, **kwargs)


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    execution_id = Column(UUIDType, ForeignKey('execution.id'))
    execution = relationship('Execution', back_populates='operations')

    operation = String(length=128)
    name = String(length=128)

    @classmethod
    def from_definition(cls, definition, **kwargs):

        logger.info("definition.variable_definitions: %r", definition.variable_definitions)
        logger.info("definition.directives: %r", definition.directives)
        logger.info("definition.selection_set: %r", definition.selection_set)

        return cls(
            operation=definition.operation,
            name=definition.name,
            **kwargs
        )
