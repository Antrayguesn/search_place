from datetime import datetime
import json

from xml.dom import minidom
import xml.etree.ElementTree as ET

datapoint = {}

with open("search.database", "r") as database:
  datapoint = json.load(database)


def export() :
  # Création de l'élément
  gpx = ET.Element("gpx")
  gpx.set("version", "1.1")
  gpx.set("creator", "Aigyre Consult")
  gpx.set("xsi:schemaLocation", "http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd")
  gpx.set("xmlns", "http://www.topografix.com/GPX/1/1")
  gpx.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
   
  for id in datapoint:
    point = datapoint[id]
    wpt = ET.SubElement(gpx, "wpt")
    # Ecriture en gpx
    try:
      wpt.set('lon', "{}".format(point["longitude"]))
      wpt.set('lat', "{}".format(point["latitude"]))
    except:
      pass
    try:
      wptName = ET.SubElement(wpt, "name")
      wptName.text = point["name"]

      wptCmt = ET.SubElement(wpt, "cmt")
      wptCmt.text = point["registerName"]
    except KeyError:
      pass

    try:
      wptDesc = ET.SubElement(wpt, "desc")
      wptDesc.text = point["user_description"]
    except KeyError:
      pass
    try:
      wptDesc.text += "\n---\n"
      wptDesc.text += point["full_description"]
    except KeyError:
      pass
    try:
      wptDesc.text += "\n"
      wptDesc.text += point["link"]

    except KeyError:
      pass
    try:
      wptDesc.text += "\n"
      wptDesc.text += point["image"]
    except KeyError:
      pass
    try:
      wptLink = ET.SubElement(wpt, "link")
      wptLink.text = point["link"]
    except KeyError:
      pass


  return minidom.parseString(ET.tostring(gpx, encoding='utf-8', method='xml')).toprettyxml(indent="  ")


print(export())