class StreamlitStub:
    """Minimal stub of Streamlit functions used in tests."""

    @staticmethod
    def cache_data(func=None, **kwargs):
        if func is None:
            def decorator(fn):
                return fn
            return decorator
        return func

    @staticmethod
    def warning(*args, **kwargs):
        pass

    @staticmethod
    def info(*args, **kwargs):
        pass

    @staticmethod
    def error(*args, **kwargs):
        pass

    @staticmethod
    def stop():
        raise SystemExit
