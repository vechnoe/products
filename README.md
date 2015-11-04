Products
========
Simple e-commerce application


Installation
------------
Create postgress db & user:

```
postgres=# CREATE USER test_user WITH password '12345';
postgres=# CREATE DATABASE products;
GRANT ALL privileges ON DATABASE products TO test_user;
```

After db creation:

```
$ git clone git://github.com/vechnoe/products
$ make
$ make run
```

Your server starts on *127.0.0.1:8000*

Admin login: *admin*
Admin password: *12345*

All the  users have password: *12345*




