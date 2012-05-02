from recipe import Recipe
import os
import urllib2
import re

class Node(Recipe):
    def __init__(self, user):
        super(Node, self).__init__(user)
        self.message('installing node')
        self.dir_local = os.path.join(self.home, 'local')
        self.dir_build = os.path.join(self.temp, 'node')
        self.version = self.node_version()
        self.filename = 'node-%s.tar.gz' % self.version
        self.url = 'http://nodejs.org/dist/latest/' + self.filename

    def execute(self):
        self.progress('adding paths to .bashrc')
        filename = os.path.join(self.home, '.bashrc')
        self.append_text(filename, 'export PATH=$HOME/local/bin:$PATH')
        self.download_and_install()

    def node_version(self):
        """Fetch the latest version string in a form like 'v0.6.16'"""
        html = urllib2.urlopen('http://nodejs.org/dist/latest/').read()
        return re.search(r'>node-(.*)\.tar\.gz<', html).group(1)

    def is_valid(self):
        return True

    def download_and_install(self):
        self.run('rm -rf ' + self.dir_local, False)
        self.run('rm -rf ' + self.dir_build, False)
        self.run('mkdir -p ' + self.dir_local, False)
        self.run('mkdir -p ' + self.dir_build, False)

        cwd = os.getcwd()

        self.progress('fetching')
        os.chdir(self.dir_build)
        self.wget(self.url, False)
        self.run('tar xzvf ' + self.filename, False)
        os.chdir(os.path.join(self.dir_build, 'node-' + self.version))
        self.run('./configure --prefix=' + self.dir_local, False)

        self.progress('building')
        self.run('make install', False)

        self.progress('cleaning up')
        self.run('rm -rf ' + self.dir_build, False)

        os.chdir(cwd)
