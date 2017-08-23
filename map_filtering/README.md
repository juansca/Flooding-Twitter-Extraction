# BASEMAP

## Dependencies

### **Requirements**

These are external packages which you will need to install before installing basemap.

- matplotlib 1.0.0 (or later, download)

- Python 2.4 (or later, including Python 3)
    matplotlib requires python 2.4 or later (download)

- numpy 1.2.1 (or later)
    array support for python (download)

- [PROJ4](http://proj4.org)  Cartographic Projections Library.


### Required library that ships with basemap

- [GEOS](http://trac.osgeo.org/geos/) (Geometry Engine - Open Source) library 3.1.1 or later.
    Source code is included in the geos-3.3.3 directory. When building from source, must be built and installed separately from basemap (see build instructions below). Included in Windows binary installers.


## Installing Dependencies

### **matplotlib**, **numpy**

These libraries will be installed once you execute:
```
$ pip install -r requirements.py
```
To install them, you have to be in 'Flooding-Twitter-Extraction' (the main)
directory

### **PROJ4**

Is a library for converting geospatial data to different coordinate reference systems.

First, download the PROJ.4 source code and datum shifting files [1]:

```
$ wget http://download.osgeo.org/proj/proj-4.9.1.tar.gz
$ wget http://download.osgeo.org/proj/proj-datumgrid-1.5.tar.gz
```

Next, untar the source code archive, and extract the datum shifting files in the nad subdirectory. This must be done prior to configuration:

```
$ tar xzf proj-4.9.1.tar.gz
$ cd proj-4.9.1/nad
$ tar xzf ../../proj-datumgrid-1.5.tar.gz
$ cd ..
```

Finally, configure, make and install PROJ.4:
```
$ ./configure
$ make
$ sudo make install
$ cd ..
```

### **GEOS**

GEOS is a C++ library for performing geometric operations, and is the default internal geometry representation used by GeoDjango (it’s behind the “lazy” geometries). Specifically, the C API library is called (e.g., libgeos_c.so) directly from Python using ctypes.

First, download GEOS 3.4.2 from the GEOS website and untar the source archive:

```
$ wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
$ tar xjf geos-3.4.2.tar.bz2
```
Next, change into the directory where GEOS was unpacked, run the configure script, compile, and install:
```
$ cd geos-3.4.2
$ ./configure
$ make
$ sudo make install
$ cd ..
```

### BaseMap

Once dependencies are installed, download and untar the source archive. Finally
install it.
```
$ wget https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz
$ tar xzf v1.1.0.tar.gz
$ cd ALGUNLADO
$ python setup.py install
```
