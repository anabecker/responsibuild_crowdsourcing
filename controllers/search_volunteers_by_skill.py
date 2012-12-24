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
from controllers.check_login import check_login
from controllers.show_error_html import show_error_html



def search_volunteers_by_skill(self):
    logging.debug("show_index_html")
    session = get_current_session()
    staff_boolean = False
    try:
        staff_boolean = session['staff']
    
    except:
        staff_boolean = False
        
    if staff_boolean:
        construction = self.request.get("construction")
        mold_remediation = self.request.get("mold_remediation")
        chainsaw = self.request.get("chainsaw")
        leadership = self.request.get("leadership")
        #q = GqlQuery(SELECT * FROM Member WHERE skill_list IN 'Betty', 'Charlie')
        #q = GqlQuery(SELECT * FROM Member)
        search_string = "SELECT * FROM Member WHERE "
        variable_string = ""
        if chainsaw:
            search_string = search_string + "skill_list = :chainsaw"
        
       
        q = db.GqlQuery(search_string, chainsaw = chainsaw, email = "none")
        results = q.fetch(1000)
        for result in results:
            print result.email
        results2 = q.fetch(1000)
        results.extend(results2)
        
        for result in results:
            print 3
            
            
        # Learn GQL IN method, maybe this will help you
        
        
    
    
    else:
        pass