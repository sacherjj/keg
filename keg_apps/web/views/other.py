from __future__ import absolute_import
from __future__ import unicode_literals

import flask

from keg.web import BaseView as KegBaseView

blueprint = flask.Blueprint('other', __name__)


class BaseView(KegBaseView):
    blueprint = blueprint


class AutoAssign(BaseView):
    auto_assign = ('bar', 'baz')

    def get(self):
        self.bar = 'bar'
        self.baz = 'baz'
        self.foo = 'foo'
        pass

