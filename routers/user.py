from fastapi import APIRouter, HTTPException, Depends
from db import get_conn
from schemas.user import UserCreate



router=APIRouter(
    tags=["Users"],
    prefix="/users"
)
@router.post('/')
def create_user(user:UserCreate, conn= Depends(get_conn)):
    try:
        with conn.cursor() as cur:
            cur.execute(
    'INSERT INTO "user" (name, email) VALUES (%s, %s) RETURNING id;',
    (user.name, user.email)
)
            new_id=cur.fetchone()[0]
            conn.commit()
            return {"id": new_id, "message": "New user created successfully!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))  

@router.get('/')
def get_users(conn=Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute(
            'SELECT * FROM "user";'
        )
        users=cur.fetchall()
        return [
            {"id": row[0], "name": row[1], "email": row[2]}
            for row in users
        ]
    
@router.get('/{user_id}')
def get_user(user_id:int, conn=Depends(get_conn)):
    with conn.cursor() as cur:
        cur.execute(
            'SELECT * FROM "user" WHERE id = %s;',
            (user_id, )
        )  
        user=cur.fetchone()
        if not user: 
            raise HTTPException(status_code=404, detail="User not found with this id")
        return {"id": user[0], "name": user[1], "email": user[2]}

@router.delete('/{user_id}') 
def delete_user(user_id:int, conn=Depends(get_conn)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                'DELETE FROM "user" WHERE id=%s RETURNING id;',
                (user_id, )
            )  
            deleted_user=cur.fetchone()
            if not deleted_user:
                raise HTTPException(status_code=404, detail="user not found with this id")
            deleted_id=deleted_user[0]
            conn.commit() 
            return {"id": deleted_id, "msg": "user was deleted successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/{user_id}')
def update_user(user_id: int, user: UserCreate, conn=Depends(get_conn)):
    try:
        with conn.cursor() as cur:
            cur.execute(
                'UPDATE "user" SET name=%s, email=%s WHERE id=%s RETURNING id;',
                (user.name, user.email, user_id)
            )
            updated_user = cur.fetchone()
            if updated_user is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            updated_id = updated_user[0]
            
            conn.commit()
            return {"id": updated_id, "msg": "user was updated successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
