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

#import netifaces
import socket
import getpass


def identity(preset_user):
    if not preset_user:
        user = getpass.getuser()
    else:
        user = preset_user
    hostname = socket.gethostname()
    ipaddrs = ["127.0.0.1"]
    ip = ','.join(ipaddrs)
    return (user, hostname, ip)


def retrieve_user():
    user = input('Username: ')
    return user


def retrieve_password():
    passwd = getpass.getpass()
    return passwd
