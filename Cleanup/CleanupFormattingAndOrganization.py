import os, shutil

def remove_strPrefix(strDirPath, strPrefix):
    try:
        arrFiles = os.listdir(strDirPath)
        arrTargetFiles = [f for f in arrFiles if f.startswith(strPrefix)]
        
        for strFilename in arrTargetFiles:
            if ".DS_Store" == strFilename: continue
            strNewFilename = strFilename[len(strPrefix):] 
            strOldFilename = os.path.join(strDirPath, strFilename)
            strNewFilepath = os.path.join(strDirPath, strNewFilename)
            
            os.rename(strOldFilename, strNewFilepath)
            print(f"Renamed file: {strFilename} -> {strNewFilename}")
        
    except Exception as ex:
        print(f"\tERROR\nAn error occurred: {str(ex)}")


def moveToOwnFolders(strDirPath):
    try:
        arrFiles = [f for f in os.listdir(strDirPath) if os.path.isfile(os.path.join(strDirPath, f))]
        
        for strFilename in arrFiles:
            if ".DS_Store" == strFilename: continue
            strFilepath = os.path.join(strDirPath, strFilename)
            strFoldername, _ = os.path.splitext(strFilename)
            strFolderPath = os.path.join(strDirPath, strFoldername)
            
            os.makedirs(strFolderPath, exist_ok=True)
            shutil.move(strFilepath, os.path.join(strFolderPath, strFilename))
            
            print(f"Moved file: {strFilename} -> {strFoldername}/{strFilename}")
        
    except Exception as ex:
        print(f"\tERROR\nAn error occurred: {str(ex)}")


def readFilesRecursively(strRootFolder):
    try:
        for strFoldername, arrSubFolders, arrFilenames in os.walk(strRootFolder):
            for strFilename in arrFilenames:
              
                if ".DS_Store" == strFilename: continue
                strFilepath = os.path.join(strFoldername, strFilename)
                try:
                    with open(strFilepath, 'r') as objFile:
                        strContent = objFile.read()
                        print(len(strContent), strFilepath)
                        #Cleanup functions could be placed here as needed.
                except Exception as ex:
                    print(f"\tERROR\nCould not read file {strFilepath} due to {str(ex)}")
    except Exception as ex:
        print(f"\tERROR\nAn error occurred: {str(ex)}")



