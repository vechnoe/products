Products
========
Simple e-commerce application


Installation
------------
Create postgress db & db user:

```
postgres=# CREATE USER test_user WITH password '12345';
postgres=# ALTER USER products_user CREATEDB;
postgres=# CREATE DATABASE products;
GRANT ALL privileges ON DATABASE products TO test_user;
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




