#!/usr/bin/env python3.5
"""
    Gestion basica de estados de sensores para la API de hackerspaces.org
"""
import pickle
import time
import json
import os
from contextlib import suppress
from aiohttp import web


class Status:
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

    def __init__(self):
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
        keys = list(status_dict.values())[0].keys()
        for key in ['timeout', 'trigger', 'open']:
            if key not in keys:
                raise AttributeError('Un estado tiene que tener timeout,'
                                     ' open y trigger')
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
        dict_ = {a: b for a, b in self.__dict__.items()
                 if not a.startswith('_')}
        dict_['state'] = self.state
        return json.dumps(dict_).encode('utf-8')


class StatusAPI(web.View):
    """ Status API """
    async def get(self):
        """ Devuelve el diccionario completo del objeto estado """
        return web.Response(body=self.request.app['status'].__json__)

    async def patch(self):
        """
            Establece cualquier propiedad del objeto ``Status``
        """
        await self.request.post()
        for key, value in self.request.POST.items():
            setattr(self.request.app['status'], key, json.loads(value))
        self.request.app['status'].save()
        return web.Response(body=b'OK')


async def on_shutdown(app):
    """ Guardamos el estado cuando paramos el servicio """
    app['status'].save()


def server():
    """ Lanzamos el servidor web"""
    app = web.Application()
    app['status'] = Status().load()
    app.router.add_route('*', '/', StatusAPI)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app)


if __name__ == "__main__":
    server()
