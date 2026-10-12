from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.get_db import get_db
from app.models import Memo
from app.pydantic_model import MemoCreate,MemoRead,MemoUpdate
from app.pagination import pagination


router=APIRouter()


# 渲染
@router.get("/list")
def getlist(
    keyword:Optional[str]=None,
    pages=Depends(pagination),
    db:Session=Depends(get_db)
):
    res=db.query(Memo)
    if keyword:
        res=res.filter(Memo.title.like(f"%{keyword}%"))
    total=res.count()
    data=res.offset(pages["skip"]).limit(pages["pageSize"]).all()
    return {"total":total,"data":data}

# 新增
@router.post("/add",status_code=status.HTTP_201_CREATED)
def add_memo(form:MemoCreate,db:Session=Depends(get_db)):
    res=Memo(**form.model_dump())
    db.add(res)
    db.commit()
    db.refresh(res)
    return {"msg":"新增成功","data":res}

# 修改
@router.put("/edit/{id}")
def edit_memo(id:int,form:MemoUpdate,db:Session=Depends(get_db)):
    res=db.query(Memo).get(id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="未找到该内容")
    info=form.model_dump(exclude_unset=True)
    for k,v in info.items():
        setattr(res,k,v)
    db.commit()
    db.refresh(res)
    return {"msg":"修改成功","data":res}

# 删除
@router.delete("/delete_memo/{id}")
def delete_memo(id:int,db:Session=Depends(get_db)):
    res=db.query(Memo).get(id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="未找到该内容,无法删除")
    db.delete(res)
    db.commit()
    return {"msg":"删除成功"}
# 根据ID查询单条数据
@router.get("/get_one/{id}",response_model=MemoRead)
def get_one(id:int,db:Session=Depends(get_db)):
    res=db.query(Memo).get(id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="未找到该内容")
    return res