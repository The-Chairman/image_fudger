usage: image_fudger.py [-h] -i IMAGEPATH -n NEWFILENAME [-o] [-g] [-d] [-l]
                       [-r] [-s]
```
Muck around with the data in an image

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGEPATH, --imagepath IMAGEPATH
                        the full path to the source image we want to change
  -n NEWFILENAME, --newfilename NEWFILENAME
                        the name of the output file to create
  -o, --orientation     randomize the exif orientation of the image
  -g, --gps             randomize the exif GPS location of an image
  -d, --datetime        randomize various exif datetimes of an image
  -l, --line            add a random horizonta line to the image
  -r, --random          permute 1 percent of the pixels in this image
  -s, --summary         print a summary of the exif data of the source and the
                        manipulated copy
```
