import os
import os.path

from fabric.colors import *
from fabric.api import *

env.warn_only = True

NODE_VERSION = "0.8.14"
NODE_URL = "https://github.com/joyent/node/archive/v%s.zip" % NODE_VERSION


def exists_exe(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def exists_file(filename):
    return os.path.exists(filename)


def syncdb():
    local('./manage.py syncdb')
    local('./manage.py migrate')


@task
def install():
    """ Installs all requirements """

    # virtualenv activado
    if 'VIRTUAL_ENV' not in os.environ:
        exit(red("ERROR: you must activate the virtualenv first!"))
    VIRTUAL_ENV = os.environ['VIRTUAL_ENV']

    # requerimientos
    print(green("Check exists files ..."))
    for c in ["git", "wget", "make"]:
        if not exists_exe(c):
            exit(red("ERROR: install " + c))

    # directorio temporal
    if not exists_file("_tmp"):
        local("mkdir _tmp")

    # node
    if not exists_file('../bin/npm'):
        print(green("Install NODE.js ..."))
        if not exists_file("_tmp/node.zip"):
            print(green("Download node..."))
            local("wget %s -O _tmp/node.zip" % NODE_URL)

        local('cd _tmp && unzip node.zip')
        local('cd _tmp/node-%s && ./configure --prefix="%s"' % (NODE_VERSION, VIRTUAL_ENV))
        local('cd _tmp/node-%s && make' % NODE_VERSION)
        local('cd _tmp/node-%s && make install' % NODE_VERSION)

    # lessc
    if not exists_exe('lessc'):
        print(green("Install less..."))
        local('npm install less -g')

    # coffe
    if not exists_exe('coffee'):
        print(green("Install coffescript..."))
        local('npm install coffee-script -g')

    # borramos temp
    local('rm -rf _tmp')

    # downloads
    execute(download_static_files)

    # bootstrap
    if not exists_file('_static/js/bootstrap.min.js'):
        execute(reset_bootstrap)

    # requeriments
    execute(requirements)

    # others
    local("chmod +x manage.py")


@task
def reset_bootstrap():
    """ Update bootstrap install """
    print(green("Install Bootstrap..."))

    if not exists_file("_tmp"):
        local("mkdir _tmp")

    local('rm -rf _static/bootstrap')
    local('mkdir _static/bootstrap')
    local('rm -rf _tmp/*')

    local('git clone https://github.com/twitter/bootstrap.git _tmp/bootstrap')
    local('rm -rf _tmp/bootstrap/.git')

    local('cp -r _tmp/bootstrap/js _static/bootstrap/js')
    local('rm -rf _static/bootstrap/js/tests _static/bootstrap/js/.jshintrc')
    local('cp -r _tmp/bootstrap/less _static/bootstrap/less')
    local('rm -rf _static/bootstrap/less/tests')
    local('cp -r _tmp/bootstrap/img _static/bootstrap/img')

    local('npm install recess connect uglify-js@1 jshint -g')
    local('cd _tmp/bootstrap && make')


@task
def requirements():
    """ Install requirements """
    print(green("Install requirements..."))
    local('pip install -r requirements.txt')


@task
def download_static_files():
    """ Download files """
    if not exists_file('_static/js/jquery.js'):
        print(green("Download JQuery..."))
        local('wget -qO _static/js/jquery.js http://code.jquery.com/jquery.js')
        local('wget -qO _static/js/jquery.min.js http://code.jquery.com/jquery.min.js')
