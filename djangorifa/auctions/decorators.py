# Much hacked version of
# http://www.caktusgroup.com/blog/2009/05/26/explicit-table-locking-with-postgresql-and-django/
from django.utils.functional import wraps
LOCK_MODES = (
    'ACCESS SHARE',
    'ROW SHARE',
    'ROW EXCLUSIVE',
    'SHARE UPDATE EXCLUSIVE',
    'SHARE',
    'SHARE ROW EXCLUSIVE',
    'EXCLUSIVE',
    'ACCESS EXCLUSIVE',
)

class require_lock(object):

    def __init__(self, model, lock, *args, **kwargs):
        self.model = model
        self.lock = lock

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return inner

    def enable(self):
        if self.lock not in LOCK_MODES:
            raise ValueError('%s is not a PostgreSQL supported lock mode.')
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute(
            'LOCK TABLE %s IN %s MODE' % (self.model._meta.db_table, self.lock)
        )