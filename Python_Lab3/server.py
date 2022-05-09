import pickle
import socket

import db
import things

mess = 256


def start():
    s.listen()
    c, addr = s.accept()
    while True:

        received = ""

        received = pickle.loads(c.recv(mess))
        match received:
            case "getManufacturer":  # getManufacturer
                c.send(pickle.dumps("get manufacturer: waiting for id"))
                id = pickle.loads(c.recv(mess))
                obj = database.getManufacturer(id)
                ser_obj = pickle.dumps(obj)
                c.send(ser_obj)

            case "getSoftware":  # getSoftware
                c.send(pickle.dumps("get software: waiting for id"))
                id = pickle.loads(c.recv(mess))
                obj = database.getSoftware(id)
                ser_obj = pickle.dumps(obj)
                c.send(ser_obj)

            case "getAllManufSoftware":  # getAllManufSoftware
                c.send(pickle.dumps("get all software from manufacturer: waiting for manufacturer id"))
                mid = pickle.loads(c.recv(mess))
                obj = database.getAllManufSoftware(mid)
                ser_obj = pickle.dumps(obj)
                c.send(ser_obj)

            case "getAllManufacturers":  # getAllManufacturers
                objects = database.getAllManufacturers()
                ser_obj = pickle.dumps(objects)
                c.send(ser_obj)

            case "addManufacturer":  # addManufacturer
                c.send(pickle.dumps("add manufacturer: waiting for manufacturer"))
                a = pickle.loads(c.recv(mess))
                manuf = things.Manufacturer(a.id, a.name)
                database.addManufacturer(manuf)
                c.send(pickle.dumps(manuf))

            case "addSoftware":  # addSoftware
                c.send(pickle.dumps("add software: waiting for software"))
                soft = pickle.loads(c.recv(mess))
                database.addSoftware(soft)
                c.send(pickle.dumps(soft))

            case "delSoftware":  # delSoftware
                c.send(pickle.dumps("delete software: waiting for id"))
                id = pickle.loads(c.recv(mess))
                database.delSoftware(id)
                c.send(pickle.dumps("done"))
            case "delAllManufSoftware":  # delAllManufSoftware
                c.send(pickle.dumps("delete all software from manufacturer: waiting for manufacturer id"))
                mid = pickle.loads(c.recv(mess))
                database.delAllManufSoftware(mid)
                c.send(pickle.dumps("done"))
            case "delManufacturer":  # delManufacturer
                c.send(pickle.dumps("delete manufacturer: waiting for id"))
                mid = pickle.loads(c.recv(mess))
                database.delManufacturer(mid)
                c.send(pickle.dumps("done"))
            case "editSoftware":  # editSoftware
                c.send(pickle.dumps("edit software: waiting for id"))
                id = pickle.loads(c.recv(mess))
                c.send(pickle.dumps("edit software: waiting for new software"))
                soft = pickle.loads(c.recv(mess))
                database.editSoftware(id, soft)
                c.send(pickle.dumps("done"))
            case "findSoftwareByName":  # findSoftwareByName
                c.send(pickle.dumps("find software by name, waiting for software name"))
                name = pickle.loads(c.recv(mess))
                obj = database.findSoftwareByName(name)
                ser_obj = pickle.dumps(obj)
                c.send(ser_obj)
            case "countSoftware":  # countSoftware
                c.send(pickle.dumps("count manufacturer software: waiting for manufacturer id"))
                mid = pickle.loads(c.recv(mess))
                a = database.countSoftware(mid)
                c.send(pickle.dumps(a))
            case "end":  # end
                c.close()
                break
            case _:
                c.send(pickle.dumps("wrong request"))


try:
    s = socket.socket()
    host = socket.gethostname()
    port = 8888
    s.bind((host, port))
    database = db.Database('lab2', 'postgres', 'admin', 'localhost')
    start()
    database.close()
except Exception as e:
    print(e)
