import uuid
import hashlib
import random
import logging

logger = logging.getLogger(__name__)


class ExposesUUID():

    def sha256(self):
        return hashlib.sha256(self.hashstring)

    def uuid3(self):
        return uuid.uuid3(self.UUID_NAMESPACE, self.hashstring)

    def uuid5(self):
        return uuid.uuid5(self.UUID_NAMESPACE, self.hashstring)


class GQLDocumentHash(ExposesUUID):
    UUID_NAMESPACE = uuid.UUID('f73a37e1-03cc-4d13-8859-aebc7f28892a')

    def __init__(self, document):
        definition_hashes = []
        for definition in document.definitions:
            definition_hashes.append(
                GQLDefinitionHash(definition).sha256().hexdigest()
            )
        self.hashstring = ''.join(sorted(definition_hashes))


class GQLDefinitionHash(ExposesUUID):
    UUID_NAMESPACE = uuid.UUID('d4fefabe-6811-4e2f-a0c8-cb77cbf0cf9c')

    def __init__(self, definition):
        raise NotImplementedError()
