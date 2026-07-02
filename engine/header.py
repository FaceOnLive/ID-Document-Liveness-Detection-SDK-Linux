import os

from ctypes import *
from numpy.ctypeslib import ndpointer

def print_log(fmt): print("[LOG] \033[98m{}\033[00m" .format(fmt))
def print_info(fmt): print("[INFO] \033[92m{}\033[00m" .format(fmt))
def print_error(fmt): print("[ERR] \033[91m{}\033[00m" .format(fmt)) 
def print_warning(fmt): print("[WARNING] \033[93m{}\033[00m" .format(fmt))


libPath = os.path.abspath(os.path.dirname(__file__)) + '/lib/libidlivesdk.so'
libidlivesdk = cdll.LoadLibrary(libPath)

get_deviceid = libidlivesdk.getHWID
get_deviceid.argtypes = []
get_deviceid.restype = c_char_p

set_activation = libidlivesdk.setLicenseKey
set_activation.argtypes = [c_char_p]
set_activation.restype = c_int32

init_sdk = libidlivesdk.initSDK
init_sdk.argtypes = [c_char_p]
init_sdk.restype = c_int32

processImage = libidlivesdk.processImage
processImage.argtypes = [ndpointer(c_ubyte, flags='C_CONTIGUOUS'), c_int32, c_int32]
processImage.restype = c_char_p

