from math import ceil
from app import db

class Pagination(object):
    def __init__(self, page, per_page, total_count, collection):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.collection = collection

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_page(self):
        return self.page + 1

    @property 
    def prev_page(self):
        return self.page - 1


    def getPage(self):
        # return a iterable self.page which have self.per_page documents
        # self.page is the page count you want
        cursor = db[self.collection].find().sort('_id', -1).limit(self.per_page)

        if self.page == 1:
            return cursor;

        last_id = None
        for each in cursor:
            last_id = each['_id'] # get the _id of the last document in the first page

        cursor = None
        for i in range(self.page -1): # the first page no count
            cursor = db[self.collection].find({'_id': {'$lt': last_id}}).sort('_id', -1).limit(self.per_page)

            if i == self.page-1 - 1: # the last page we want
                return cursor

            for each in cursor:
                last_id = each['_id'] # get the _id of this self.page, to find the next page
