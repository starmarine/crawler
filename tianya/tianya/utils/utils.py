# -*- coding: utf-8 -*-

import pymongo
from pymongo import MongoClient
import md5

class MongoUtils():
    client = None
    db = None
    postCol = None
    
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['tianya']
        self.postCol = self.db.post
        
    def insert(self,post):
        url = post['url']
        entry = self.postCol.find_one({'url':url})
        if(entry == None):
            digest = self.computeDigest(post)
            post['md5'] = digest
            self.postCol.insert_one(post)
        else:
            digest = self.computeDigest(post)
            if(digest != entry['md5']):
                self.postCol.remove(entry)
                self.postCol.insert_one(post)
            else:
                print "no need to update"
           
    def computeDigest(self,post):
        md5
        md5Digestor = md5.new()
        md5Digestor.update(post['content'].encode('utf-8'))
        digest = md5Digestor.hexdigest()
        return digest
