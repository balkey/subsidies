# -*- coding: utf-8 -*-

from __future__ import print_function
import requests, math, time, requesocks, socket, sys, time
from random import shuffle, randint
from models import *

USERNAME = 'user'

class Data(object):

    SUCCESS_COUNT = 0
    ERROR_COUNT = 0
    LOCK_LIMIT = 25

    def __init__(self):

        self.force = Force()
        current_ip = Tor.getip_requests()
        print(u'Current computer\'s IP: {}'.format( current_ip ) )
        session = Tor.renew_identity()
        print(u'')
        print(u'')
        self.force.session = session

    def startMigrate( self ):

        sq = DBSession.query( Object.id ) \
            .filter( Object.is_finished == False ) \
            .filter( Object.is_locked_by == None ) \
            .order_by( func.random() ) \
            .limit( self.LOCK_LIMIT ) \
            .all()

        DBSession.query( Object ) \
            .filter( Object.id.in_( sq ) ) \
            .update({ 'is_locked_by': USERNAME }, synchronize_session = 'fetch' )

        DBSession.commit()

        obj = DBSession.query( Object ) \
            .filter( Object.is_locked_by == USERNAME ) \
            .filter( Object.is_finished == False ) \
            .all()

        print('[Lock %d street]' % ( len( obj ) ) )
        if len( obj ) == 0:
            return

        for o in obj:
            # TODO script: make request
            print(o)

        self.startMigrate()


class Force(object):

    session = None
    BASE_URL = ""

    def getNewIdentity( self ):

        Data.ERROR_COUNT = 0
        Data.SUCCESS_COUNT = 0
        session = Tor.renew_identity()
        if session is not None:
            self.session = session

    def createRequest(self, message):

        if Data.ERROR_COUNT > 3 or Data.SUCCESS_COUNT > 100:
            self.getNewIdentity()

        try:
            r = self.session.get( self.BASE_URL ), timeout=5 )
            Data.SUCCESS_COUNT += 1
            return txt

        except socket.timeout or requesocks.packages.urllib3.packages.socksipy.socks.Socks5Error or requesocks.exceptions.Timeout or requests.exceptions.Timeout:
            Data.ERROR_COUNT += 1
            return None

        except:
            self.getNewIdentity()
            return None

class Tor( object ):

    CHECK_URL = "http://ipinfo.io/ip"
    PASS_AUTH = "foobar"

    @classmethod
    def getip_requests( cls ):
        r = requests.get( cls.CHECK_URL )
        return r.text.replace("\n", "")

    @classmethod
    def getip_requesocks( cls ):
        session = requesocks.session()
        session.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }

        r = session.get( cls.CHECK_URL )
        return session, r.text.replace("\n", "")

    @classmethod
    def renew_identity( cls ):

        try:
            s = socket.socket()
            s.connect(('localhost', 9051))
            s.send('AUTHENTICATE "{0}"\r\n'.format( cls.PASS_AUTH ))
            resp = s.recv(1024)

            if resp.startswith('250'):
                s.send("signal NEWNYM\r\n")
                resp = s.recv(1024)

                if resp.startswith('250'):
                    session, ip = cls.getip_requesocks()
                    print( "[{}] ".format( ip ), end = '' )
                    return session

        except Exception as e:
            print( "[?] ", end = '' )

        return None