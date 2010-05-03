django-site-gen
===============

a utility script for generating skeleton django sites

it's still pretty tied to my workflow, so check back as I hope to be
making it more generic.


What it creates
---------------

assuming a base directory of /home/user/public_html/, django-site-gen
will create the following when executed like so::

    python generate_site.py twitter 9001

* ~/public_html/twitter.com/twitter/ - the root directory of django site
* ~/public_html/twitter.com/twitter/apache/ - where the wsgi file lives
* ~/public_html/twitter.com/twitter/media/ - site media served by nginx
* ~/public_html/twitter.com/logs/ - where the apache and nginx logs live
* ~/public_html/twitter.com/ - apache and nginx confs for local and production


The setup is based on the setup described by the following two tutorials:

* http://lethain.com/entry/2009/feb/13/the-django-and-ubuntu-intrepid-almanac/
* http://www.meppum.com/2009/jan/17/installing-django-ubuntu-intrepid/
