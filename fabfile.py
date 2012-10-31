from fabric.api import *


def requirements():
    # less coffies
    local('sudo npm install -g less coffeelint')
    local('coffee --version || sudo npm install -g coffee-script')


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


def install():
    execute(requirements)
    execute(static)
    execute(syncdb)
