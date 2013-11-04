Python Wrapper for L-measure.

It is advised that one be familiar with L-measure and it's functionalities before using this wrapper.

Operating systems Supported:
1. Linux 32 and 64 bit

Installation:
Linux:
Caution: Do not place these files in a system path.
 1. Copy the folder 'LMIO' wrapper to a location(for example <home directory>/installations/)
 2. Add the path '<path to LMIO>/LMIO/' to the system PYTHONPATH  by adding the following line to .profile or .bashrc

    export PYTHONPATH="$PYTHONPATH:<path to LMIO>/LMIO/"

    Source the .profile or .bashrc file.

Usage:

See the file testLMIO.py for example usage. Mainly, three functions are implemented getMeasure(), getMeasureDistribution() and
getMeasureDependence().

The general workflow:
    1. make a new LMIO object, initializing it with the path to an swcfile.
    2. call one of the three functions specifying the measures required.
    3. read output dictionary LMIO.LMOutput for the output.

Usage Notes:
    1. Set the flag LMIO.rawDataOutputFlag to 'True' to obtain the raw data in addition to the statistics which are
    usually returned. The raw data can be read from the variable 'LMIO.LMOutput['rawData']'. Remember that this can lead to large execution times and memory usage.
    2. Once an LMIO object is initialized with a swcfile path, any number of measures can be obtained on the same
    swc file by repeatedly calling the three 'get..()' methods. The results dictionary 'LMIO.LMOutput' will be refreshed
    everytime one of the 'get...()' methods is called.
    3. Look at the documentation strings for more information
