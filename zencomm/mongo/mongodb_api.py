import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

client = None

def _get_mongodb_uri():
    uri = 'mongodb://localhost:27017/?maxPoolSize=200&connectTimeoutMS=1000'
    return uri

def _get_mongodb_client():
    global client
    if client is None:
        client = MongoClient(_get_mongodb_uri())
    return client

def _get_mongodb_db():
    client = _get_mongodb_client()
    return client.esse

def close_mongodb_connection():
    global client
    if client is not None:
        client.close()

def get_activity_adverts_collection():
    return _get_collection('act_adverts')

def get_activity_comments_collection():
    return _get_collection('act_comments')

def get_aimi_collection():
    return _get_collection('aimi')

def _get_collection(collection):
    db = _get_mongodb_db()
    return db[collection]

 
def insert_one_activity_adverts(doc_adverts):
    #insert one activity adverts
    #dict_adverts format:
    #{"activity_id": "activity_id", "data": data}
    collection = get_activity_adverts_collection()
    return _insert_one_document(doc_adverts, collection)

def insert_many_activity_adverts(doc_adverts):
    collection = get_activity_adverts_collection()
    return _insert_many_documents(doc_adverts, collection)

def insert_one_activity_comments(doc_comments):
    #insert one activity adverts
    #dict_adverts format:
    #{"activity_id": "activity_id", "data": data}
    collection = get_activity_comments_collection()
    return _insert_one_document(doc_comments, collection)

def insert_many_activity_comments(doc_comments):
    collection = get_activity_comments_collection()
    return _insert_many_documents(doc_comments, collection)

def get_act_adverts_by_activity_id(act_id):
    collection = get_activity_adverts_collection()
    try:
        result = collection.find_one({"activity_id": act_id})
        return result
    except pymongo.errors.PyMongoError as e:
        print "find_one error occurred: %" %e
        return {}

def get_act_adverts_by_object_id(obj_id):
    collection = get_activity_adverts_collection()
    return _get_document_by_object_id(obj_id, collection)

def get_act_comments_by_activity_id(act_id):
    collection = get_activity_comments_collection()
    try:
        result = collection.find_one({"activity_id": act_id})
        return result
    except pymongo.errors.PyMongoError as e:
        print "find_one error occurred: %" %e
        return {}

def get_act_comments_by_object_id(obj_id):
    collection = get_activity_comments_collection()
    return _get_document_by_object_id(obj_id, collection)

def _get_document_by_object_id(obj_id, collection):
    try:
        result = collection.find_one({"_id": ObjectId(obj_id)})
        return result
    except pymongo.errors.PyMongoError as e:
        print "find_one error occurred: %" %e
        return {}



def _insert_one_document(document, collection):
    #insert one document
    try:
        print "_insert_one_document"
        advert_id = collection.insert_one(document).inserted_id
        return str(advert_id)
    except pymongo.errors.PyMongoError as e:
        print "insert_one error occurred: %s" %e
        #TODO: raise exception
     

def _insert_many_documents(documents, collection):
    #insert many documents
    #documents format is like:
    #[{"activity_id": "activity_id", "data": data}, {"activity_id": "activity_id", "data": data}]
    try:
        advert_ids = collection.insert_many(documents).inserted_ids
        ids = []
        for advert_id in advert_ids:
            ids.append(str(advert_id))
            return ids
    except pymongo.errors.PyMongoError as e:
        print "insert_many error occurred: %s" %e
        #TODO: raise exception

