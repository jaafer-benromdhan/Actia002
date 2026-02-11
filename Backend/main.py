from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 
import os
import re

app = FastAPI()
app.add_middleware(  CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_methods=["*"],
    allow_headers=["*"])
  


""" #normalement el end point bech yetbadel esmou 
@app.get("/getFiles_ids")
def getBoardsFromFiles():
 path = "C:\\Users\\jbenromd\\Desktop\\actia001-main\\backend\\cfgFiles"
 if not os.path.exists(path):
        return {"error": "Path not found"}
 pattern = r'^[-_]+|testDescription' 
 files = [  
            f.replace(pattern, "").split(".")[0]
            for f in os.listdir(path) 
            if os.path.isfile(os.path.join(path, f))
        ]
 ids = [f.replace("testDescription", "").replace(".cfg", "") for f in files]
 ids = [i.lstrip('-_') for i in ids]
 print(files)
 print(ids)
 return {"ids": ids}
 """
 
@app.get("/getFiles_tests")
def getBoardsTestsFromFiles():
    folder_path = r"C:\Users\jbenromd\Desktop\actia001-main\backend\cfgFiles"
    results = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".cfg"):
           
            clean_id = re.sub(r'^[-_]+|testDescription', '', filename).split('.')[0]
            clean_id = clean_id.lstrip('-_')

            full_path = os.path.join(folder_path, filename)
            try:
                with open(full_path, "r") as f:
                    lines = [line.strip() for line in f.readlines()]
                    
                results[clean_id] = lines
            except Exception as e:
                print(f"Could not read {filename}: {e}")
    print(results)
    return {"tests": results}

#getBoardsFromFiles()
getBoardsTestsFromFiles()
if __name__=="__main__":
       uvicorn.run(app,host="0.0.0.0",port=8000)