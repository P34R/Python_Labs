import pickle
import socket

import things

mess = 256


def getManufacturer(id: int):
    s.send(pickle.dumps("getManufacturer"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(mess))
    return obj


def getSoftware(id: int):
    s.send(pickle.dumps("getSoftware"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(mess))
    return obj


def getAllManufSoftware(id: int):
    s.send(pickle.dumps("getAllManufSoftware"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(mess))
    return obj


def getAllManufacturers():
    s.send(pickle.dumps("getAllManufacturers"))
    obj = pickle.loads(s.recv(mess))
    return obj


def addManufacturer(mf: things.Manufacturer):
    s.send(pickle.dumps("addManufacturer"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(mf))
    obj = pickle.loads(s.recv(mess))
    return obj


def addSoftware(sf: things.Software):
    s.send(pickle.dumps("addSoftware"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(sf))
    obj = pickle.loads(s.recv(mess))
    return obj


def delSoftware(id: int):
    s.send(pickle.dumps("delSoftware"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(mess))
    return obj


def delAllManufSoftware(id: int):
    s.send(pickle.dumps("delAllManufSoftware"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(mess))
    return obj


def delManufacturer(id: int):
    s.send(pickle.dumps("delManufacturer"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(mess))
    return obj


def editSoftware(id: int, sf: things.Software):
    s.send(pickle.dumps("editSoftware"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(id))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(sf))
    obj = pickle.loads(s.recv(mess))
    return obj


def findSoftwareByName(name: str):
    s.send(pickle.dumps("findSoftwareByName"))
    print(pickle.loads(s.recv(mess)))
    s.send(pickle.dumps(name))
    obj = pickle.loads(s.recv(mess))
    return obj


def countSoftware(id: int):
    s.send(pickle.dumps("countSoftware"))
    print(pickle.loads(s.recv(1024)))
    s.send(pickle.dumps(id))
    obj = pickle.loads(s.recv(1024))
    return obj


def end():
    s.send(pickle.dumps("end"))
    s.close()



try:
    s = socket.socket()
    host = socket.gethostname()
    port = 8888
    s.connect((host, port))

    manuf = getAllManufacturers()
    soft = None
    for i in manuf:
        print(i)
        soft = getAllManufSoftware(i.id)
        for ss in soft:
            print(ss)
    m = things.Manufacturer(0, "testing")
    m = addManufacturer(m)
    print(m)
    soft_add1 = things.Software(0, "test1", 1.1, m)
    soft_add2 = things.Software(0, "test2", 2.1, m)
    soft_add3 = things.Software(0, "test3", 3.3, m)
    soft_add1 = addSoftware(soft_add1)
    soft_add2 = addSoftware(soft_add2)
    soft_add3 = addSoftware(soft_add3)
    print(getAllManufSoftware(m.id))
    print(countSoftware(m.id))
    delSoftware(soft_add2.id)
    print(getAllManufSoftware(m.id))
    print(countSoftware(m.id))
    print(findSoftwareByName("test1"))
    soft_add1.name = "test1_new"
    editSoftware(soft_add1.id, soft_add1)
    print(getSoftware(soft_add1.id))
    print(findSoftwareByName("test1"))
    print(findSoftwareByName("test1_new"))
    print(delManufacturer(m.id))
    manuf = getAllManufacturers()
    soft = None
    for i in manuf:
        print(i)
        soft = getAllManufSoftware(i.id)
        for ss in soft:
            print(ss)
    end()
except Exception as e:
    print("client error: ",e)
