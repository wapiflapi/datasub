import datetime
import logging
import uuid

import graphql.language.ast
import graphql.language.printer

from sqlalchemy.orm import backref, relationship
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import func
from sqlalchemy import ForeignKey, Column, Table
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


execution_operation_link = Table(
    'execution_operation_link', Base.metadata,
    Column('left_id', UUIDType, ForeignKey('execution.id')),
    Column('right_id', UUIDType, ForeignKey('operation.id'))
)


execution_fragment_link = Table(
    'execution_fragment_link', Base.metadata,
    Column('left_id', UUIDType, ForeignKey('execution.id')),
    Column('right_id', UUIDType, ForeignKey('fragment.id'))
)


class Execution(Base):
    __tablename__ = "execution"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    dt = Column(DateTime, nullable=True, default=datetime.datetime.utcnow)
    ds = Column(Float, nullable=True)

    request_id = Column(UUIDType, ForeignKey('request.id'))
    request = relationship('Request', back_populates='executions')

    operations = relationship(
        "Operation",
        secondary=execution_operation_link,
        back_populates="executions",
    )
    fragments = relationship(
        "Fragment",
        secondary=execution_fragment_link,
        back_populates="executions",
    )

    variables = Column(JSONType())

    @classmethod
    def from_document(cls, session, document, **kwargs):

        operations = [
            Operation.get_or_create_from_definition(session, definition)
            for definition in document.definitions
            if isinstance(definition, graphql.language.ast.OperationDefinition)
        ]

        fragments = [
            Fragment.get_or_create_from_definition(session, definition)
            for definition in document.definitions
            if isinstance(definition, graphql.language.ast.FragmentDefinition)
        ]

        return cls(
            operations=operations,
            fragments=fragments,
            **kwargs
        )


class GetOrCreateMixIn():

    @classmethod
    def get_or_create(cls, session, **kwargs):
        try:
            return session.query(cls).filter_by(**kwargs).one()
        except NoResultFound:
            pass

        created = cls(**kwargs)

        try:
            session.add(created)
            session.commit()
            return created
        except IntegrityError:
            session.rollback()
            return session.query(cls).filter_by(**kwargs).one()


class Operation(Base, GetOrCreateMixIn):
    __tablename__ = 'operation'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    executions = relationship(
        'Execution',
        secondary=execution_operation_link,
        back_populates='operations',
    )

    operation = Column(String(length=128))
    name = Column(String(length=128))

    definition = Column(Text())

    @classmethod
    def get_or_create_from_definition(cls, session, definition, **kwargs):
        definition_rep = graphql.language.printer.print_ast(definition)

        UUID_NAMESPACE = uuid.UUID('f73a37e1-03cc-4d13-8859-aebc7f28892a')
        definition_uuid = uuid.uuid5(UUID_NAMESPACE, definition_rep)

        return cls.get_or_create(
            session,
            id=definition_uuid,
            operation=definition.operation,
            name=definition.name.value,
            definition=definition_rep,
            **kwargs
        )


class Fragment(Base, GetOrCreateMixIn):
    __tablename__ = 'fragment'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)

    executions = relationship(
        'Execution',
        secondary=execution_fragment_link,
        back_populates='fragments',
    )

    name = Column(String(length=128))
    type_condition = Column(String(length=128))

    definition = Column(Text())

    @classmethod
    def get_or_create_from_definition(cls, session, definition, **kwargs):
        definition_rep = graphql.language.printer.print_ast(definition)

        UUID_NAMESPACE = uuid.UUID('d4fefabe-6811-4e2f-a0c8-cb77cbf0cf9c')
        definition_uuid = uuid.uuid5(UUID_NAMESPACE, definition_rep)

        return cls.get_or_create(
            session,
            id=definition_uuid,
            name=definition.name.value,
            type_condition = definition.type_condition.name.value,
            definition=definition_rep,
            **kwargs
        )
