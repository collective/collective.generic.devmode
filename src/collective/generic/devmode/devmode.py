import os
import sys
import optparse
import logging

import common
import commands


DEFAULT_USER = 'admin'
usage = """
"""

def get_default_zope_conf():
    if 'INSTANCE_HOME' in os.environ:
        return os.path.join(os.environ['INSTANCE_HOME'], 'etc', 'zope.conf')
    else:
        candidates = [
            os.path.join(os.path.dirname(os.path.dirname(sys.argv[0])), 'parts', 'instance', 'etc', 'zope.conf'),
            os.path.join('parts', 'instance', 'etc', 'zope.conf')]
        for candidate in candidates:
            if os.path.exists(candidate):
                return candidate

def main():
    parser = optparse.OptionParser(usage=usage)

    actions = [
        optparse.make_option('-a', '--change-admin-password',
                             action='store_true', dest='change_admin_password',
                             default = False,
                             help = 'Change password from only the admin users to the given --password password '), 
        optparse.make_option('-m', '--change-mails',
                             action='store_true', dest='change_mails',
                             default = False,
                             help = 'Change password from all users to the given --mail mail'),
        optparse.make_option('-p', '--change-password',
                             action='store_true', dest='change_password',
                             default = False,
                             help = 'Change password from all users to the given --password password including the admin user (-a)'),
        optparse.make_option('-s', '--run-script',
                             action='store_true', dest='run_script',
                             default = False,
                             help = 'Run a wrapper around bin/instance run <SCRIPT> (given via --script) to remove any security in a zope2/plone site'),
    ]

    modifiers = [
        optparse.make_option('--mail',
                             action='store', dest='mail',
                             default = 'foo@foo.com',
                              help = 'New mail'),
        optparse.make_option('--password',
                             action='store', dest='password',
                             default = 'secret',
                             help ='New password'), 
        optparse.make_option('--script',
                             action='store', dest='script',
                             help = 'script to use'), 
        optparse.make_option('-c', '--config',
                             action='store', dest='zope_conf',
                             default = get_default_zope_conf(),
                             help = 'Zope configuration file to use'),
        optparse.make_option('-u', '--user',
                             action='store', dest='user',
                             default = DEFAULT_USER,
                             help = 'Admin user to use instead of %s.' % DEFAULT_USER), 
        optparse.make_option('-l', '--site-id',
                             action='store', dest='site_id',
                             default = 'plone',
                             help = 'Plone Site id'), 
        optparse.make_option('--script-args',
                             action='store', dest='script_args',
                             default = '',
                             help = 'Arguments to give to the script if any'),  
    ]

    flags = [
        optparse.make_option('-v', '--verbose',
                             action='store_true', dest='verbose',
                             default = False,
                             help = 'Be verbose'), 
    ]

    actions_group = optparse.OptionGroup(parser, 'Actions')
    modifiers_group = optparse.OptionGroup(parser, 'Modifiers')
    flags_group = optparse.OptionGroup(parser, 'Flags')
    [[group.add_option(o) for o in opts]
     for group, opts in [(actions_group, actions),
                         (modifiers_group, modifiers),
                         (flags_group, flags)]
    ]
    [parser.add_option_group(group)
     for group in [actions_group, modifiers_group, flags_group]]
    (options, args) = parser.parse_args()
    command_options = {
        'zope_conf': options.zope_conf,
        'user': options.user,
    }

    common.init_logging(options.verbose)
    if options.change_mails:
        app, plone = common.get_live(options.zope_conf, 
                                     options.site_id, 
                                     options.user)
        commands.change_mails(app, plone, options.mail)

    if options.change_admin_password:
         app, plone = common.get_live(options.zope_conf, 
                                      options.site_id, 
                                      options.user)
         admin, password = options.user, options.password
         commands.change_admin_password(app, plone, admin, password)

    if options.change_password:
         app, plone = common.get_live(options.zope_conf, 
                                      options.site_id, 
                                      options.user)
         admin, password = options.user, options.password
         commands.change_admin_password(app, plone, admin, password)
         commands.change_password(app, plone, password)

    if options.run_script:
        commands.run_script(options.zope_conf,
                            options.site_id,
                            options.user,
                            options.script, 
                            options.script_args)

