from cloudpassage.exceptions import CloudPassageAuthentication
from cloudpassage.exceptions import CloudPassageAuthorization
from cloudpassage.exceptions import CloudPassageCollision
from cloudpassage.exceptions import CloudPassageGeneral
from cloudpassage.exceptions import CloudPassageInternalError
from cloudpassage.exceptions import CloudPassageResourceExistence
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.exceptions import CloudPassageRateLimit


class TestUnitExceptions:
    def raise_authentication(self, msg):
        raise CloudPassageAuthentication(msg)

    def raise_authorization(self, msg):
        raise CloudPassageAuthorization(msg)

    def raise_collision(self, msg):
        raise CloudPassageCollision(msg)

    def raise_general(self, msg):
        raise CloudPassageGeneral(msg)

    def raise_internal(self, msg):
        raise CloudPassageInternalError(msg)

    def raise_resource_exist(self, msg):
        raise CloudPassageResourceExistence(msg)

    def raise_validation(self, msg):
        raise CloudPassageValidation(msg)

    def raise_rate_limit(self, msg):
        raise CloudPassageRateLimit(msg)

    def test_authentication(self):
        msg = 'test'
        try:
            self.raise_authentication(msg)
        except CloudPassageAuthentication as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_authorization(self):
        msg = "test"
        try:
            self.raise_authorization(msg)
        except CloudPassageAuthorization as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_collision(self):
        msg = "test"
        try:
            self.raise_collision(msg)
        except CloudPassageCollision as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_general(self):
        msg = "test"
        try:
            self.raise_general(msg)
        except CloudPassageGeneral as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_internal(self):
        msg = "test"
        try:
            self.raise_internal(msg)
        except CloudPassageInternalError as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_resource_existence(self):
        msg = "test"
        try:
            self.raise_resource_exist(msg)
        except CloudPassageResourceExistence as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_validation(self):
        msg = "test"
        try:
            self.raise_validation(msg)
        except CloudPassageValidation as e:
            assert msg == e.msg
            assert str(e) == msg

    def test_rate_limit(self):
        msg = "test"
        try:
            self.raise_rate_limit(msg)
        except CloudPassageRateLimit as e:
            assert msg == e.msg
            assert str(e) == msg
