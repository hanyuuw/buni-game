# -*- coding: utf-8 -*-

from Cloud import Cloud


class SafeCloud(Cloud, Cloud):
    def __init__(self):
        self.type = "safe"
