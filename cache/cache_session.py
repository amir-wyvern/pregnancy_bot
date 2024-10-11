import redis
import json

DATA = {}

def get_user(chat_id, item, db: redis.Redis):

    if item == 'all':
        # resp = db.hgetall(f'tel:agent:{chat_id}')
        resp = DATA[f'tel:agent:{chat_id}']
        if resp == {}:
            resp = None
        
        # if resp['cache'] != {}
        return resp
    
    else:
        return DATA[f'tel:agent:{chat_id}'][item]
        # return db.hget(f'tel:agent:{chat_id}', item)
    

def set_new_user(chat_id, db: redis.Redis, **kwargs)-> dict:

    data = {
        'pos':'menu',
        'cache': {},
        # 'cache': json.dumps({}),
        'session': ''
    }
    data.update(kwargs)

    DATA[f'tel:agent:{chat_id}'] = data
    return True

    # resp = db.hset(f'tel:agent:{chat_id}', mapping= data)
    # return resp


def set_session(chat_id, session, db: redis.Redis):

    DATA[f'tel:agent:{chat_id}']['session'] = session
    return True

    # resp = db.hset(f'tel:agent:{chat_id}', 'session', session)
    # return resp


def del_session(chat_id, db: redis.Redis):

    DATA[f'tel:agent:{chat_id}']['session'] = ''
    return True

    # resp = db.hdel(f'tel:agent:{chat_id}', 'session')
    # return resp


def get_session(chat_id, db: redis.Redis):

    # session = db.hget(f'tel:agent:{chat_id}', 'session') 
    try:
        session = DATA[f'tel:agent:{chat_id}']['session']
    except:
       session = None

    if session :

        return session

    return None


def set_position(chat_id, pos, db:redis.Redis):

    if DATA.get(f'tel:agent:{chat_id}', None):
        DATA[f'tel:agent:{chat_id}']['pos'] = pos
    
    else:
        DATA[f'tel:agent:{chat_id}'] = {
            'pos': pos,
            'cache': {},
            'session': ''
        }
    return True

    # resp = db.hset(f'tel:agent:{chat_id}', 'pos', pos)
    # return resp


def get_position(chat_id, db:redis.Redis):

    return DATA[f'tel:agent:{chat_id}']['pos']

    # pos =db.hget(f'tel:agent:{chat_id}', 'pos')
    # return pos


def set_cache(chat_id, data, db:redis.Redis):

    DATA[f'tel:agent:{chat_id}']['cache'] = data
    return True

    # resp = db.hset(f'tel:agent:{chat_id}', 'cache', json.dumps(data))
    # return resp


def delete_cache(chat_id, db:redis.Redis):

    DATA[f'tel:agent:{chat_id}']['cache'] = {}
    # db.hset(f'tel:agent:{chat_id}', 'cache', json.dumps({}))
    return True

def get_cache(chat_id, db:redis.Redis):

    data = DATA[f'tel:agent:{chat_id}']['cache']

    return data

    # data = db.hget(f'tel:agent:{chat_id}', 'cache')
    # return json.loads(data)


def set_msg_id(chat_id, msg_id, db: redis.Redis):

    if DATA.get(f'tel:agent:msg_id:{chat_id}', None) == None:
        DATA[f'tel:agent:msg_id:{chat_id}'] = []
    
    DATA[f'tel:agent:msg_id:{chat_id}'].append(msg_id)
    # resp = db.rpush(f'tel:agent:msg_id:{chat_id}', msg_id)
    # return resp

    return True


def get_msg_id(chat_id, db: redis.Redis):

    data = DATA[f'tel:agent:msg_id:{chat_id}']
    # data = db.lrange(f'tel:agent:msg_id:{chat_id}', start=0 ,end=-1)
    return data


def remove_msg_id(chat_id, msg_id, db: redis.Redis):

    DATA[f'tel:agent:msg_id:{chat_id}'].remove(msg_id)
    return True

    # resp = db.lrem(f'tel:agent:msg_id:{chat_id}', count=1, value= msg_id)
    # return resp