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
from controllers.check_login import check_login
from controllers.show_error_html import show_error_html
from controllers.put_tag import put_tag
from controllers.get_date_time import get_date_time
from controllers.get_hash import get_hash
from controllers.datastore_results import datastore_results
from controllers.comment_minus_one_constraints import comment_minus_one_constraints
import random

def put_comment_minus_one(self):
    logging.debug("put_comment_minus_one")
    if check_login(self):
        continue_boolean = False
        email = ""
        #try:
        session = get_current_session()
        email = session['email']
        continue_boolean = True
        #except:
            #logging.debug("gaesessions exception, do not continue")
            #continue_boolean = False
            #show_error_html(self, "session error")
            
            
        if continue_boolean:
            post_id = self.request.get("post_id")
            comment_id = self.request.get("comment_id")
            comment_email = ""
            
            if comment_minus_one_constraints(self, comment_id):
                    

                filters = {
                    "comment_id": comment_id,
                }
                results, results_exist = datastore_results("Comment", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
                key = None
                points = 0
                for result in results:
                    key = result.key()
                    points = result.points
                    comment_email = result.email
                
                if key is not None:
                    p = model.Comment.get(key)
                    if points is None:
                        points = 0
                    p.points = points - 1
                    p.put()
                    
                    filters = {
                        "comment_id": comment_id,
                        "email": email,
                    }
                    
                    results, results_exist = datastore_results("CommentPlusMinusConstraints", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
                    points = 0
                    
                    if results_exist:
                        for result in results:
                            points = result.points
                            key = result.key()
                            pm = model.CommentPlusMinusConstraints.get(key)
                            pm.points = points - 1
                            pm.put()

                    
                    else:
                        pm = model.CommentPlusMinusConstraints(comment_id = comment_id, email = email, post_id = post_id, points = points - 1)
                        pm.put()
                            
                        filters = {
                            "email": comment_email,
                        }
                        results, results_exist = datastore_results("Member", filters = filters, inequality_filters = None, order = None, fetch_total = 1, offset = 0, mem_key = None)
                        if results_exist:
                            for result in results:
                                key = result.key()
                                points = result.rep_points
                    
                                member = model.Member.get(key)
                                member.rep_points = points - 2
                                member.put()
                    
            return post_id
    else:
        self.redirect("/")