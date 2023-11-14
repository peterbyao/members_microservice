from fastapi import FastAPI, Depends, Query
from typing import Annotated, List
import Resources.models as models
from Resources.database import engine, SessionLocal
from sqlalchemy.orm import Session
from Resources.schemas import MemberSchema, Member
from Resources.exceptions import MemberNotFoundError, MemberAlreadyExistError
import uvicorn

# Tutorials used
# https://fastapi.tiangolo.com/tutorial/first-steps/
# https://realpython.com/fastapi-python-web-apis/
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# https://fastapi.tiangolo.com/tutorial/body-updates/
# https://fastapi.tiangolo.com/tutorial/body/
# https://www.youtube.com/watch?v=zzOwU41UjTM&t=7s

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


##################################################################################

# Index page
@app.get('/')
async def root():
    return {"message": "Hello World"}


# GET members
@app.get("/members/")
async def get_all_members(offset: int = 0,
                          limit: int = Query(default=10, le=100),
                          session: Session = Depends(get_db)):
    members = session.query(models.Member).offset(offset).limit(limit).all()
    return members

@app.get("/members/search/", response_model=List[MemberSchema])
async def get_members(offset: int = 0,
                      limit: int = Query(default=10, le=100),
                      member_name: str = None,
                      age_gte: float = None,
                      age_lt: float = None,
                      portfolio_value_gte: float = None,
                      portfolio_value_lt: float = None,
                      sort_by: str = None,
                      session: Session = Depends(get_db)):
    query = session.query(models.Member)
    if member_name is not None:
        query = query.filter(models.Member.member_name == member_name)
    if age_gte is not None:
        query = query.filter(models.Member.age >= age_gte)
    if age_lt is not None:
        query = query.filter(models.Member.age < age_lt)
    if portfolio_value_gte is not None:
        query = query.filter(models.Member.portfolio_value >= portfolio_value_gte)
    if portfolio_value_lt is not None:
        query = query.filter(models.Member.portfolio_value < portfolio_value_lt)
    if sort_by in ["name+", "name-", "age+", "age-", "portfolio_value+", "portfolio_value-"]:
        if sort_by == "name+":
            query = query.order_by(models.Member.member_name.asc())
        if sort_by == "name-":
            query = query.order_by(models.Member.member_name.desc())
        if sort_by == "age+":
            query = query.order_by(models.Member.age.asc())
        if sort_by == "age-":
            query = query.order_by(models.Member.age.desc())
        if sort_by == "portfolio_value+":
            query = query.order_by(models.Member.portfolio_value.asc())
        if sort_by == "portfolio_value-":
            query = query.order_by(models.Member.portfolio_value.desc())

    return query.offset(offset).limit(limit).all()
    #result = await session.execute(query).offset(offset).limit(limit).all()
    #return result



# GET member_id
@app.get("/members/id/{member_id}/")
async def get_member(member_id: int, session: Session = Depends(get_db)):
    member = session.query(models.Member).get(member_id)

    if member is None:
        raise MemberNotFoundError

    return member

# GET member_name
@app.get("/members/member_name/{member_name}/")
async def get_member(member_name: str, session: Session = Depends(get_db)):
    member = session.query(models.Member).filter(models.Member.member_name == member_name).first()

    if member is None:
        raise MemberNotFoundError

    return member


# # GET member_id member_portfolio
# @app.get("/members/{member_id}/{portfolio_id}/")
# async def get_member_portfolio(member_id: str, portfolio_id: str):
#     return {"member_id": member_id, "portfolio_id": portfolio_id}


# POST add member_id
@app.post("/add_member/{member_name}/")
async def add_member(member_name: str, session: Session = Depends(get_db)):
    member = session.query(models.Member).filter(models.Member.member_name == member_name).first()
    if member:
        raise MemberAlreadyExistError

    new_member = models.Member(member_name=member_name, portfolio_value=1000000, age=23)
    session.add(new_member)
    session.commit()
    session.refresh(new_member)
    return new_member


# PUT update member_id
@app.put("/update_member/")
async def update_member(member_update: Member, session: Session = Depends(get_db)):
    member_id = member_update.id
    member = session.query(models.Member).get(member_id)

    if member is None:
        raise MemberNotFoundError

    member.member_name = member_update.member_name
    member.portfolio_value = member_update.portfolio_value
    member.age = member_update.age

    session.commit()
    session.refresh(member)

    return member


# PUT remove member_id
@app.delete("/remove_member/{member_name}/")
async def remove_member(member_name: str, session: Session = Depends(get_db)):
    member = session.query(models.Member).filter(models.Member.member_name == member_name).first()
    if member is None:
        raise MemberNotFoundError

    session.delete(member)
    session.commit()


if __name__ == "__main__":
    uvicorn.run(app, timeout_keep_alive=65, host="0.0.0.0", port=5000)
