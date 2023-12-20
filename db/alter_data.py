from bson.objectid import ObjectId

def insert_task(db, task):
    task = dict(task)
    res = db.todos.insert_one(task)
    print(res)
    return res

def update_task(db, id, task):
    id = ObjectId(id)
    task = dict(task)
    res = db.todos.update_one({'_id': id}, {'$set': task})
    return res

def update_status(db, id):
    id = ObjectId(id)
    task = db.todos.find_one({'_id': id})
    if task is not None:
        is_active = task['is_active']
    res = db.todos.update_one({'_id': id}, {'$set': {'is_active': not is_active}})
    return res

def delete_task(db, id):
    id = ObjectId(id)
    res = db.todos.delete_one({'_id': id})
    return res

def insert_user(db, user):
    user = dict(user)
    res = db.user.insert_one(user)
    return res

def insert_category(db, category):
    category = dict(category)
    res = db.category.insert_one(category)
    return res