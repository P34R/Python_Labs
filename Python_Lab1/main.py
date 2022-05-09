import xml
import xml.dom.minidom
import xml.sax

import lxml
import lxml.etree
import things


class Company:
    manufacturers = []

    software = []

    def getManufacturer(self, id: int):
        for facture in self.manufacturers:
            if facture.id == id:
                return facture

    def getSoftwareInd(self, ind: int):
        if len(self.software) <= ind or ind < 0:
            return -1
        return self.software[ind]

    def getSoftware(self, mid: int, id: int):
        for soft in self.software:
            if soft.manufacturer.id == mid:
                if soft.id == id:
                    return soft
        return -1

    def saveToFile(self, filename: str):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('root')
        doc.appendChild(root)
        for manufac in self.manufacturers:
            manufacturer = doc.createElement('manufacturer')

            mid = doc.createAttribute('id')
            mid.value=str(manufac.id)

            mname = doc.createAttribute('name')
            mname.value=manufac.name

            manufacturer.setAttributeNode(mid)
            manufacturer.setAttributeNode(mname)

            for soft in self.software:
                if soft.manufacturer == manufac:
                    software = doc.createElement('software')

                    sid = doc.createAttribute('id')
                    sid.value=str(soft.id)

                    sname = doc.createAttribute('name')
                    sname.value = soft.name

                    sversion = doc.createAttribute('version')
                    sversion.value=str(soft.version)

                    software.setAttributeNode(sid)
                    software.setAttributeNode(sname)
                    software.setAttributeNode(sversion)

                    manufacturer.appendChild(software)
            root.appendChild(manufacturer)
        xml_str = doc.toprettyxml(indent="\t")
        with open(filename, "w") as f:
            f.write(xml_str)

    def addManufacturer(self, manufacturer: things.Manufacturer):
        for m in self.manufacturers:
            if m.id == manufacturer.id:
                return False

        self.manufacturers.append(manufacturer)
        return True

    def addSoftware(self, soft: things.Software):
        for s in self.software:
            if s.id == soft.id and s.manufacturer.id==soft.manufacturer.id:
                return False
        self.software.append(soft)
        return True

    def addSoftware_(self, id: int, name: str, version: float, manufacturer: things.Manufacturer):
        a = things.Software(id, name, version, manufacturer)
        self.addSoftware(a)

    def addManufacturer_(self, id: int, name: str):
        a = things.Manufacturer(id, name)
        self.addManufacturer(a)

    def deleteManufacturer(self, id: int):
        self.deleteSoftwareManuf(id)
        for i, m in enumerate(self.manufacturers):
            if m.id == id:
                self.manufacturers.pop(i)
                break

    def deleteSoftwareInd(self, ind: int):
        self.software.pop(ind)

    def deleteSoftware(self, mid: int, id: int):
        for i, s in enumerate(self.software):
            if s.manufacturer.id == mid and s.id == id:
                self.software.pop(i)
                break

    def deleteSoftwareManuf(self, mid: int):
        d = []
        for i, s in enumerate(self.software):
            if s.manufacturer.id == mid:
                d.insert(0, i)
        while len(d) != 0:
            self.deleteSoftwareInd(d[0])
            d.pop(0)


def HandleRoot(node):
    manufacturers = node.getElementsByTagName("manufacturer")
    array = Company()
    for m in manufacturers:
        manufac, softs = HandleManufacturer(m)
        for soft in softs:
            array.addSoftware(soft)
        array.addManufacturer(manufac)
    return array


def HandleManufacturer(node):
    id = int(node.getAttribute("id"))
    name = node.getAttribute("name")
    m = things.Manufacturer(id, name)
    array = []
    software = node.getElementsByTagName("software")
    for soft in software:
        s = HandleSoftware(soft)
        s.setManufacturer(m)
        array.append(s)
    return m, array


def HandleSoftware(node):
    id = int(node.getAttribute("id"))
    name = node.getAttribute("name")
    version = float(node.getAttribute("version"))
    soft = things.Software(id, name, version, None)
    return soft


def __main__():
    tree = xml.dom.minidom.parse("xml.xml")
    validator = lxml.etree.XMLSchema(file="xml.xsd")
    file = lxml.etree.parse("xml.xml")
    if not validator.validate(file):
        print("validation failed")
        return
    else:
        print("xml validation completed. No errors")
    manufacs = HandleRoot(tree)
    for a in manufacs.manufacturers:
        print(a.toString())
    for b in manufacs.software:
        print(b.toString())
    manufacs.addSoftware_(3,"IntelliJ",2.2,manufacs.getManufacturer(2))
    manufacs.addManufacturer_(3,"Meta")
    manufacs.addSoftware_(1,"Facebook",1.1,manufacs.getManufacturer(3))
    manufacs.deleteSoftware(2,1)
    manufacs.deleteManufacturer(1)
    print("\nafter\n\n")
    for a in manufacs.manufacturers:
        print(a.toString())
    for b in manufacs.software:
        print(b.toString())
    manufacs.saveToFile("xml.xml")

__main__()
"""

Програмне забезпечення
Об'єкти 
Виробники, manufacturer
Програмні продукти software

Примітка 
Програмні продукти
згруповані по виробникам.
Для кожного виробника
задано множину продуктів.

Перевірка
структури
документа XML

Схема XML


"""
