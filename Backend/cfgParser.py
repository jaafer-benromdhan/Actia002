import os
import re
import time
import subprocess
VERSION = "21"
def getTestParam(line):
        lineSplit = re.split(r'\s+', line.strip())
        print (line)
        CATEGORY = lineSplit[0]
        TEST_TYPE = lineSplit[1]
        FAMILY = lineSplit[2]
        FILE = lineSplit[3]
        ADDRESS = lineSplit[4]
        BIN_DIR = lineSplit[5]
        RESET = lineSplit[6]
        PORT_NAME = lineSplit[7]
        SN = lineSplit[8]
        SECTORS = lineSplit[9]
        INTERFACE = lineSplit[10]
        HSMLICENSE = lineSplit[11]
        RSSEPATH = lineSplit[12]
        INPUT = lineSplit[13]
        OUTPUT = lineSplit[14]
        ELPATH = lineSplit[15]
        SNV3 = lineSplit[16]
        SLAVEADDRESS = lineSplit[17]
        OBK_Cert_file = lineSplit[18]
        OBK_PWD_file = lineSplit[19]
        keyPATH = lineSplit[20]
        PATH_CERT  = lineSplit[21]
        PATH_PWD  = lineSplit[22]
        CONSECUTIVE  = lineSplit[23]
        OB  = lineSplit[24]
        OB_VALUE  = lineSplit[25]
        paramTestList = [str(CATEGORY),str(TEST_TYPE), str(FAMILY), str(FILE), str(ADDRESS), str(BIN_DIR), str(RESET), str(PORT_NAME), str(SN), str(SECTORS), str(INTERFACE), str(HSMLICENSE), str(RSSEPATH), str(INPUT), str(OUTPUT), str(ELPATH), str(SNV3), str(SLAVEADDRESS), str(OBK_Cert_file), str(OBK_PWD_file), str(keyPATH), str(PATH_CERT), str(PATH_PWD), str(CONSECUTIVE), str(OB), str(OB_VALUE)]
        return paramTestList


def getCfgFiles():
    filesList = [x for x in os.listdir("./cfgFiles") if x.endswith(".cfg") and x.startswith("testDescription")]
    return  filesList


def getCsvName (cfgFile):
    if cfgFile.startswith("testDescription"):
        csvName = cfgFile.replace("testDescription", '')
        csvName = csvName.replace(".cfg" , ".csv")
        return csvName

def isWL(SN, PORTNAME,stlinkList,nbrOfStlink,USBList,nbrOfUSB):
    SNDeviceIDList = []
    if PORTNAME == "SWD":
        for i in range (0, nbrOfStlink):
            SNDeviceIDList.append((stlinkList[i].serialNumber,stlinkList[i].deviceId))
        for sn, deviceId in SNDeviceIDList:
            if SN == sn:
                deviceId = deviceId
                return deviceId
            else:
                deviceId = '0x000'
                return deviceId
    if PORTNAME == "USB1":
        for i in range (0, nbrOfUSB):
            SNDeviceIDList.append(USBList[i].serialNumber)
        for sn, deviceId in SNDeviceIDList:
            if SN == sn:
                deviceId = deviceId
                return deviceId
            else:
                deviceId = '0x000'
                return deviceId

def isRsseNeeded(SN, PORTNAME,stlinkList,nbrOfStlink,USBList,nbrOfUSB):
    SNDeviceIDList = []
    if PORTNAME == "SWD":
        for i in range (0, nbrOfStlink):
            SNDeviceIDList.append((stlinkList[i].serialNumber,stlinkList[i].deviceId))
        for sn, deviceId in SNDeviceIDList:
            if SN == sn:
                devId = deviceId
                if devId == '0x497' or devId == '0x472' :
                    return 1
                else:
                    return 0
    if PORTNAME == "USB1":
        for i in range (0, nbrOfUSB):
            SNDeviceIDList.append(USBList[i].serialNumber)
        for sn, deviceId in SNDeviceIDList:
            if SN == sn:
                devId = deviceId
                if devId == '0x497' or devId == '0x472':
                    return 1
                else:
                    return 0

def checkDeviceConnexion(SN,INTERFACE ,stlinkList, nbrOfStlink, USBList, nbrOfUSB, JLinkList, nbrOfJLINK):
    serialNumberList = []
    if INTERFACE == "STLINK":
        for i in range(0, nbrOfStlink):
            serialNumberList.append(stlinkList[i].serialNumber)
        if SN in serialNumberList:
            connected = 1
            return connected
        else:
            connected = 0
            return connected
    if INTERFACE == "USB":
        for i in range(0, nbrOfUSB):
            serialNumberList.append(USBList[i].serialNumber)
        if SN in serialNumberList:
            connected = 1
            return connected
        else:
            connected = 0
            return connected
    if INTERFACE == "JLINK":
        for i in range(0,nbrOfJLINK ):
            serialNumberList.append(JLinkList[i].serialNumber)
        if SN in serialNumberList:
            connected = 1
            return connected
        else:
            connected = 0
            return connected

def getCsvFiles():
    filesList = [x for x in os.listdir("./csvFiles") if x.endswith(".csv")]
    return  filesList
def IsEmpty(line):
    testvide=1
    if len(line)==0 :
            testvide=0
    return testvide
def getObFiles(FILE):
    fileslist = [x for x in os.listdir("./ObtestFiles") if x==FILE]
    return fileslist

def getparam(line):
    Param = line.split(",")
    dic={}
    while(len(Param)!=0):
        dic[str(Param[0])]=str(Param[1])
        del Param[0:2]
    return dic
def getadressFile(csvName):
    for x in os.listdir("./AdresseFiles"):
        if x == csvName:
            return x
def getAdrdese (x,csvName):
    file=getadressFile(csvName)
    #print("Reading Adresse FILE \n", file)
    ADRESSE_file_object = open("./AdresseFiles/" + str(csvName), "r")
    ADRESSE_lines = ADRESSE_file_object.read().split('\n')
    for line in ADRESSE_lines:
        if line.startswith('#'):
            continue
        if x[0] in line :
            Param=line.split('   ')
            Adresse= str(Param[-2])
            break
    return Adresse
def getPosition(x,csvName):
    file = getadressFile(csvName)
    # print("Reading Adresse FILE \n", file)
    ADRESSE_file_object = open("./AdresseFiles/" + str(csvName), "r")
    ADRESSE_lines = ADRESSE_file_object.read().split('\n')
    for line in ADRESSE_lines:
        if line.startswith('#'):
            continue
        if x[0] in line:
            Param = line.split('   ')
            Position = Param[-1]
            break
    if 'to' in Position:
        p=str(Position).split("to")
        return list(p)
    else:
        return int(Position)
def get_success_condition(FILE):
        OB_file_object = open("./ObtestFiles/" + str(FILE), "r")
        OB_lines = OB_file_object.read().split('\n')
        for line in OB_lines:
            if IsEmpty(line) == 0:
                continue
            else:
                if line.startswith('#') and 'OK_PATTERN' in line:
                    condition=line.split('=')
                    break
        return condition[1].split('_')
def get_failure_condition(FILE):
    OB_file_object = open("./ObtestFiles/" + str(FILE), "r")
    OB_lines = OB_file_object.read().split('\n')
    for line in OB_lines:
        if IsEmpty(line) == 0:
            continue
        else:
            if line.startswith('#') and 'FAIL_PATTERN' in line:
                condition = line.split('=')
                break
    return condition[1]

def run_command_and_measure(command):
    start_time = time.perf_counter()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    if result.returncode != 0:
        print(f"Erreur lors de l'exécution de la commande : {result.stderr}")
    
    return execution_time
def extract_TEXEC (testResult) :
    map_Result = testResult.split(',')
       # Parcourir chaque paire
    for item in map_Result:
        # Diviser la paire en clé et valeur
        if 'TEXEC' in item:
            cle, valeur = item.split(':')
            if cle.strip() == 'TEXEC':
                return float(valeur.strip())
    
    # Si TEXEC n'est pas trouvé, retourner None ou un message d'erreur
    return 0