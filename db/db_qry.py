from bson.objectid import ObjectId


def todos(db, name=None, id=None):
    query = dict()
    if name is not None:
        query['name'] = name
    if id is not None:
        query['_id'] = ObjectId(id)
    if len(query) > 0:
        res = db.todos.find_one(query)
    else:
        cursor = db.todos.find()
        res = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            res.append(doc)
    return res

def users(db, id=None, name=None):
    query = dict()
    if id is not None:
        query['_id'] = ObjectId(id)
    if name is not None:
        query['name'] = name
    if len(query) > 0:
        res = db.user.find_one(query)
    else:
        cursor = db.user.find()
        res = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            res.append(doc)
    return res

def categories(db, id=None, name=None):
    query = dict()
    if id is not None:
        query['_id'] = ObjectId(id)
    if name is not None:
        query['name'] = name
    if len(query) > 0:
        res = db.category.find_one(query)
    else:
        cursor = db.category.find()
        res = []
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            res.append(doc)
    return res