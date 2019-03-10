import csv
import xml.dom.minidom
import sys


def extractAddress(row):
    # This extracts an address from a row and returns it as a string. This requires knowing
    # ahead of time what the columns are that hold the address information.
    return '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (row['utc_time'], row['gps_lat'], row['gps_long'], row['gps_alti'], row['baro_alti'], row['baro_temp'], row['accel.x'], row['accel.y'], row['accel.z'], row['gyro.x'], row['gyro.y'], row['gyro.z'], row['mag.x'], row['mag.y'], row['mag.z'], row['system'])


def createPlacemark(kmlDoc, coordinatesString):
    # <Placemark>
    placemarkElement = kmlDoc.createElement('Placemark')

    # <Point>
    styleUrlElement = kmlDoc.createElement('styleUrl')
    styleUrlText = kmlDoc.createTextNode('#randomColorIcon')
    styleUrlElement.appendChild(styleUrlText)
    placemarkElement.appendChild(styleUrlElement)

    # <Point>
    pointElement = kmlDoc.createElement('Point')
    placemarkElement.appendChild(pointElement)

    # <altitudeMode>
    altitudeElement = kmlDoc.createElement('altitudeMode')
    altitudeText = kmlDoc.createTextNode('absolute')
    altitudeElement.appendChild(altitudeText)
    pointElement.appendChild(altitudeElement)

    # add coordinates string
    coordinates = coordinatesString
    coorElement = kmlDoc.createElement('coordinates')
    coorElement.appendChild(kmlDoc.createTextNode(coordinates))
    pointElement.appendChild(coorElement)

    # Return this marker
    return placemarkElement

# <Style id="randomColorIcon">
#       <IconStyle>
#          <color>ff00ff00</color>
#          <colorMode>random</colorMode>
#          <scale>1.1</scale>
#          <Icon>
#             <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
#          </Icon>
#       </IconStyle>
#    </Style>

def createIconStyle(kmlDoc):
    # <Style>
    styleElement = kmlDoc.createElement('Style')
    styleElement.setAttribute('id', 'randomColorIcon')

    # <IconStyle>
    iconStyleElement = kmlDoc.createElement('IconStyle')
    styleElement.appendChild(iconStyleElement)

    # <color>
    colorElement = kmlDoc.createElement('color')
    colorText = kmlDoc.createTextNode('ff00ff00')
    colorElement.appendChild(colorText)
    iconStyleElement.appendChild(colorElement)

    # <Icon>
    iconElement = kmlDoc.createElement('Icon')
    iconStyleElement.appendChild(iconElement)

    # <href>
    hrefElement = kmlDoc.createElement('href')
    hrefText = kmlDoc.createTextNode('http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png')
    hrefElement.appendChild(hrefText)
    iconElement.appendChild(hrefElement)

    # Return this marker
    return styleElement


def createKML(csvReader, fileName, order):
    # This constructs the KML document from the CSV file.
    kmlDoc = xml.dom.minidom.Document()
    kmlElement = kmlDoc.createElementNS(
        'http://earth.google.com/kml/2.2', 'kml')
    kmlElement.setAttribute('xmlns', 'http://earth.google.com/kml/2.2')
    kmlElement = kmlDoc.appendChild(kmlElement)

    # <document>
    documentElement = kmlDoc.createElement('Document')
    documentElement = kmlElement.appendChild(documentElement)

    # define different icon
    styleElement = createIconStyle(kmlDoc)
    documentElement.appendChild(styleElement)

    # This creates a  element for a row of data. A row is a dict.
    # <Placemark>
    placemarkElement = kmlDoc.createElement('Placemark')

    # <LineString>
    pointElement = kmlDoc.createElement('LineString')
    placemarkElement.appendChild(pointElement)

    # <tessellate>
    tessellateElement = kmlDoc.createElement('tessellate')
    tessellateText = kmlDoc.createTextNode('1')
    tessellateElement.appendChild(tessellateText)
    pointElement.appendChild(tessellateElement)

    # <altitudeMode>
    altitudeElement = kmlDoc.createElement('altitudeMode')
    altitudeText = kmlDoc.createTextNode('absolute')
    altitudeElement.appendChild(altitudeText)
    pointElement.appendChild(altitudeElement)

    # Skip the header line and prepare coordinates
    csvReader.next()
    coordinates = ""

    for row in csvReader:
        # Build the string for line path
        # coordinatesString = row['gps_long'] + "," + row['gps_lat'] + "," + row['gps_alti']
        coordinatesString = row['gps_long'] + "," + row['gps_lat'] + "," + row['baro_alti']
        coordinates += coordinatesString + '\n'

        # Build each individual point
        singlePointELement = createPlacemark(kmlDoc, coordinatesString)
        documentElement.appendChild(singlePointELement)

    # Attach string of coordinates to <coordinates>
    coorElement = kmlDoc.createElement('coordinates')
    coorElement.appendChild(kmlDoc.createTextNode(coordinates))
    pointElement.appendChild(coorElement)

    # Attach the flight path to the kml document
    documentElement.appendChild(placemarkElement)

    # Write the kml document
    kmlFile = open(fileName, 'w')
    kmlFile.write(kmlDoc.toprettyxml('  ', newl='\n', encoding='utf-8'))


def main():
    # At this point, this is specifically tailored to the csv we have
    if len(sys.argv) > 1:
        order = sys.argv[1].split(',')
    else:
        order = ['utc_time', 'gps_lat',	'gps_long',	'gps_alti',	'baro_alti', 'baro_temp', 'accel.x',
                 'accel.y',	'accel.z', 'gyro.x', 'gyro.y', 'gyro.z', 'mag.x', 'mag.y', 'mag.z', 'system']

    # Begin processing our csv into kml
    csvreader = csv.DictReader(open('realdeal.csv'), order)
    kml = createKML(csvreader, 'result.kml', order)


if __name__ == '__main__':
    main()
