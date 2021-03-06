#!/usr/bin/env python3.5
"""
    Gestion basica de estados de sensores para la API de hackerspaces.org
"""
import pickle
import time
import json
import os
from contextlib import suppress
import asyncio
import aiohttp
import sys
from aiohttp import web


class PersistentDict(dict):
    @classmethod
    def path(cls):
        """ Path del pickle """
        return os.path.expanduser('~/.statusapi.pickle')

    @classmethod
    def load(cls):
        """ Recarga el objeto desde el pickle y lo devuelve """
        with suppress(FileNotFoundError, EOFError):
            return pickle.load(open(cls.path(), 'rb'))
        return cls()

    def save(self):
        """ Guarda en el pickle el objeto actual"""
        with open(self.path(), 'wb') as fobj:
            pickle.dump(self, fobj)


class Status(PersistentDict):
    def __init__(self):
        self._mandatory_attrs = ["api", "logo", "url", "space"]
        self._statuses = {}
        self["api"] = "0.13"
        self.token = False
        PersistentDict.__init__(self)

    @property
    def open(self):
        for _, status in self._statuses.items():
            if status['timeout'] == 0 and status['open']:
                return True
            if status['open'] and status['timeout'] < time.time():
                return True
        return False

    @property
    def state(self):
        def _get_last_status():
            with suppress(IndexError):
                return sorted(self._statuses.values(),
                              key=lambda x: x['time'])[-1]
            return {'time': 0, 'trigger': "Nobody"}

        last_status = _get_last_status()
        return {'open': self.open,
                'lastchange': last_status['time'],
                'trigger_person': last_status['trigger']}

    @state.setter
    def state(self, status_dict):
        keys = set(list(status_dict.values())[0].keys())
        if not set(['timeout', 'trigger', 'open']).issubset(keys):
            raise aiohttp.web.HTTPBadRequest(text="Bad status, needs to have"
                                             " timeout, trigger and open")
        for key, values in status_dict.items():
            values['time'] = time.time()
            self._statuses[key] = values

    def is_complete(self):
        with suppress(KeyError):
            return all([self[attr] for attr in self._mandatory_attrs])
        return False

    @property
    def __json__(self):
        if not self.is_complete:
            raise aiohttp.web.HTTPBadRequest(
                text="Not all mandatory args are set ({})".format(
                    self._mandatory_attrs))
        self['state'] = self.state
        self['open'] = self.open
        return json.dumps(self).encode('utf-8')


class StatusClient(Status):
    def __init__(self, path="http://localhost:8080", token=False):
        self._path = path
        self.headers = {'AUTH': token}

    def path(self, resource=False):
        if not resource:
            return self._path
        return self._path + "/{}".format(resource)

    def __enter__(self):
        self.block([self.load()])
        return self

    def __exit__(self, *args):
        print(self.block(self.save_all()))

    async def load(self):
        with aiohttp.ClientSession() as session:
            async with session.get(self.path()) as resp:
                if resp.status != 200:
                    raise Exception(await resp.text())
                json_ = await resp.json()
                for key, value in json_.items():
                    self[key] = value

    async def save(self, where, what):
        with aiohttp.ClientSession() as session:
            async with session.patch(self.path(where), data=what,
                                     headers=self.headers) as resp:
                if resp.status != 200:
                    return await resp.text()
                return True

    def save_all(self):
        def awaitables():
            for attr_name, attr_values in self.items():
                value = json.dumps(attr_values).encode('utf-8')
                yield self.save(attr_name, value)
        return awaitables()

    @classmethod
    def block(cls, awaitables):
        loop = asyncio.get_event_loop()
        waited = loop.run_until_complete(asyncio.wait(list(awaitables)))
        return [res.result() for res in waited[0]]


class StatusAPI(web.View):
    async def get(self):
        return web.Response(body=self.request.app['status'].__json__)

    async def patch(self):
        token = self.request.headers.get('AUTH')
        expected = self.request.app['status'].token
        if expected:
            if token != expected:
                raise aiohttp.web.HTTPUnauthorized()
        else:
            self.request.app['status'].token = token

        key = self.request.match_info['what']
        if key == "state":
            setattr(self.request.app['status'], 'state',
                    await self.request.json())
        else:
            self.request.app['status'][key] = await self.request.json()
        self.request.app['status'].save()
        return web.Response(body=b'OK')


async def on_shutdown(app):
    app['status'].save()


def server():
    app = web.Application()
    app['status'] = Status().load()
    app.router.add_route('*', '/api/{what}', StatusAPI)
    app.router.add_route('*', '/api', StatusAPI)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app)


def client():
    with StatusClient(sys.argv[1], sys.argv[2]) as client:
        assert len(sys.argv) > 1, "Wrong params: url token [key] [value]"
        if len(sys.argv) > 3:
            client[sys.argv[3]] = json.loads(sys.argv[4])
        print(client)


if __name__ == "__main__":
    server()
