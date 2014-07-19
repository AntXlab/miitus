from tornado.web import Application, RequestHandler, StaticFileHandler
from restless.tnd import TornadoResource
from werkzeug.utils import find_modules, import_string
from miitus import defs
from miitus.srv import utils
from .base import SwaggerJsonFileHandler


class App(utils.Singleton):
    """
    tornado application container
    """

    @staticmethod
    def __gen_route(kls):
        ret = []
        if issubclass(kls, RequestHandler):
            for p in getattr(kls, defs.ROUTE_ATTR_NAME):
                ret.append((p, kls))
        elif issubclass(kls, TornadoResource):
            for r in getattr(kls, defs.ROUTE_ATTR_NAME):
                if r[1] == 'list':
                    ret.append((r[0], kls.as_list()))
                elif r[1] == 'detail':
                    ret.append((r[0], kls.as_detail()))

        return ret

    @staticmethod
    def __routes(package_name=None):
        """
        generating route by scanning modules in package(by package_name)

        Note: only modules would be scanned, handlers declared in package's
        __init__.py won't be scannd.
        """
        package_name = '.'.join(__name__.split('.')[:-1])

        ret = []
        for name in find_modules(package_name, recursive=True):
            mod = import_string(name)
            for item_name in dir(mod):
                item = getattr(mod, item_name)
                if type(item) == type and hasattr(item, defs.ROUTE_ATTR_NAME):
                    ret.extend(App.__gen_route(item))

        return ret

    def __init__(self, package_name=None):
        r = App.__routes(package_name)
        c = utils.Config().to_dict(defs.TORNADO_CONFIG_PREFIX)
        if c['debug']:
            # serve static files from tornado directly
            r.append((defs.STATIC_WEB_URL_FILTER, StaticFileHandler, {"path": utils.get_static_web_folder()}))
            r.append((
                defs.STATIC_APIDOC_URL_FILTER,
                SwaggerJsonFileHandler,
                {"path": utils.get_static_api_doc_folder()}
            ))

        self.__app = Application(r, **c)

    @property
    def app(self):
        """
        access tornado app instance
        """
        return self.__app

