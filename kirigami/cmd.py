#
# Copyright (c) 2016 Dennis Chen
# Copyright (c) 2016 Vijay Pillai
#
# This file is part of Kirigami
#
# Kirigami is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Kirigami is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Kirigami.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import os.path
import socket
import sys

import kirigami.tagger
import kirigami.settings
from .handlers import *
from .connection import Remote


def main(r, settings):
    r.clear_auth()
    while True:
        logging.debug('Getting Actions from Remote.')
        try:
            actions = r.pending_actions()
        except socket.timeout as e:
            logging.warn('Connection timed out.')
            actions = None

        if actions:
            for action in actions:
                logging.debug('Recieved Action %s', action)
                try:
                    controller(action)(r, settings, logging)
                except socket.timeout as e:
                    logging.warn('Connection timed out.')


def controller(event):
    events = {
        'AuthenticationRequested': auth_handler,
        'UserMessages': message_handler,
        'AuthenticationExpired': expiration_handler,
        'BalanceUpdate': balance_handler
    }
    return events.get(event, bug_handler)


def cli():
    log = {
        'format': '%(asctime)s - %(levelname)s %(message)s',
        'level': logging.DEBUG
    }
    logging.basicConfig(**log)

    logging.info('Parsing Configuration from kirigami.conf')
    settings = kirigami.settings.parse_config(
        os.path.expanduser('kirigami.conf'), logging)

    identity = kirigami.tagger.identity(settings['main']['user'])
    logging.debug('Identity tagged as %s', identity)

    r = Remote(settings['main'], identity)

    try:
        main(r, settings)
    except KeyboardInterrupt:
        print('Exiting...')
