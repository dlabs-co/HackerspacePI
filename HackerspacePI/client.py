#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    APIClient
"""

import requests
import ConfigParser
import os


class APIClient(object):
    """
        Main API client
    """
    def __init__(self, api_point):
        """
            Start
        """
        self.api_point = api_point
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.expanduser('~/.hackerspaceapi.cfg'))
        self.status_modules = []

    def status(self):
        """
            Start all status modules and get them into status_modules
        """
        statuses = {}
        is_open = 0
        for item, priority in dict(self.config.items('client')):
            if priority == 0:
                continue
            _item = __import__(item)
            try:
                # Setup is optional
                getattr(_item, 'setup')
            except AttributeError:
                pass

            statuses[item] = getattr(_item, 'status') * priority
            # TODO: rest time spent * priority

        for name, status_value in statuses:
            print name
            is_open += status_value

        if is_open > 100:
            return True

        return False

    def update_status(self):
        """
            Update status
        """
        status = self.status()
        if status:
            requests.post(
                "{}/state".format(self.api_point),
                json={'status': status}
            )
