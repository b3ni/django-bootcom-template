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


def static():
    # scripts
    local('wget -qO _static/js/jquery.js http://code.jquery.com/jquery.js')
    local('wget -qO _static/js/jquery.min.js http://code.jquery.com/jquery.min.js')
    local('wget -qO _static/js/coffee-script.min.js http://coffeescript.org/extras/coffee-script.js')
    local('wget -qO _static/js/less.min.js http://lesscss.googlecode.com/files/less-1.3.0.min.js')

    # bootstrap
    local('rm -rf _static/bootstrap')
    local('git clone https://github.com/twitter/bootstrap.git _static/bootstrap')
    local('rm -rf _static/bootstrap/.git')
    local('make -C _static/bootstrap bootstrap')
    local('cp _static/bootstrap/bootstrap/js/bootstrap.min.js _static/js')


def syncdb():
    local('chmod +x manage.py')
    local('./manage.py syncdb')
    local('./manage.py migrate')


@task
def install():
    # virtualenv activado
    if 'VIRTUAL_ENV' not in os.environ:
        exit(red("ERROR: you must activate the virtualenv first!"))
    VIRTUAL_ENV = os.environ['VIRTUAL_ENV']

    # requerimientos
    print(green("Requeriments ..."))
    for c in ["git", "wget", "make"]:
        if not exists_exe(c):
            exit(red("ERROR: install " + c))

    # directorio temporal
    if not exists_file("_tmp"):
        local("mkdir _tmp")

    # node
    if not exists_exe('npm'):
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

        # local('wget -qO _static/js/less.min.js http://lesscss.googlecode.com/files/less-1.3.0.min.js')

    # coffe
    if not exists_exe('coffee'):
        print(green("Install coffescript..."))
        local('npm install coffee-script -g')

        # local('wget -qO _static/js/coffee-script.min.js http://coffeescript.org/extras/coffee-script.js')

    # borramos temp
    local('rm -rf _tmp')

    # downloads
    if not exists_file('_static/js/jquery.js'):
        print(green("Download JQuery..."))
        local('wget -qO _static/js/jquery.js http://code.jquery.com/jquery.js')
        local('wget -qO _static/js/jquery.min.js http://code.jquery.com/jquery.min.js')

    # bootstrap
    if not exists_file('_static/bootstrap'):
        print(green("Install Bootstrap..."))

        local('npm install recess -g')
        local('npm install uglify-js -g')

        local('git clone https://github.com/twitter/bootstrap.git _static/bootstrap')
        local('rm -rf _static/bootstrap/.git')
        local('make -C _static/bootstrap bootstrap')

        local('cp _static/bootstrap/bootstrap/js/bootstrap.min.js _static/js')
