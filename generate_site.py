#!/usr/bin/env python

import os
import sys
import yaml
from random import choice

from django.conf import settings
from django.template import Context
from django.template.loader import get_template

if len(sys.argv) < 3:
    print 'Usage: python generate_site.py [site_name] [port]'
    sys.exit(-1)

site_name, port = sys.argv[1], sys.argv[2]
current_dir = os.path.dirname(os.path.realpath(__file__))

settings.configure(
    TEMPLATE_DIRS=(current_dir,),
)

fh = open('conf.yaml', 'r')
config = yaml.load(fh)
config = config['settings']
fh.close()

secret_key = secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
config.update({
    'site_name': site_name,
    'port': port,
    'local': False,
    'secret_key': secret_key
})

context = Context(config)

def write_template(template_name, dest, context):
    t = get_template(template_name)
    contents = t.render(context)
    f = open(dest % context, 'w')
    print "Writing %s" % (dest % context)
    f.write(contents)
    f.close()

# create the directory structure for the site
try:
    os.makedirs('%(base_site)s%(site_name)s.com/%(site_name)s/apache/' % context)
    os.makedirs('%(base_site)s%(site_name)s.com/%(site_name)s/media/' % context)
    os.makedirs('%(base_site)s%(site_name)s.com/%(site_name)s/templates/' % context)
    os.makedirs('%(base_site)s%(site_name)s.com/logs/' % context)
    os.makedirs('%(base_site)s%(site_name)s.com/private/' % context)
except OSError:
    pass

# load mapping of template -> destination file
mapping = {
    'settings.py.conf': '%(base_site)s%(site_name)s.com/%(site_name)s/settings.py',
    'urls.py.conf': '%(base_site)s%(site_name)s.com/%(site_name)s/urls.py',     
    'manage.py.conf': '%(base_site)s%(site_name)s.com/%(site_name)s/manage.py',
    'empty.conf': '%(base_site)s%(site_name)s.com/%(site_name)s/__init__.py',
    'empty.conf': '%(base_site)s%(site_name)s.com/logs/apache_error.log',
    'empty.conf': '%(base_site)s%(site_name)s.com/logs/apache_access.log',
    'empty.conf': '%(base_site)s%(site_name)s.com/logs/nginx_error.log',
    'empty.conf': '%(base_site)s%(site_name)s.com/logs/nginx_access.log',
    'wsgi.conf': '%(base_site)s%(site_name)s.com/%(site_name)s/apache/%(site_name)s.wsgi',
    'apache.conf': '%(base_site)s%(site_name)s.com/apache_%(site_name)s.com',
    'nginx.conf': '%(base_site)s%(site_name)s.com/nginx_%(site_name)s.com',
    'hosts.conf': '%(base_site)s%(site_name)s.com/hosts',
    'ports.conf': '%(base_site)s%(site_name)s.com/ports.conf'
}

# mapping of template -> destination file for local dev settings
local_mapping = {
    'apache.conf': '%(base_site)s%(site_name)s.com/local_apache_%(site_name)s.com',
    'nginx.conf': '%(base_site)s%(site_name)s.com/local_nginx_%(site_name)s.com',
    'hosts.conf': '%(base_site)s%(site_name)s.com/local_hosts',
}

# write all files
for template_name, destination in mapping.items():
    write_template(template_name, destination, context)

# write local versions of the config files
context['local'] = True
for template_name, destination in local_mapping.items():
    write_template(template_name, destination, context)

print 'Creating database %(site_name)s_main' % context
os.system('createdb %(site_name)s_main' % context)
os.system('chmod 755 %(base_site)s%(site_name)s.com/%(site_name)s/manage.py' % (context))

print 'Copying media directory'
os.system('cp -R ./media/* %(base_site)s%(site_name)s.com/%(site_name)s/media/' % (context))

print 'Done!'
