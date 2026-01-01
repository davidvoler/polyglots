
from models.user_vocab import UserVocab
from models.auth import User, UserAuth0Request
from models.user_pref import UserPref
from models.user_vocab import UserVocab
from utils.db import get_current_customer, get_query_results, run_query

def get_current_customer():
    return 'polyglots'

async def get_current_user(user_id):
    pass

async def get_user_by_id(user_id:str, customer_id:str='polyglots')-> User:
    sql = f"""
    SELECT * FROM {customer_id}_users.users WHERE user_id = %s 
    """
    res = await get_query_results(sql, (user_id,))
    if not res:
        return None
    return User(**res[0])


async def get_or_create_user_vocab( lang:str,user_id:str, customer='polyglots')->UserVocab:
    sql = f"""
    SELECT * FROM {customer}_users.user_vocab 
    WHERE user_id = %s
    AND lang = %s
    """
    
    res = await get_query_results(sql, (user_id, lang ))
    # print("--------------------")
    # print(res)
    # print("--------------------")
    if res:
        # user vocab exists
        uv = UserVocab(**res[0])
        return uv
    else:
        # create user vocab - with all the default fields
        uv = UserVocab(user_id=user_id, lang=lang)
        u_dict = uv.to_dict()
        
        keys =[]
        values = []
        for k , v in u_dict.items():
            keys.append(k)
            values.append(v)
        fields = ', '.join(keys)
        placeholders = ', '.join(['%s'] * len(keys))
        sql = f"""
        INSERT INTO {customer}_users.user_vocab ({fields}) 
        VALUES ({placeholders})
        """
        await run_query(sql, tuple(values))

        return uv

async def update_or_create_user_vocab(uv:UserVocab)->UserVocab:
    u_dict = uv.to_dict()
    keys =[]
    values = []
    for k , v in u_dict.items():
        keys.append(k)
        values.append(v)
    fields = ', '.join(keys)
    placeholders = ', '.join(['%s'] * len(keys))
    # print(f"update_or_create_user_vocab: {uv.customer_id} ")
    sql = f"""
    INSERT INTO {uv.customer_id}_users.user_vocab ({fields}) 
    VALUES ({placeholders})
    ON CONFLICT (lang, user_id ) DO UPDATE
    SET 
    last_step = %s,
    last_mode = %s,
    mark = %s,
    current_practice_type = %s,
    current_practice_id = %s
    """
    values = values + [
        uv.last_step,
        uv.last_mode,
        uv.mark,
        uv.current_practice_type.value,
        uv.current_practice_id
    ]
    # print(f"update_or_create_user_vocab: {sql} {values}")
    await run_query(sql, tuple(values))
    return uv

async def _create_user(UserAuth0Request):
    user = User(
        email=UserAuth0Request.email,
        full_name=UserAuth0Request.full_name,
        customer_id=get_current_customer(),
    )
    user.generate_user_id()
    sql = f"""
    INSERT INTO {get_current_customer()}_users.users 
    (user_id, email, customer_id, lang, to_lang) 
    VALUES (%s, %s, %s, %s, %s)
    """
    print("======================")
    print(user.to_lang)
    await run_query(sql, (user.user_id, user.email,
                                        user.customer_id, 
                                        user.lang,
                                        user.to_lang,))
    print("======================")
    return user

async def get_or_create_user_by_auth_req(UserAuth0Request)-> User:
    user = await get_user_by_email_from_db(UserAuth0Request.email)
    if not user:
        user = await _create_user(UserAuth0Request)
    return user


async def change_languages(user_id:str, lang:str, to_lang, customer_id:str)->UserPref:
    sql = f"""
    UPDATE {customer_id}_users.users 
    SET lang = %s, to_lang = %s
    WHERE user_id = %s
    """
    await run_query(sql, (lang,  to_lang, user_id, ))
    return await user_pref_from_db(user_id)


async def get_user_by_email_from_db(email:str)-> User:
    sql = f"""
    SELECT * FROM {get_current_customer()}_users.users 
    WHERE email = %s
    """
    res = await get_query_results(sql, (email,))
    if not res:
        return None
    return User(**res[0])

async def get_user_pref(user:User)-> UserPref:
    user_vocab = None
    if user.lang:
        user_vocab = await get_or_create_user_vocab(user.lang, user.user_id, user.customer_id)

    return UserPref(
        user=user,
        user_vocab=user_vocab 
    )
    

async def user_pref_from_db(user_id:str)-> UserPref:
    user = await get_user_by_id(user_id)
    if not user:
        return None
    user_vocab = None
    if user.lang:
        user_vocab = await get_or_create_user_vocab(user.lang, user_id, user.customer_id)
    return UserPref(
        user=user,
        user_vocab=user_vocab 
    )

async def _save_user_vocab(user_vocab:UserVocab):
    pass 

async def save_preferences(up:UserPref):
    user = up.user
    if user:
        if user.lang and user.to_lang:
           await change_languages(user.user_id, user.lang, user.to_lang)
    uv = up.user_vocab
    if uv:
        await _save_user_vocab(uv)
    return await user_pref_from_db(user.user_id)