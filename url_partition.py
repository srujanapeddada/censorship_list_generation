#!/usr/bin/python3
'''
Create lists of URLs from a set of urls and the outgoing links from those pages
Partition URLs in to path and server components and create lists for the following
9 combinations - (same_domain, same_host, differnt_domain) x (root, depth = 1, depth > 1)

Also create lists based on the absolute depth of the path
'''

from urlparse import urlsplit
from publicsuffix import get_public_suffix

class ClassifiedPaths:
    def __init__(self):
        self.root = []
        self.depth_one = []
        self.deeper = []
        # Temp: create list by depth
        self.by_depth = {}

    def add (self, link):
        link_url = urlsplit(link)
        depth = link_depth (link_url.path)
        # check if it's root
        if depth == 0:
            self.root.append(link)
        elif depth == 1:
            self.depth_one.append (link)
        # depth > 1
        else: 
            self.deeper.append (link)
        if (depth not in self.by_depth): self.by_depth[depth] = []
        self.by_depth[depth].append(link)

class ClassifiedUrls:
    def __init__(self, page):
        self.page_url = urlsplit (page)
        self.same_domain = ClassifiedPaths()
        self.same_host = ClassifiedPaths()
        self.diff_domain = ClassifiedPaths()

    def add_link (self, link):
        link_url = urlsplit (link)
        # Same domain
        if self.page_url.hostname == link_url.hostname:
            self.same_domain.add(link)
        # Subdomains of same second-level domain
        elif get_public_suffix(self.page_url.hostname) == get_public_suffix(link_url.hostname):
            self.same_host.add (link)
        # Different Domain
        else:
            self.diff_domain.add (link)

# absolute depth of link path
def link_depth (path):
        if (path == "/" or path == ""):
                return 0;
        else: 
          return path.count ("/")

def create_lists(orig_url, links):
        lists = ClassifiedUrls(orig_url)
        for link in links:
                lists.add_link (link)

create_lists ("http://www.yamc.info/", ["http://www.parallels.com/",
"http://www.parallels.com/intro",
"http://www.parallels.com/products/automation/intro",
"http://www.parallels.com/products/containers/intro",
"http://www.parallels.com/products/desktop/intro",
"http://www.parallels.com/products/desktop/pd4wl/intro",
"http://www.parallels.com/products/panel/intro",
"http://www.parallels.com/products/server/intro",
"http://yamc.info/test/fcgi/test.html",
"http://yamc.info/test/perl/test.html",
"http://yamc.info/test/php/test.html",
"http://yamc.info/test/python/test.html",
"http://yamc.info/test/ssi/test.html", "https://yamc.info:8443/"])


