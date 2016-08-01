#!/usr/bin/env python

from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import (
    NOT_DONE_YET,
    Site,
)

from regex import prepathurl__protocol_host

class APICall(Resource):
    def allow_host(self, request):
        url = request.prePathURL()
        protocol, host = prepathurl__protocol_host.match(url).groups()

        request.setHeader("Access-Control-Allow-Origin", protocol + host)

class ChatSpawner(APICall):
    isLeaf = True

    def render_GET(self, request):
        request.site.add_user(request)

        request.setHeader("Content-Type", "text/event-stream")
        self.allow_host(request)

        return NOT_DONE_YET

class SendMessage(APICall):
    isLeaf = True

    def render_POST(self, request):
        self.allow_host(request)
        request.site.send_message(request.args["message".encode()][0])

        return "".encode()

class Root(Resource):
    def __init__(self):
        super().__init__()

        self.putChild("chat-spawner".encode(), ChatSpawner())
        self.putChild("send-message".encode(), SendMessage())

class Server(Site):
    def __init__(self, root):
        self._users = []

        super().__init__(root)

    def add_user(self, user):
        self._users.append(user)

    def send_message(self, message):
        message = message.decode()
        for user in self._users[:]:
            try:
                data = "data: {message}\r\n\r\n".format(**locals())
                user.write(data.encode())
            except AttributeError:  # Disconnected
                self._users.remove(user)

factory = Server(Root())
reactor.listenTCP(10194, factory)

reactor.run()
