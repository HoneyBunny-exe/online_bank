import contextvars


class UserContext:
    _user = contextvars.ContextVar('user', default=None)
    _token = None

    @classmethod
    def get_user(cls):
        return cls._user.get()

    @classmethod
    def set_user(cls, user):
        cls._user.set(user)

    @classmethod
    def drop_user(cls):
        cls._user.set(None)

    @classmethod
    def run(cls, func, *args, **kwargs):
        ctx = contextvars.copy_context()
        return ctx.run(func, *args, **kwargs)

