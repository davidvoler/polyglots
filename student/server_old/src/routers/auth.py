from fastapi import APIRouter, Response, Request, status, HTTPException
from models.auth import UserAuth0Request, User, UserStatusRequest
from models.user_pref import UserPref, UpdatePreferences
from utils.users import (get_or_create_user_by_auth_req, 
                         get_user_pref, 
                         get_user_by_email_from_db, 
                         save_preferences,
                         change_languages,
                         user_pref_from_db,
                         update_or_create_user_vocab,
                         )

from utils.users import *

router = APIRouter()



@router.post("/get_or_create_user")
async def get_user_by_email(user_request:UserAuth0Request, response:Response) -> UserPref:
    user = await get_or_create_user_by_auth_req(user_request)
    res = None
    if user:
        res = await get_user_pref(user)
    else:
        raise HTTPException(status_code=404, detail="user not found")
    response.set_cookie(key="user_id", value=user.user_id, max_age=31536000)
    if user.lang:
        response.set_cookie(key="lang", value=user.lang, max_age=31536000)
    if user.to_lang:
        response.set_cookie(key="to_lang", value=user.to_lang, max_age=31536000)
    return res


@router.post("/login_with_user_cookie")
async def login_with_user_id(request: Request, response: Response) -> UserPref:
    try:
        user_id = request.cookies.get("user_id")
        return await user_pref_from_db(user_id)
    except Exception as e:
        print("Error getting user_id from cookies: ", e)
        return HTTPException(status_code=401, detail="user not found")
  


@router.post("/update_user")
async def get_user_by_email(email:str) -> UserPref:
    user = await get_user_by_email_from_db(email)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return await get_user_pref(user)
   


@router.post("/get_user_pref")
async def get_user_preferences(req: dict) -> UserPref:
    try:
        user_id = req.get("user_id")
        print("user_id: ", user_id)
        if not user_id:
            raise HTTPException(status_code=401, detail="user_id not provided")
        
        user_pref = await user_pref_from_db(user_id)
        if not user_pref:
            raise HTTPException(status_code=404, detail="user not found")
            
        print("user_pref: ", user_pref)
        return user_pref
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        print("Error getting user preferences: ", e)
        # Return a proper error response instead of None
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/update_user_pref")
async def update_user_pref(uv:UserVocab):
    print("update_user_pref: ", uv)
    return await update_or_create_user_vocab(uv)



@router.post("/update_langs")
async def update_langs(pref:UpdatePreferences):
    print("update_langs: ", pref)
    return await change_languages(pref.user_id, pref.lang, pref.to_lang, pref.customer_id)
    



@router.post("/user_status")
async def get_user_status(req:UserStatusRequest) -> UserPref:
    return await get_or_create_user_vocab(req.lang, req.user_id)