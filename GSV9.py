import pandas as pd
from streetview import search_panoramas
from streetview import get_streetview
from streetview import get_panorama_meta
import os
import csv
import requests
# Read the CSV file into a DataFrame
RobesoncoordinatesCSVFile= '/Users/andrew/Downloads/Robeson1.csv'
DurhamcoordinatesCSVFile='/Users/andrew/Downloads/AnyConv.com__DurhamCountyDataFINAL.csv'

#TestingFiles
ScotlandcoordinatesCSVFile = '/Users/andrew/Downloads/ScotlandCountyCoordinatesFinal.csv'
ColumbuscoordinatesCSVFile ='/Users/andrew/Downloads/ColumbusCountyCoordinatesFinal.csv'
WakeCountycoordinatesCSVFile = '/Users/andrew/Downloads/WakeCountyCoordinatesFinal.csv'
GuilfordCountycoordinatesCSVFile = '/Users/andrew/Downloads/GuilfordCountyCoordinatesFinal.csvele'
df = pd.read_csv(ScotlandcoordinatesCSVFile)

foldernumber = 1 #The subfolder number in the Images Folder
folder_name = f"Image/{foldernumber}" #The folder we'll save the csv files to. Foldernumber is the subfoler in the Image folder


csv_filename = 'dat2.csv' #The CSV File we'll write the image data too
ImageNumber = 0 #Initializes Image Number

# Get the first two columns
first_column = df.iloc[:, 0]
second_column = df.iloc[:, 1]
e=0
for value1, value2 in zip(first_column, second_column):
    #print(value1, value2)
    for i in range(4):  # This for loop takes 4 photos, one from every direction, for each lat and lon coordinate

        panos = search_panoramas(value1, value2)  # the lattittude and longitude of where you want the streetview image
        first = panos[0]  # There are multiple images at that location so you pick which one you want

        print(first)  # prints the pano_id for the image you want and other info
        meta = get_panorama_meta(pano_id=first.pano_id, api_key='AIzaSyCXNyCNpX62rVPyVjmHbXkqElpbZxwPNYI')

        print(meta)  # prints date the streetview was taken and other info
        date = meta.date
        direction = i
        heading = 90 * direction
        pitch = first.pitch
        roll = first.roll
        panoid= meta.pano_id

        image = get_streetview(  # Gets the actual image
            pano_id=first.pano_id,
            heading=90 * direction,
            api_key='AIzaSyCXNyCNpX62rVPyVjmHbXkqElpbZxwPNYI',
        )


        def get_address_components(value1, value2, api_key):  # Gets Street, City, State and Zip Code for the coordinate
            url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={value1},{value2}&key={api_key}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                if 'results' in data and len(data['results']) > 0:
                    result = data['results'][0]
                    address_components = result['address_components']
                    street_address = None
                    city = None
                    state = None
                    zip_code = None
                    for component in address_components:
                        types = component.get('types', [])
                        if 'street_number' in types or 'route' in types:
                            street_address = component['long_name']
                        elif 'locality' in types:
                            city = component['long_name']
                        elif 'administrative_area_level_1' in types:
                            state = component['short_name']
                        elif 'postal_code' in types:
                            zip_code = component['long_name']
                    return street_address, city, state, zip_code
                else:
                    return None, None, None, None
            else:
                print("Error:", data['error_message'])
                return None, None, None, None  ##F


        # This method finds the street_address, city, state, and zip code for the lat and long coordinates

        api_key = 'AIzaSyCXNyCNpX62rVPyVjmHbXkqElpbZxwPNYI'

        street_address, city, state, zip_code = get_address_components(value1, value2, api_key)

        file_name = f"{ImageNumber:0>7}_{i}.jpg"
        file_path = f"{folder_name}/{file_name}"
        image.save(file_path, "jpeg")  # Saves the image to a file
        imagedata = [file_name, file_path, date, value1, value2, direction,heading, street_address, city, state, zip_code, pitch, roll, panoid]
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(imagedata)
        ImageNumber += 1  # Represents how number of images taken Ex: 15 would be the 15th image taken
        if (ImageNumber % 10000 == 0):
            foldernumber += 1
            folder_name = f"Image/{foldernumber}"  # Will increaase foldernumber by 1 after we add 1000 photos to the the folder
            if not os.path.exists(
                    folder_name):  # Will make the new folder after the 10000 photos have been added. Need to add the code
                os.makedirs(folder_name)


