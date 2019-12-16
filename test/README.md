## Testing

Unfortunately the load sequence is very particular in Flask.

Basically your DB connection has to be setup BEFORE you import any of the model
classes, because it is on module import that they register themselves. So our
tests need to override the db connection string very early.

We do this in fixtures.py and make sure to override the string early before any
other imports.
