import xml.etree.ElementTree as ET
import numpy as np
import cv2 as cv
# def read_calib_matrix(path ) : 
#     """"
#     Function that read the XML file made with Metashape and gives the camera matrix and distortion coefficients
#     Parameters
#     ----------
#     path : string
#         path of where the XML file is located
#     name : string
#         name of the XML file
#     Returns
#     -------
#     mtx : <class 'list'>
#         camera matrix
#     dist : <class 'numpy.ndarray'>
#         distortion coefficients
#     """
#     print(path)
#     tree = ET.parse(path)
#     root = tree.getroot()
#     mtx =root[3][3].text
#     mtx = mtx.split(' ')
#     matrix = np.zeros((1,9))
#     k = 0
#     for i in range(len(mtx)) :
#         mtx[i] = (mtx[i]).strip('\n')
#         if mtx[i]!='':
#             matrix[0,k] = float(mtx[i])
#             k +=1
#     matrix = matrix.reshape((3,3))

#     disto = root[4][3].text
#     disto = disto.split(' ')
#     t = len(disto)
#     dist = np.zeros((1,t))
#     k = 0
#     for i in range(t) : 
#         disto[i] = (disto[i]).strip('\n')
#         if disto[i]!='':
#             dist[0,k] = float(disto[i])
#             k +=1
#     return matrix, dist

def read_calib_matrix(fname): 
    """"
    Function that read the XML file made with Metashape and gives the camera matrix and distortion coefficients
    Parameters
    ----------
    fname : string
        name of the XML file

    Returns
    -------
    mtx : <class 'list'>
        camera matrix
    dist : <class 'numpy.ndarray'>
        distortion coefficients
    """
    fs = cv.FileStorage(fname, cv.FILE_STORAGE_READ)
    mtx = fs.getNode("Camera_Matrix").mat()
    dist = fs.getNode("Distortion_Coefficients").mat()
    return mtx, dist