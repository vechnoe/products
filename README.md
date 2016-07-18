Products
========
Simple e-commerce application

Installation
------------
Make sure that the redis is running on port 6379 and 
the redis-server version >= 2.6.0,
otherwise comment out 'cacheops' INSTALLED_APPS

Create postgress db & db user:

```
postgres=# CREATE USER products_user WITH password '12345';
postgres=# ALTER USER products_user CREATEDB;
postgres=# CREATE DATABASE products;
GRANT ALL privileges ON DATABASE products TO products_user;
```

After db creation:

```
$ git clone git://github.com/vechnoe/products
$ cd products
$ make
$ make run
```

Your server starts on *127.0.0.1:8000*

Admin login: *admin*
Admin password: *12345*

All the  users have password: *12345*




