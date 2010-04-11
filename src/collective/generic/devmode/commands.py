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
import logging
import os
import sys

def change_mails(app, plone, mail, **kwargs):
    import transaction
    logger = logging.getLogger('collective.generic.devmode.change_mails')
    logger.info('start')
    pc = plone.portal_catalog
    pp = plone.portal_properties
    pm = plone.portal_membership
    new_email = mail
    if not new_email: raise Exception
    portal = plone
    portal.email_from_address = new_email
    members = pm.listMembers()
    total = len(members)
    for index, member in enumerate(members):
        member.setMemberProperties({"email": new_email})
        if ((index<10)
            or ((index<100) and index % 10 == 0)
            or (index % 100 == 0)):
            logger.info('Changed email of %s users / %s' % (index+1, total))
            transaction.commit()
    transaction.commit()
    logger.info("users has lost their email. "
                "Emails has been setted to %s"%(mail))
 
    logger.info('end')


def get_startup_cmd(zope_conf, python, more, pyflags=""):
    from Zope2.Startup import zopectl

    # If we pass the configuration filename as a win32
    # backslashed path using a ''-style string, the backslashes
    # will act as escapes.  Use r'' instead.
    # Also, don't forget that 'python'
    # may have spaces and needs to be quoted.
    pypath = ''
    for entry in sys.path:
        pypath += "import sys;sys.path.insert(0,'%s');" % entry
    cmdline = ( '"%s" %s -c "%sfrom Zope2 import configure; '
               'configure(r\'%s\'); ' %
               (python, pyflags, pypath, zope_conf)
              )
    cmdline = cmdline + more + '\"'
    if getattr(zopectl, 'WIN', False):
        # entire command line must be quoted
        # as well as the components
        return '"%s"' % cmdline
    else:
        return cmdline


def run_script(zope_conf, site_id, user, script, script_args, **kwargs):
    """ The runned script will have app -> zope2 root and plone -> plonsite
    registered as globals."""
    logger = logging.getLogger('collective.generic.devmode.run_scripts')
    logger.info('start')

    # cowardly adapted from 
    # http://svn.plone.org/svn/collective/buildout/plone.recipe.zope2instance/trunk/src/plone/recipe/zope2instance/ctl.py

    zopecmd = 'import sys; sys.argv.pop();sys.argv.append(r\'%s\');'  % script
    argv = [a for a in script_args.strip().split() if a]
    zopecmd = ''
    if argv :
        zopecmd += '[sys.argv.append(x) for x in %s]; ' % argv
    zopecmd += 'import Zope2; app=Zope2.app();'
    zopecmd += 'from collective.generic.devmode.common import get_live;'
    zopecmd += "app, plone = get_live('%s', '%s', '%s');" % (zope_conf, site_id, user)
    zopecmd += 'execfile(r\'%s\')' % script
    cmd = get_startup_cmd(zope_conf, sys.executable, zopecmd)
    exitstatus = os.system(cmd)
    sys.exit(exitstatus)
    logger.info('end')


def change_admin_password(app, plone, admin, password, **kwargs):
    import transaction
    logger = logging.getLogger('collective.generic.devmode.change_admin_password')
    logger.info('start')
    add_or_updated = ''
    try:
        app.acl_users.users.manage_addUser(admin, 'manager', password, password)
        add_or_updated = 'added'
    except KeyError:
        add_or_updated = 'updated'
        pass 
    app.acl_users.users.manage_updateUserPassword(admin, password, password)
    app.acl_users.users.manage_updateUserPassword(admin, password, password)
    app.acl_users.roles.assignRoleToPrincipal('Manager', admin)
    logger.info(
        "An user called '%s' with your password "
        "had been %s with the role 'Manager'." % (
            admin, add_or_updated
        )
    ) 
    transaction.commit() 
    logger.info('end')

def change_password(app, plone, password, **kwargs):
    import transaction
    logger = logging.getLogger('collective.generic.devmode.change_password')
    logger.info('start')
    p = plone.portal_membership
    users = plone.acl_users.source_users
    ids = users.getUserIds()
    total = len(ids)
    for index, id in enumerate(ids):
        users.doChangeUser(id, password)
        if ((index<10)
            or ((index<100) and index % 10 == 0)
            or (index % 100 == 0)):
            logger.info('Changed passwords of %s users / %s' % (index+1, total))
            transaction.commit() 
    transaction.commit() 
    logger.info('All passwords had been updated to %s.' % password)
    logger.info('end')


# vim:set et sts=4 ts=4 tw=80:
