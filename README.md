django-bootcom-template
=======================

Django Template startproject with bootstrap and node.js inside virtualenv.

Features:

- Bootstrap
- Node (inside virtualenv)
- Lessc (inside virtualenv)
- Coffeescript (inside virtualenv)
- South
- Django Debug Toolbar

Requirements

```bash
$ virtualenv myproject
$ cd myproject
$ source bin/activate
$ pip install django fabric
```

Install

```bash
$ django-admin.py startproject --template https://github.com/b3ni/django-bootcom-template/zipball/master -e py,ini,gitignore,in,conf,md,sample myproject
$ cd myproject
$ fab install
```