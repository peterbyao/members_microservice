from fastapi import FastAPI, Response
import uvicorn

# Tutorials used
# https://fastapi.tiangolo.com/tutorial/first-steps/
# https://realpython.com/fastapi-python-web-apis/
# https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# https://fastapi.tiangolo.com/tutorial/body-updates/
# https://fastapi.tiangolo.com/tutorial/body/

app = FastAPI()


# Index page
@app.get('/')
async def root():
    return {"message": "Hello World"}


# GET members
@app.get("/members")
async def get_all_members():
    return {"message": "Hello members list"}


# GET member_id
@app.get("/members/{member_id}")
async def get_members(member_id: str):
    return {"member_id": member_id}


# GET member_id member_portfolio
@app.get("/members/{member_id}/{portfolio_id}")
async def get_member_portolio(member_id: str, portfolio_id: str):
    return {"member_id": member_id, "portfolio_id": portfolio_id}


# POST add member_id
@app.post("/add_member/{member_id}")
async def add_member(member_id: str):
    return {"member_id": member_id}


# PUT update member_id
@app.put("/update_member/{member_id}")
async def update_member(member_id: str):
    return {"member_id": member_id}


# PUT remove member_id
@app.put("/remove_member/{member_id}")
async def remove_member(member_id: str):
    return {"member_id": member_id}


if __name__ == "__main__":
    uvicorn.run(app)
