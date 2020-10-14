"""This app manages activity logs : things that we want to see in
Django admin and for which we want a log entry in the database.

This is essentially a wrapper around the Django Activity Stream app
that gives us a way to log a database entry for an arbitrary action.
"""
default_app_config = 'logs.apps.LogsConfig'
