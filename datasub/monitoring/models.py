import datetime
import logging
import uuid

import graphql.language.ast
import graphql.language.printer

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

from sqlalchemy import func
from sqlalchemy import ForeignKey, Column
from sqlalchemy import DateTime, Float, String, Text

from sqlalchemy_utils import aggregated, UUIDType, JSONType


logger = logging.getLogger(__name__)


Base = declarative_base()

UUIDType = UUIDType(binary=False)

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
    fragments = relationship('Fragment', back_populates='execution')

    variables = Column(JSONType())

    @classmethod
    def from_document(cls, document, **kwargs):

        operations = [
            Operation.from_definition(definition)
            for definition in document.definitions
            if isinstance(definition, graphql.language.ast.OperationDefinition)
        ]

        fragments = [
            Fragment.from_definition(definition)
            for definition in document.definitions
            if isinstance(definition, graphql.language.ast.FragmentDefinition)
        ]

        return cls(
            operations=operations,
            fragments=fragments,
            **kwargs
        )


class Operation(Base):
    __tablename__ = 'operation'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    execution_id = Column(UUIDType, ForeignKey('execution.id'))
    execution = relationship('Execution', back_populates='operations')

    operation = Column(String(length=128))
    name = Column(String(length=128))

    definition = Column(Text())

    @classmethod
    def from_definition(cls, definition, **kwargs):
        return cls(
            operation=definition.operation,
            name=definition.name.value,
            definition=graphql.language.printer.print_ast(definition),
            **kwargs
        )


class Fragment(Base):
    __tablename__ = 'fragment'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    execution_id = Column(UUIDType, ForeignKey('execution.id'))
    execution = relationship('Execution', back_populates='fragments')

    name = Column(String(length=128))
    type_condition = Column(String(length=128))

    definition = Column(Text())

    @classmethod
    def from_definition(cls, definition, **kwargs):
        return cls(
            name=definition.name.value,
            type_condition = definition.type_condition.name.value,
            definition=graphql.language.printer.print_ast(definition),
            **kwargs
        )
