from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import Dict, List, Any

# ---------------------------
# Config FastAPI + CORS
# ---------------------------
app = FastAPI(title="Test Suites API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ton front
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Modèles (pour /run_test)
# ---------------------------
class TestItem(BaseModel):
    name: str
    file: str
    address: str
    mcu: str
    interface: str
    reset: bool

# ---------------------------
# Parsing des .cfg
# ---------------------------
CFG_DIR = r"C:\Users\jbenromd\Desktop\actia001-main\backend\cfgFiles"

def parse_cfg_files() -> Dict[str, List[dict]]:
    """
    Lit tous les .cfg du dossier et renvoie:
    {
      "BoardName1": [ {test_object}, ... ],
      "BoardName2": [ ... ]
    }
    """
    if not os.path.isdir(CFG_DIR):
        raise FileNotFoundError(f"Dossier introuvable: {CFG_DIR}")

    cfg_files = [f for f in os.listdir(CFG_DIR) if f.lower().endswith(".cfg")]
    boards: Dict[str, List[dict]] = {}

    for cfg_file in cfg_files:
        board_name = cfg_file.replace(".cfg", "").replace("testDescription", "")
        boards[board_name] = []

        full_path = os.path.join(CFG_DIR, cfg_file)

        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            for raw_line in f:
                line = raw_line.strip()

                # Ignore commentaires et lignes vides
                if not line or line.startswith("#"):
                    continue

                # Découpe sur espaces/tabs
                parts = line.split()

                # Remplace '---'/'-----' par string vide pour stabiliser les index
                parts = [p if p.strip("-") else "" for p in parts]

                # Sécurité: s'assurer qu'on a assez de colonnes
                # Indices utilisés plus bas: 1,2,3,4,6,10
                if len(parts) < 11:
                    # Si une ligne est incomplète, on la saute proprement
                    # (tu peux aussi la logger)
                    continue

         

                name = parts[1]
                file_path = parts[3]
                address = parts[4]
                mcu = parts[2]
                interface = parts[10] if len(parts) > 10 else ""
                reset = (parts[6].upper() == "TRUE") if len(parts) > 6 else False

                test_object = {
                    "name": name,
                    "file": file_path,
                    "address": address,
                    "mcu": mcu,
                    "interface": interface,
                    "reset": reset,
                }

                boards[board_name].append(test_object)

    return boards

# ---------------------------
# Endpoints
# ---------------------------

@app.get("/testsuites")
def get_testsuites_grouped() -> Dict[str, List[dict]]:
   
    try:
        return parse_cfg_files()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/testsuites_flat")
def get_testsuites_flat() -> Dict[str, List[dict]]:

    try:
        boards = parse_cfg_files()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    flat: List[dict] = []
    for board, tests in boards.items():
        # Si tu veux inclure le nom du board dans chaque test:
        for t in tests:
            flat.append({**t, "board": board})

    return {"tests": flat}



if __name__ == "__main__":
    # Démarrage: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
