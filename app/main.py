from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from app.connection_manager import ConnectionManager

manager = ConnectionManager()
app =FastAPI()
templates = Jinja2Templates(directory="./templates")


@app.post("/exec")
async def exec(name:str = Form(...),command:str = Form(...),connection_type:str = Form(...)):
    result =manager.paramiko_connect(name,command,connection_type)
    #result = paramiko_connect(name,command)
    return {"server":name,"result":result}

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    #servers =read_struct_yaml("servers")
    servers =manager.read_struct_yaml("servers")
    commands = manager.read_struct_yaml("commands") 
    #commands = read_struct_yaml("commands") 
    return templates.TemplateResponse("index.html",{"request":request,"servers":servers,"commands":commands}) 

@app.post("/new_server")
async def new_server(request:Request):
    data = await request.form()
    manager.register_server(data)
    return RedirectResponse(url="/", status_code=303)

@app.post("/new_command")
async def new_command(name:str = Form(...),description:str = Form(...),command:str = Form(...)):
    manager.register_command(name,description,command) 
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete_command")
async def delete_command(command:str = Form(...)):
    manager.delete_command(command) 
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete_server")
async def delete_server(name:str = Form(...)):
    manager.exlude_server(name)
    return RedirectResponse(url="/", status_code=303)




