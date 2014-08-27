#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jens Neuhalfen'
SITENAME = u'baSSHtion'
SITEURL = 'http://www.basshtion.org'

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('OpenSSH.org', 'http://www.openssh.com/'),
         ('GitHub', 'https://github.com/baSSHtion/'),)

# Social widget
SOCIAL = () # (('You can add links in your config file', '#'),

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME="/home/jens/Documents/projects/baSSHtion/pelican-bootstrap3"
BOOTSTRAP_THEME="slate"

STATIC_PATHS = ['images', 'extra/CNAME', 'extra/LICENSE', 'extra/README.md']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},'extra/LICENSE': {'path': 'LICENSE'},'extra/README.md': {'path': 'README.md'},}
