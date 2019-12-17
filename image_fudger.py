from PIL import Image
import argparse
import piexif
import os.path
import sys
from random import seed
from random import randint
from random import uniform
from datetime import datetime
from math import modf

def rand_orientation( current_orientation ):
    new_orientation = current_orientation
    
    seed( datetime.now() )
    
    while( new_orientation == current_orientation ):
        new_orientation = randint( 1, 8 )

    return new_orientation 

# thanks kind stranger:
def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

# YYYY:MM::DD HH:MM:SS with time shown in 24-hour format and the date and time separated by one blank
def random_datetime( ):
    return 0

def random_lat_long( cur_lat, cur_lat_ref, cur_long, cur_long_ref ):


    seed( datetime.now() )

    # random lat
    ngps = uniform(0, 90)

    (rest, new_lat_degrees) = modf( ngps )
    (rest, new_lat_mins) = modf( rest * 60 )
    (rest, new_lat_secs) = modf( rest * 60 )

    new_lat_ref = ''
    if randint(1,11) % 2 == 0:
        new_lat_ref = 'N'
    else:
        new_lat_ref = 'S'

    # random long
    ngps = uniform(0, 90)

    (rest, new_long_degrees) = modf( ngps )
    (rest, new_long_mins) = modf( rest * 60 )
    (rest, new_long_secs) = modf( rest * 60 )

    new_long_ref = ''
    if randint(1,11) % 2 == 0:
        new_long_ref = 'E'
    else:
        new_long_ref = 'W'


    return (
        ( (new_lat_degrees, 1), (new_lat_mins, 1), (new_lat_secs,1 ) ), new_lat_ref,
        ( (new_long_degrees, 1), (new_long_mins, 1), (new_long_secs,1 ) ), new_long_ref,
    )
    

    

def main():

    # Argument Parser Stuff ###################################################
    ap = argparse.ArgumentParser( description="Muck around with the data in an image" )

    ap.add_argument( '-i', '--imagepath', required=True,
        help='the full path to the source image we want to change' )
    ap.add_argument( '-n', '--newfilename', required=True,
        help='the name of the output file to create' )
    ap.add_argument( '-o', '--orientation', action='store_true',
        help='randomize the exif orientation of the image')
    ap.add_argument( '-g', '--gps', action='store_true',
        help='randomize the exif GPS location of an image')
    ap.add_argument( '-d', '--datetime', action='store_true',
        help='randomize the exif datetime of an image')

    args = ap.parse_args()

    # Check sanity 
    
    if not os.path.isfile( args.imagepath ):
        print("Error: couldn't open source image file")
        sys.exit(-1) 

    with Image.open( args.imagepath ) as source_image:
        exif_dict = piexif.load( source_image.info['exif'] )
        exif_copy = exif_dict.copy()
        
        if args.orientation:
            new_orientation = rand_orientation(exif_dict[ '0th'][piexif.ImageIFD.Orientation])
            exif_copy['0th'][piexif.ImageIFD.Orientation] = new_orientation

            print("Altering orientation: {}->{}".format( exif_dict[ '0th'][piexif.ImageIFD.Orientation],
                 new_orientation) )
        
        if args.gps:
            print("Altering gps")
            
            print("{} {} {} {}".format( exif_dict['GPS'][piexif.GPSIFD.GPSLatitude], 
                exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef],  
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitude],  
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] ) ) 

            random_lat_long(  exif_dict['GPS'][piexif.GPSIFD.GPSLatitude], 
                exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef],  
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitude],  
                exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] ) 

        if args.datetime:
            print("Altering datetime") 
        
        source_image.save( args.newfilename, exif=piexif.dump(exif_copy) )

if __name__ == "__main__":
    main()
