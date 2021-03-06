from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from gaesessions import get_current_session
import logging
import model
import urllib
from google.appengine.ext import db
import random
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from os import environ
from google.appengine.api import memcache
from google.appengine.api import images
from google.appengine.api import oauth
import Cookie
import hashlib
from models import model
from controllers.datastore_results import datastore_results



def check_post_duplicates(post_id):
    logging.debug("check_post_duplicates")
    session = get_current_session()
    email = session['email']
    filters = {
        "email": email,
        "post_id": post_id,
    }
    results, results_exist = datastore_results("Post", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
    if not results_exist:
        return False
    
    for result in results:
        key = result.key()
        return key