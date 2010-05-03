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

file_mapping = config['files']
local_file_mapping = config['local_files']
directories = config['directories']

config = config['settings']
fh.close()

secret_key = secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
config.update({
    'site_name': site_name,
    'port': port,
    'local': False,
    'secret_key': secret_key,
})
config.update({
    'site_root': directories['site_root'] % config,
    'wsgi': directories['wsgi'] % config,
    'media': directories['media'] % config,
    'templates': directories['templates'] % config,
    'logs': directories['logs'] % config
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
    for directory in directories.values():
        os.makedirs(directory % context)
except OSError:
    pass

# write all files
for destination, template_name in file_mapping.items():
    write_template(template_name, destination, context)

# write local versions of the config files
context['local'] = True
for destination, template_name in local_file_mapping.items():
    write_template(template_name, destination, context)

print 'Creating database %(site_name)s_main' % context
os.system('createdb %(site_name)s_main' % context)

print 'Copying media directory'
os.system('cp -R ./media/* %(media)s' % (context))

print 'Done!'
