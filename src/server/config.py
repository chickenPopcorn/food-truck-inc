import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'mysecret'
    MONGO_DBNAME = 'cloudlogin'
    DATABASE_URI = 'mongodb://user:user@ds055626.mlab.com:55626/cloudlogin'
    S3_ACCESS_KEY = 'YOUR_S3_ACCESS_KEY'
    S3_SECRET_KEY = 'YOUR_S3_SECRET_KEY'
    S3_BUCKET_URL = 'YOUR_S3_BUCKET_URL'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
