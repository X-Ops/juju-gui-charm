# This file is part of the Juju GUI, which lets users view and manage Juju
# environments within a graphical interface (https://launchpad.net/juju-gui).
# Copyright (C) 2013 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Juju GUI server test utilities."""

from tornado import (
    concurrent,
    gen,
    websocket,
)

from guiserver import clients


class EchoWebSocketHandler(websocket.WebSocketHandler):
    """A WebSocket server echoing back messages."""

    def initialize(self, close_future):
        """The given future will be fired when the connection is terminated."""
        self._closed_future = close_future

    def on_message(self, message):
        self.write_message(message, isinstance(message, bytes))

    def on_close(self):
        self._closed_future.set_result(None)


class WebSocketClient(clients.WebSocketClient):
    """Used to test the guiserver.clients.WebSocketClient."""

    _message_received_future = None

    def send(self, *args, **kwargs):
        super(WebSocketClient, self).send(*args, **kwargs)
        self._message_received_future = concurrent.Future()
        return self._message_received_future

    def write_message(self, *args, **kwargs):
        super(WebSocketClient, self).write_message(*args, **kwargs)
        self._message_received_future = concurrent.Future()
        return self._message_received_future

    def received_message(self, message, *args, **kwargs):
        super(WebSocketClient, self).received_message(message, *args, **kwargs)
        self._message_received_future.set_result(message.data)


class WSSTestMixin(object):
    """Add some helper methods for testing secure WebSocket handlers."""

    def get_wss_url(self, path):
        """Return an absolute secure WebSocket url for the given path."""
        return 'wss://localhost:{}{}'.format(self.get_http_port(), path)
