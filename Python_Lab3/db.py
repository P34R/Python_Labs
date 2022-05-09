import psycopg2
import random
import things


class Database:

    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.cursor = self.conn.cursor()

    def getManufacturer(self, id: int):
        sql = 'SELECT * from manufacturers where id=%s'
        try:
            self.cursor.execute(sql, (id,))
            res = self.cursor.fetchone()
            return things.Manufacturer(res[0], res[1])
        except:
            raise Exception("ERROR: get manufacturer error, there is no such manufacturer with id = %s" % id)

    def getSoftware(self, id: int):
        sql = 'SELECT * from software where id=%s'
        try:
            self.cursor.execute(sql, (id,))
            res = self.cursor.fetchone()
            manuf = self.getManufacturer(res[3])
            return things.Software(res[0], res[1], res[2], manuf)
        except:
            raise Exception("ERROR: get manufacturer error, there is no such software with id = %s" % id)

    def getAllManufSoftware(self, mid: int):
        sql = 'SELECT * from software where manufacturer_id=%s'
        try:
            manuf = self.getManufacturer(mid)
            self.cursor.execute(sql, (mid,))
            res = self.cursor.fetchall()
            software = []
            for r in res:
                software.append(things.Software(r[0], r[1], r[2], manuf))
            return software
        except:
            raise Exception(
                "ERROR: get all manufacture software error, there is no such manufacturer or software with manufacturer id = %s" % mid)

    def addManufacturer(self, m: things.Manufacturer):
        sql = 'INSERT INTO manufacturers (name) VALUES (%s) RETURNING id'
        try:
            self.cursor.execute(sql, (m.name,))
            m.id=self.cursor.fetchone()[0]
            self.conn.commit()
        except:
            raise Exception("ERROR: add manufacturer error")

    def addSoftware(self, s: things.Software):
        sql = 'INSERT INTO software (name,version,manufacturer_id) VALUES (%s,%s,%s) RETURNING id'
        try:
            data = (s.name, s.version, s.manufacturer.id)
            self.cursor.execute(sql, data)
            s.id=self.cursor.fetchone()[0]
            self.conn.commit()
        except:
            raise Exception(
                "ERROR: add software error, probably there is no such manufacturer with id = " % s.manufacturer.id)

    def delSoftware(self, id: int):
        sql = 'DELETE FROM software where id=%s'
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
        except:
            raise Exception("ERROR: delete software error, there is no such software with id = %s" % id)

    def delAllManufSoftware(self, mid: int):
        sql = 'DELETE FROM software where manufacturer_id=%s'
        try:
            self.cursor.execute(sql, (mid,))
            self.conn.commit()
        except:
            raise Exception(
                "ERROR: delete all manufacture software error, there is no software for this id or there is no such manufacturer with id = %s" % mid)

    def delManufacturer(self, id: int):
        sql = 'DELETE FROM manufacturers where id=%s'
        self.delAllManufSoftware(id)
        try:
            self.cursor.execute(sql, (id,))
            self.conn.commit()
        except:
            raise Exception("ERROR: delete software error, there is no such manufacturer with id = %s" % id)

    def editSoftware(self, id: int, soft: things.Software):
        sql = 'UPDATE software set name=%s, version=%s, manufacturer_id=%s where id=%s'
        try:
            self.cursor.execute(sql, (soft.name, soft.version, soft.manufacturer.id, id))
            self.conn.commit()
        except:
            raise Exception("ERROR: edit software error, probably there is no such software")

    def findSoftwareByName(self, name: str):
        sql = 'SELECT * from software where name=%s'
        try:
            self.cursor.execute(sql, (name,))
            res = self.cursor.fetchall()
            software = []
            for i in res:
                software.append(things.Software(i[0], i[1], i[2], self.getManufacturer(i[3])))
            return software
        except:
            raise Exception("ERROR: Get software by name error")

    def countSoftware(self, mid: int):
        sql = 'SELECT count(*) from software WHERE manufacturer_id = %s;'
        try:
            self.cursor.execute(sql, (mid,))
            res = self.cursor.fetchone()
            return res[0]
        except:
            raise Exception("ERROR: count software error")

    def getAllManufacturers(self):
        sql = 'SELECT * from manufacturers'
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            manufacturers = []
            for i in res:
                manufacturers.append(things.Manufacturer(i[0], i[1]))
            return manufacturers
        except:
            raise Exception("ERROR: getting all manufacturers error")

    def close(self):
        self.cursor.close()
        self.conn.close()
