#!/usr/bin/env python2.7
# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

from operator import methodcaller
import sys

from six.moves import input, map, range

from boxsdk.network.dev_vm_network import LiveOrDevVMOAuth2, OAuthClient

dev_vm_name = None
while not dev_vm_name:
    dev_vm_name = input('dev vm name: ')

oauths = []

while True:
    if oauths:
        y_or_n = input('Add another user? [y]/n: ')
        if y_or_n.lower() in ['n', 'no']:
            break
    refresh_token = input('Refresh token? ')
    if refresh_token:
        oauth = LiveOrDevVMOAuth2(dev_vm_name=dev_vm_name, refresh_token=refresh_token)
        oauth.refresh(None)
    else:
        oauth = LiveOrDevVMOAuth2(dev_vm_name=dev_vm_name)
        print('Open this url in your web browser, do login:', oauth.get_authorization_url('http://localhost')[0])
        auth_code = input("Quickly copy-paste the 'code' here: ")
        oauth.authenticate(auth_code)
    oauths.append(oauth)

try:
    try:
        clients = list(map(OAuthClient, oauths))

        users = list(map(methodcaller('get'), map(methodcaller('user'), clients)))

        event_endpoints = list(map(methodcaller('events'), clients))

        manual_pollings = list(map(methodcaller('generate_event_lists_with_manual_polling'), event_endpoints))

        while True:
            for i, user in enumerate(users):
                events = next(manual_pollings[i])
                if events:
                    print()
                    print(user.login)
                    for event in events:
                        print(event)
                    print()
    except BaseException:
        print()
        print('Refresh tokens:')
        for oauth in oauths:
            print(oauth._refresh_token)
        print()
        raise
except Exception:
    raise
except BaseException:
    raise BaseException
