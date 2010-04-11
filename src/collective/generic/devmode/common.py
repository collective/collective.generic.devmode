#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010, Mathieu PASQUET <mpa@makina-corpus.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the <ORGANIZATION> nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__docformat__ = 'restructuredtext en'

import os
import sys
import logging

LOG_FORMAT =  "%(asctime)s %(name)-1s %(levelname)-2s - %(message)s"
def init_logging(verbose = False, log_format = LOG_FORMAT):
    level = verbose and logging.DEBUG or logging.INFO
    # logging to stdout
    logging.root.setLevel(level)
    lformatter = logging.Formatter(log_format)
    lhandler = logging.StreamHandler(sys.stdout)
    lhandler.setFormatter(lformatter)
    logging.root.addHandler(lhandler)

def su_plone(app, plone, user):
    logger = logging.getLogger('collective.generic.devmode.su_plone')
    logger.debug('start')
    from AccessControl.SecurityManagement import newSecurityManager
    user = app.acl_users.getUser(user).__of__(plone.acl_users)
    newSecurityManager(None, user)
    logger.debug('end')

def set_component_site(plone):
    from zope.app.component.hooks import setSite
    setSite(plone) 
 
def get_plone(app, site_id):
    logger = logging.getLogger('collective.generic.devmode.get_plone')
    logger.debug('start')
    site = app.unrestrictedTraverse(site_id)
    logger.debug('end')
    return site

def su_zope(app):
    logger = logging.getLogger('collective.generic.devmode.su_zope')
    logger.debug('start')
    from AccessControl.SpecialUsers import system
    from AccessControl.SecurityManagement import newSecurityManager
    newSecurityManager(None, system)
    from AccessControl.SecurityManager import setSecurityPolicy
    from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy
    _policy = PermissiveSecurityPolicy()
    _oldpolicy = setSecurityPolicy(_policy)
    logger.debug('end')

def get_zope(zope_conf):
    """options is an options optparser object."""
    logger = logging.getLogger('collective.generic.devmode.get_zope')
    logger.debug('start')
    os.environ['ZOPE_COMPATIBLE_STARTUP'] = " "
    os.environ['ZOPE_CONFIG'] = zope_conf
    import Zope2
    from Testing.makerequest import makerequest
    app = makerequest(Zope2.app())    
    logger.debug('end')
    return app

def get_live(zope_conf, site_id, user):
    app = get_zope(zope_conf)
    su_zope(app)
    plone = get_plone(app, site_id)
    set_component_site(plone)
    su_plone(app, plone, user)
    return app, plone

# vim:set et sts=4 ts=4 tw=80:
