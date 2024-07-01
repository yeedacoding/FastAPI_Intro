from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"ping" : "pong"}

todo_data = {
    1 : {
        "id" : 1,
        "contents" : "FastAPI Section 1",
        "is_done" : True,
    },
    2 : {
        "id" : 2,
        "contents" : "FastAPI Section 2",
        "is_done" : False,
    },
    3 : {
        "id" : 3,
        "contents" : "FastAPI Section 3",
        "is_done" : False,
    }
}

# 1-1. get method : todo 데이터 전체 조회
@app.get("/todos", status_code=200) # + http status code 적용
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())
    # DESC 입력 -> 내림차순으로 데이터 보여줌
    if order == "DESC" :
        return ret[::-1]
    return ret

# 1-2. get method : todo 데이터 단일 조회
@app.get("/todos/{todo_id}", status_code=200)
def get_todo_handler(todo_id : int) :
    todo = todo_data.get(todo_id)
    if todo :
        return todo
    # 없는 todo id를 조회할 경우 404 오류처리 수행(detail은 오류 메시지)
    raise HTTPException(status_code=404, detail="ToDo Not Found")



# 2. post method : todo 생성
class CreateToDoRequest(BaseModel) :
    # request body 형태 지정 -> todo_data와 동일한 schema
    id : int
    contents : str
    is_done : bool


@app.post("/todos", status_code=201)
def create_todo_handler(request: CreateToDoRequest):
    # request body(CreateToDoRequest) 형식에 맞게 입력을 받고 해당 내용대로 api 생성
    todo_data[request.id] = request.dict()
    return todo_data[request.id]



# 3. patch method : todo 업데이트
# is_done값을 입력받아 todo 업데이트
@app.patch("/todos/{todo_id}", status_code=200)
def update_todo_handler(
    todo_id : int,
    is_done : bool = Body(..., embed=True),
    ) :
    todo = todo_data.get(todo_id)
    if todo :
        todo["is_done"] = is_done
        return todo
    raise HTTPException(status_code=404, detail="ToDo Not Found")

# 4. delete method : todo 삭제
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo_handler(todo_id : int) :
    todo = todo_data.pop(todo_id, None)
    if todo :
        return
    raise HTTPException(status_code=404, detail="ToDo Not Found")