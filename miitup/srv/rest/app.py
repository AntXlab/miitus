from .route import r
from ..util import Config
from tornado.web import Application
import miitup.defs


app = Application(
    r,
    **(Config().to_dict(miitup.defs.TORNADO_CONFIG_PREFIX))
)

