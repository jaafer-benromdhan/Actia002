import os

directory = r"C:\Users\jbenromd\Desktop\actia001-main\backend\cfgFiles"
cfgFiles = os.listdir(directory)

all_boards_tests = {}

for cfgFile in cfgFiles:
    boardName = cfgFile.replace(".cfg", "").replace("testDescription", "")
    all_boards_tests[boardName] = []

    full_path = os.path.join(directory, cfgFile)

    with open(full_path, "r") as file:
        for line  in file:
            
            line = line.strip()
            parts = [p if p.strip("-") else "" for p in parts]
           
            test_object = {
                    "name": parts[1],          
                    "file": parts[3],          
                    "address": parts[4],       
                    "mcu": parts[2],           
                    "interface": parts[9],    
                    "reset": parts[5] == "TRUE"
                }

            all_boards_tests[boardName].append(test_object)

        
        print(all_boards_tests) 

# Debug print
for b, tests in all_boards_tests.items():
    print(f"\nBoard: {b}")
    for t in tests:
        print(t)