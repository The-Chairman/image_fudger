from PIL import Image
import argparse
import piexif
import os.path
import sys
import copy
from random import seed
from random import randint
from random import uniform
from random import random
from datetime import datetime
from math import modf
from datetime import timedelta

def rand_orientation( current_orientation ):
    new_orientation = current_orientation
    
    seed( datetime.now() )
    
    while( new_orientation == current_orientation ):
        new_orientation = randint( 1, 8 )

    return new_orientation 

# thanks kind stranger:
def gen_datetime(min_year=1900, max_year=datetime.now().year):
    # generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    seed( datetime.now() )
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random()

# YYYY:MM::DD HH:MM:SS with time shown in 24-hour format and the date and time separated by one blank
def random_datetime( ):
    return bytes( gen_datetime().strftime( "%Y:%m:%d %H:%M:%S" ), 'ascii' ) 

def random_lat_long( cur_lat, cur_lat_ref, cur_long, cur_long_ref ):
    seed( datetime.now() )

    # random lat
    ngps = uniform(0, 90)

    (rest, new_lat_degrees) = modf( ngps )
    (rest, new_lat_mins) = modf( rest * 60 )
    (rest, new_lat_secs) = modf( rest * 60 )

    new_lat_ref = ''
    if randint(1,11) % 2 == 0:
        new_lat_ref = bytes('N', 'ascii')
    else:
        new_lat_ref = bytes('S', 'ascii')

    # random long
    ngps = uniform(0, 90)

    (rest, new_long_degrees) = modf( ngps )
    (rest, new_long_mins) = modf( rest * 60 )
    (rest, new_long_secs) = modf( rest * 60 )

    new_long_ref = ''
    if randint(1,11) % 2 == 0:
        new_long_ref = bytes('E', 'ascii')
    else:
        new_long_ref = bytes('W', 'ascii')

    return [
        ( ( (int( new_lat_degrees ), 1), (int( new_lat_mins ), 1), (int( new_lat_secs ),1 ) ), 
            new_lat_ref ),
        ( ( (int( new_long_degrees ), 1), (int( new_long_mins ), 1), (int( new_long_secs ),1 ) ), 
            new_long_ref ),
    ]
    

def print_exif_summary( exif_dict ):

    
    print( "{:<12}: {}".format( "Orientation",exif_dict['0th'][piexif.ImageIFD.Orientation] if piexif.ImageIFD.Orientation in exif_dict['0th'] else "") )
    print( "{:<12}: {}".format( "Latitude", exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] if piexif.GPSIFD.GPSLatitude in exif_dict['GPS'] else "" ) )
    print( "{:<12}: {}".format( "Latitude Ref", exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] if piexif.GPSIFD.GPSLatitudeRef in exif_dict['GPS'] else "" ) )
    print( "{:<12}: {}".format( "Longitude", exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] if piexif.GPSIFD.GPSLongitude in exif_dict['GPS'] else "" ) )
    print( "{:<12}: {}".format( "Longitude Ref", exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] if piexif.GPSIFD.GPSLongitudeRef in exif_dict['GPS'] else "" ) )
    print( "{:<12}: {}".format( "DateTimeOriginal", 
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] if piexif.ExifIFD.DateTimeOriginal in exif_dict['Exif'] else "" ) )
    print( "{:<12}: {}".format( "DateTime", 
        exif_dict['0th'][piexif.ImageIFD.DateTime] if piexif.ImageIFD.DateTime in exif_dict['0th'] else "" ) )
    

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
        help='randomize various exif datetimes of an image')
    ap.add_argument( '-l', '--line', action='store_true',
        help='add a random horizonta line to the image' )
    ap.add_argument( '-r', '--random', action='store_true',
        help='permute 1% of the pixels in this image' )
    ap.add_argument( '-s', '--summary', action='store_true',
        help='print a summary of the exif data of the source and the manipulated copy')

    args = ap.parse_args()

    # Check sanity 
    
    if not os.path.isfile( args.imagepath ):
        print("Error: couldn't open source image file")
        sys.exit(-1) 

    with Image.open( args.imagepath ) as source_image:
        pixels = source_image.load()
        exif_dict = piexif.load( source_image.info['exif'] )
        exif_copy = copy.deepcopy( exif_dict )
        
        if args.orientation:
            new_orientation = rand_orientation(exif_dict[ '0th'][piexif.ImageIFD.Orientation])
            exif_copy['0th'][piexif.ImageIFD.Orientation] = new_orientation
        
        if args.gps:
            print("Altering gps")

            if not exif_dict['GPS']:
                new_gps = random_lat_long( 0, '', 0,  '') 
            else:
                new_gps = random_lat_long(  exif_dict['GPS'][piexif.GPSIFD.GPSLatitude], 
                    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef],  
                    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude],  
                    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] ) 

            exif_copy['GPS'][piexif.GPSIFD.GPSLatitude] = new_gps[0][0]
            exif_copy['GPS'][piexif.GPSIFD.GPSLatitudeRef] = new_gps[0][1]
            exif_copy['GPS'][piexif.GPSIFD.GPSLongitude] = new_gps[1][0]
            exif_copy['GPS'][piexif.GPSIFD.GPSLongitudeRef] = new_gps[1][1]

        if args.datetime:
            print("Altering datetime") 
            exif_copy['Exif'][piexif.ExifIFD.DateTimeOriginal] = random_datetime()
            exif_copy['0th'][piexif.ImageIFD.DateTime] = random_datetime()

        if args.line:
            print("Adding a line to the image")
            seed( datetime.now() )
            target_row = randint( 0, source_image.size[1] )
            random_color = ( randint( 0, 250), randint(0, 250), randint(0, 250) )
            for c in range( source_image.size[0] ):
                pixels[c, target_row] = random_color
        if args.random:
            print( "Altering 1% of the pixels of the image" )
            seed( datetime.now() )
            num_pixels = int( .01 * source_image.size[0] * source_image.size[1] )

            for i in range( num_pixels ):
                col = randint( 0, source_image.size[0] -1 )
                row = randint( 0, source_image.size[1]  -1 )
                random_color = ( randint( 0, 250), randint(0, 250), randint(0, 250) )
                pixels[col, row] = random_color
                
        print()

        source_image.save( args.newfilename, exif=piexif.dump(exif_copy) )

        if args.summary:
            print_exif_summary( exif_dict )
            print("="*40 )
            print_exif_summary( exif_copy )

if __name__ == "__main__":
    main()
