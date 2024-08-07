from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
import uuid
from app.config import get_settings
from .validators import validate_email_format
from .security import get_password_hash,verify_password

settings = get_settings()


class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __repr__(self) -> str:
        return f"User(email={self.email}, user_id={self.user_id})"

    def __str__(self) -> str:
        return self.__repr__()

    def set_password(self, password, commit=False):
        pw_hash=get_password_hash(password)
        self.password = pw_hash
        if commit:
            self.save()
        return True
        
    @staticmethod
    def create_user(email, password=None):
        q = User.objects.filter(email=email)
        if q.count() > 0:
            raise Exception("User already exists")
        valid, msg, email = validate_email_format(email)
        if not valid:
            raise Exception(f"Invalid Email:{msg}")
        user = User(email=email)
        user.set_password(password)
        user.save()
        return user
    
    def verify_password(self, raw_password):
        verified,_=verify_password(self.password, raw_password)
        return verified
