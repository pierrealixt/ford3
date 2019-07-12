# FORD3 

[![FORD Screenshot](http://ford3.kartoza.com)](http://ford3.kartoza.com)


A django app for creating publishing open education program data for South Africa.

View a running instance at [http://ford3.kartoza.com](http://ford3.kartoza.com)


Note that whilst usable, Ford3 is under continual development and not
yet feature complete.

The latest source code is available at 
[https://github.com/kartoza/ford3](https://github.com/kartoza/ford3).

* **Developers:** See our [developer guide](README-dev.md)
* **For production:** See our [deployment guide](README-docker.md)


## Key features

* An clean, easy to use API for discovering courses, institutions etc. from educational facilities in South Africa
* A backend administration system for educational institutions to maintain their own data

## Project activity

* Current test status master: [![Build Status](https://api.travis-ci.com/kartoza/ford3.svg?branch=master)](https://travis-ci.com/kartoza/ford3) and
[![Code Health](https://landscape.io/github/kartoza/ford3/master/landscape.svg?style=flat)](https://landscape.io/github/kartoza/ford3/master)

* Current test status develop: [![Build Status](https://api.travis-ci.com/kartoza/ford3.svg?branch=develop)](https://travis-ci.org/kartoza/ford3) and
[![Code Health](https://landscape.io/github/kartoza/ford3/develop/landscape.svg?style=flat)](https://landscape.io/github/kartoza/ford3/develop)

* Test coverage [![codecov](https://codecov.io/gh/kartoza/ford3/branch/develop/graph/badge.svg)](https://codecov.io/gh/kartoza/ford3)

## Quick Installation Guide

For deployment we use [docker](http://docker.com) so you need to have docker 
running on the host. Ford3 is a django app so it will help if you have
some knowledge of running a django site.

To run the project locally, there are four steps:
1. Build the images and set up the docker env
2. Populate initial data
3. Run the server
4. Open browser

### 1. Build the images and set up the docker for the project

Clone the repo
```
git clone git://github.com/kartoza/ford3.git
```

- We will use Makefile script available under deployment folder.
- Any `make` commands should be run under deployment folder.


```
cd ford3/deployment
cp btsync-db.env.EXAMPLE btsync-db.env
cp btsync-media.env.EXAMPLE btsync-media.env
make build
make permissions
make web
# Wait a few seconds for the DB to start before to do the next command
make migrate
make collectstatic
```

### 2. Populate initial Data
#### Add superuser
Admin user is required to administer the site.
To add admin:

```
cd deployment
make superuser
# write your usename, email, and password
```

#### Add initial data
```
cd deployment
make load-initial-data
```

### 3. Run the server
```
cd deployment/ansible/development/group_vars
cp all.sample.yml all.yml
```

- edit line 4 (*use_pycharm*), line 6 (*remote_user*), 8 (*remote_group*), and 10 (*project_path*) in all.yml accordingly
  - make sure that *remote_user* is equal to your local user
  - *remote_group* is likely stay the same if using linux and macOS
  - *project_path* is equal to `/home/web/ford3`

```
cd deployment/ansible
mkdir tmp
cd ..
make setup-ansible
# choose your pycharm version from the list or hit Enter if you don't use pycharm.
```

#### A. From PyCharm Professional
- Open PyCharm
- Notice your pycharm, there should be *Ford3* django server in the toolbar.
  - Wait for a couple of minutes. Make sure the PyCharm has loaded all the necessary files.
  - If pycharm requires to install additional supported modules, click on the provided link
- Click on the `play button` or `debug button` next to *Ford3* instance in the toolbar. The pycharm will run the server for you
  - sometimes restart pycharm can remedy the problem too
  - If the server doesn't run, try:

```
cd deployment
make down
make up
```


#### B. From CLI
```
cd deployment
make migrate
make up
make shell
python manage.py runserver 0.0.0.0:8080
```

#### 4. Open Browser

- Open browser and type: `http://localhost`
- You have the project running now

## Useful tools for development

These tools are suggested before developers make a pull request to the repo.

###  Coding style

**flake8** is used to make sure the code is aligned with coding style.

```
cd deployment
make flake8
```
- Fix the code if the tool complaint about the coding

### Selenium and django tests

#### Selenium IDE
 In order to run the selenium tests, make sure you have [https://www.seleniumhq.org/selenium-ide/](Selenium IDE) installed.

 The tests assume you have an user with the following credentials:
 - email: admin@admin.com
 - password: admin

 In Selenium IDE, choose the project `selenium-ide/OpenEdu.side` and execute the test suite `Default Suite`. Tests will fail if you run them individually.

 Before running the tests, you must start a local server.
 
#### Django tests
 ```
 cd deployment
 make test
 ```


## Miscellaneous

### Backups

If you don't need backups, you can let the default content.

If you wish to sync backups, you need to establish a read / write btsync 
key on your production server and run one or more btsync clients 
with a read only key.

```
cd deployment
cp btsync-media.env.EXAMPLE btsync-media.env
cp btsync-db.env.EXAMPLE btsync-db.env
```

Now edit the ``btsync-media.env`` and ``btsync-db.env`` files, including 
relevant SECRET and DEVICE settings.

### Render a graphical overview of the app's models

```
cd deployment
make shell
apt-get install graphviz
pip install django-extensions graphviz pyparsing pydot pygraphviz
./manage.py graph_models --pygraphviz -a -g -o openedu_models.png --exclude-models Session,AbstractBaseSession,PostGISSpatialRefSys,PostGISGeometryColumns,EmailConfirmation,SocialToken,LogEntry,EmailAddress,SocialAccount,SocialApp,Site,ContentType
```


## Participation


We work under the philosophy that stakeholders should have access to the
development and source code, and be able to participate in every level of the 
project - we invite comments, suggestions and contributions.  See
[our milestones list](https://github.com/kartoza/ford3/milestones) and
[our open issues list](https://github.com/kartoza/ford3/issues?page=1&state=open)
for known bugs and outstanding tasks. You can also chat live with our developers
and community members using the link below.


## Credits

Ford3 was developed by [Kartoza.com](http://kartoza.com) and 
individual contributors. The project is funded by the [Ford Foundation](http://fordfoundation.org).

## License

Ford3 is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License version 3 (GPLv3) as
published by the Free Software Foundation.

The full GNU General Public License is available in LICENSE.txt or
http://www.gnu.org/licenses/gpl.html


## Disclaimer of Warranty (GPLv3)

There is no warranty for the program, to the extent permitted by
applicable law. Except when otherwise stated in writing the copyright
holders and/or other parties provide the program "as is" without warranty
of any kind, either expressed or implied, including, but not limited to,
the implied warranties of merchantability and fitness for a particular
purpose. The entire risk as to the quality and performance of the program
is with you. Should the program prove defective, you assume the cost of
all necessary servicing, repair or correction.

## Thank you

Thank you to the individual contributors who have helped to build ford3:

* Tim Sutton (Lead developer): tim@kartoza.com
* Dražen Odobašić : dodobas@geoinfo.geof.hr
* George Irwin : github@grvhi.com
* Ismail Sunni : ismail@kartoza.com
* Richard Duivenvoorde : richard@duif.net
* Rischan Mafrur

