#!/usr/bin/env python3.5
"""
    Gestion basica de estados de sensores para la API de hackerspaces.org
"""
import pickle
import time
import json
import os
from contextlib import suppress
import aiohttp
from aiohttp import web


class BaseStatus:
    def __init__(self):
        self._mandatory_attrs = ["api", "logo", "url", "space"]
        self._statuses = {}
        self.api = "0.13"
        self.logo = False
        self.url = False
        self.logo = False
        self.location = {'lat': False, 'lon': False, 'address': False}
        self.open = False
        self.space = False
        self.contact = {}
        self.icon = {'open': False, 'closed': False}
        self.issue_report_channels = ["email"]


class Status(BaseStatus):
    """
        Objeto StatusAPI, para empezar, carga este objeto en ipython,
        crealo con los parametros necesarios rellenos y guardalo con save
        El sistema de estados es bastante sencillo:
            - Almacenamos, por cada sensor, el timeout del sensor
            (unix timestamp de la fecha en la que va a caducar),
            el trigger_person (en la mayoria de sensores, salvo
            por ejemplo en uno de tarjetas esto sera el sensor mismo)
            y si el estado al que pasa el sensor es a abierto o a cerrado
            Podemos poner un timeout a cero, para sensores sin timeout
            - En base a esto, calculamos si el espacio esta abierto o cerrado
            - Podemos actualizar multiples sensores en una sola peticion
    """
    @classmethod
    def path(cls):
        """ Path del pickle """
        return os.path.expanduser('~/.statusapi.pickle')

    @property
    def state(self):
        """ Devuelve el estado del hackerspace """
        def _get_status():
            """ Devuelve el estado del hackerspace
                (abierto(True)/cerrado(False))"""
            for _, status in self._statuses.items():
                if status['timeout'] == 0 and status['open']:
                    return True
                if status['open'] and status['timeout'] < time.time():
                    return True
            return False

        def _get_last_status():
            """ Last status"""
            with suppress(IndexError):
                return sorted(self._statuses.values(),
                              key=lambda x: x['time'])[-1]
            return {'time': 0, 'trigger': "Nobody"}

        last_status = _get_last_status()
        return {'open': _get_status(),
                'lastchange': last_status['time'],
                'trigger_person': last_status['trigger']}

    @state.setter
    def state(self, status_dict):
        """ Establece un estado """
        keys = set(list(status_dict.values())[0].keys())
        assert set(['timeout', 'trigger', 'open']).issubset(keys)
        for key, values in status_dict.items():
            values['time'] = time.time()
            self._statuses[key] = values

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

    @property
    def __json__(self):
        """ Dict magic """
        assert all([getattr(self, a) for a in self._mandatory_attrs]), \
            "No todos los parametros obligatorios estan establecidos"
        dict_ = {a: b for a, b in self.__dict__.items()
                 if not a.startswith('_')}
        dict_['state'] = self.state
        return json.dumps(dict_).encode('utf-8')


class StatusClient(Status):
    """ Seteamos _path despues de instanciarla
        antes de operar con ella"""
    _path = "http://localhost:8080"

    @property
    def path(self):
        return self._path

    async def load(self):
        """ Recarga el objeto desde el pickle y lo devuelve """
        with aiohttp.ClientSession() as session:
            async with session.get(self.path) as resp:
                for key, value in await resp.json():
                    setattr(self, key, value)

    async def save(self):
        """ Guarda en el pickle el objeto actual"""
        for attr_name, attr_values in self.__json__:
            value = json.dumps(attr_values).encode('utf-8')
            with aiohttp.ClientSession() as session:
                async with session.patch(self.path + "/{}".format(attr_name),
                                         data=value) as resp:
                    await resp.text()


class StatusAPI(web.View):
    """ Status API """
    async def get(self):
        """ Devuelve el diccionario completo del objeto estado """
        return web.Response(body=self.request.app['status'].__json__)

    async def patch(self):
        """
            Establece cualquier propiedad del objeto ``Status``
        """
        key = self.request.match_info['what']
        setattr(self.request.app['status'], key, await self.request.json())
        self.request.app['status'].save()
        return web.Response(body=b'OK')


async def on_shutdown(app):
    """ Guardamos el estado cuando paramos el servicio """
    app['status'].save()


def server():
    """ Lanzamos el servidor web"""
    app = web.Application()
    app['status'] = Status().load()
    app.router.add_route('*', '/{what}', StatusAPI)
    app.router.add_route('*', '/', StatusAPI)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app)



if __name__ == "__main__":
    server()
