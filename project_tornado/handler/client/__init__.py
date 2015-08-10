class Client(object):
    from project_tornado.handler.client.welcome_handler import WelcomeHandler
    from project_tornado.handler.client.error_handler import ErrorHandler


__all__ = ["Client"]
