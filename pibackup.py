#!/usr/bin/env python3


import os, exiftool, shutil, psutil, time, sys
from hashlib import blake2s
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setwarnings(False)

wMAAiAgzyzME = '/media/pi/'

def DZFdeMBxAsqe():
    while len(os.listdir(wMAAiAgzyzME)) == 0:
        GPIO.output(16, False)
        time.sleep(0.5)
        GPIO.output(16, True)
        time.sleep(0.5)
    JTnXaKTRqAmk = os.listdir(wMAAiAgzyzME)[0]
    destino = wMAAiAgzyzME + JTnXaKTRqAmk
    while len(os.listdir(wMAAiAgzyzME)) == 1:
        GPIO.output(16, True)
        time.sleep(0.1)
        GPIO.output(16, False)
        time.sleep(0.1)
    if JTnXaKTRqAmk == os.listdir(wMAAiAgzyzME)[0]:
        itWUkLZSYtgi = os.listdir(wMAAiAgzyzME)[1]
    else:
        itWUkLZSYtgi = os.listdir(wMAAiAgzyzME)[0]
    origen = wMAAiAgzyzME + itWUkLZSYtgi
    destino = wMAAiAgzyzME + JTnXaKTRqAmk
    if not os.path.isdir(destino + '/PiBackup/'):
        os.mkdir(destino + '/PiBackup/')
        print("'PiBackup' folder created")
    print("Source Disk  : " + itWUkLZSYtgi)
    print("Backup Disk  : " + JTnXaKTRqAmk)
    return origen, destino

def yilyHcExNhch(origen, destino):
    VveaUFUsgOSm = []
    BsvcwWAbsCUf = []
    pDeLEZWbOwww = []
    RRoLoAKgalWm = []
    time.sleep(0.2)
    for D, SD, F in os.walk(origen):
        for file in F:
            if not file.endswith('DS_Store'):
                VveaUFUsgOSm.append(file)
                path_file = os.path.join(origen, D, file)
                BsvcwWAbsCUf.append(path_file)
    for D2, SD2, F2 in os.walk(destino):
        for file2 in F2:
            if not file2.endswith('DS_Store'):
                pDeLEZWbOwww.append(file2)
                path_file2 = os.path.join(destino, D2, file2)
                RRoLoAKgalWm.append(path_file2)
    return VveaUFUsgOSm, BsvcwWAbsCUf, pDeLEZWbOwww, RRoLoAKgalWm

def UdAKmrztivjz(NaMnbtSMGexA):
        m = blake2s(digest_size=32)
        with open(NaMnbtSMGexA, 'rb') as fp:
            for chunk in fp:
                m.update(chunk)
        return m.hexdigest()

def UysvgxXAmkye(NWovQqEyeehU, YyvlUUgVnbkx, YSjSriqAVNxY, rmsNyEsmmeRy, destino):
    hvfYVfgVpFsj = destino + '/PiBackup/'
    GPIO.output(16, True)
    EZQxjCZCbPqH = False
    YbqHqHYPYihS = 0
    BOjZVevymCZB = []
    dNpgPbtbrvfQ = []
    extension = []
    tMccebhZWmOW = ('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2', 'RW2', 'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG', 'ptx', 'PTX', 'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2', 'SR2', 'tiff', 'TIFF', 'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')
    hyMujndcnCDs = ('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')
    YowPSkzxHdnf = ('hevc', 'HEVC', 'mkv', 'MKV', 'avi', 'AVI', 'mov', 'MOV', 'wmv', 'WMV', 'mp4', 'MP4', 'm4p', 'M4P', 'm4v', 'M4V', 'mpg', 'MPG', 'mpeg', 'MPEG', 'lrv', 'LRV')
    if sys.argv[1] == 'j':
        extension = hyMujndcnCDs
    elif sys.argv[1] == 'r':
        extension = tMccebhZWmOW
    elif sys.argv[1] == 'v':
        extension = YowPSkzxHdnf
    elif sys.argv[1] == 'jr':
        extension = hyMujndcnCDs + tMccebhZWmOW
    elif sys.argv[1] == 'jrv':
        extension = hyMujndcnCDs + tMccebhZWmOW + YowPSkzxHdnf
    for a in range(len(NWovQqEyeehU)):
        EZQxjCZCbPqH = False
        eEpRjWDtnDeN  = os.path.getsize(YyvlUUgVnbkx[a])
        if NWovQqEyeehU[a].endswith((extension)):
            bjQZtXaKgfTV, gByWmzDRWpsE = os.path.splitext(NWovQqEyeehU[a])
            for b in range(len(YSjSriqAVNxY)):
                if EZQxjCZCbPqH == False:
                    if bjQZtXaKgfTV in YSjSriqAVNxY[b] and YSjSriqAVNxY[b].endswith(gByWmzDRWpsE):
                        if NWovQqEyeehU[a] == YSjSriqAVNxY[b]:
                            azHtmCiRMOeb = os.path.getsize(rmsNyEsmmeRy[b])
                            if eEpRjWDtnDeN == azHtmCiRMOeb:
                                EZQxjCZCbPqH = True
                            else:
                                n = 1
                                KbHpyXAzLHVk = UdAKmrztivjz(YyvlUUgVnbkx[a])
                                PlGouTmCMDmz, pLdQFITHSlQX = os.path.splitext(rmsNyEsmmeRy[b])
                                while os.path.isfile(PlGouTmCMDmz[:-1] + str(n) + gByWmzDRWpsE):
                                    path = os.path.join(PlGouTmCMDmz[:-1] + str(n) + pLdQFITHSlQX)
                                    OziFlMFCGbUo = UdAKmrztivjz(path)
                                    if KbHpyXAzLHVk == OziFlMFCGbUo:
                                        EZQxjCZCbPqH = True
                                    n += 1
                        else:
                            n = 1
                            KbHpyXAzLHVk = UdAKmrztivjz(YyvlUUgVnbkx[a])
                            PlGouTmCMDmz, pLdQFITHSlQX = os.path.splitext(rmsNyEsmmeRy[b])
                            while os.path.isfile(PlGouTmCMDmz[:-1] + str(n) + gByWmzDRWpsE):
                                path = os.path.join(PlGouTmCMDmz[:-1] + str(n) + pLdQFITHSlQX)
                                OziFlMFCGbUo = UdAKmrztivjz(path)
                                if KbHpyXAzLHVk == OziFlMFCGbUo:
                                    EZQxjCZCbPqH = True
                                n += 1
            if not EZQxjCZCbPqH:
                BOjZVevymCZB.append(NWovQqEyeehU[a])
                dNpgPbtbrvfQ.append(YyvlUUgVnbkx[a])
                YbqHqHYPYihS += eEpRjWDtnDeN
    print('\nFiles to copy      : ' + str(len(BOjZVevymCZB)))
    print('Size of Backup     : ' + str(round((YbqHqHYPYihS/1000000000),3)) + ' GB')
        
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_usage = psutil.disk_usage(partition.mountpoint)
        if partition.mountpoint == destino:
            jJgBIeUATePB = partition_usage.free/1000000000
            print('Available Space    : ' +str(round(jJgBIeUATePB,1)) + ' GB') 
    if (YbqHqHYPYihS/1000000000) < jJgBIeUATePB:
        return BOjZVevymCZB, dNpgPbtbrvfQ
    else:
        print("\nNot enough space on 'Backup Disk' to make Backup !")
    
def CYbBSxrfCBuR(HtaVsyPuNItp, DuVRhAAMEhiG, YSjSriqAVNxY , destino):
    hvfYVfgVpFsj = destino + '/PiBackup/'
    fQzGPNBDLfno = 0
    HgbPkkZzMYMO = False
    print('\ncopying files...\n')
    for a in range(len(HtaVsyPuNItp)):
        for b in range(len(YSjSriqAVNxY)):
            if HtaVsyPuNItp[a] == YSjSriqAVNxY[b]:
                HgbPkkZzMYMO = True
        if HgbPkkZzMYMO:
            n = 1
            bjQZtXaKgfTV,extension = os.path.splitext(HtaVsyPuNItp[a])
            while (bjQZtXaKgfTV + "_" + str(n) + extension) in  YSjSriqAVNxY:
                n += 1
            shutil.copy2(DuVRhAAMEhiG[a], hvfYVfgVpFsj + bjQZtXaKgfTV + "_" + str(n) + extension)
            YSjSriqAVNxY.append(bjQZtXaKgfTV + "_" + str(n) + extension)
            if fQzGPNBDLfno == 0:
                GPIO.output(16, False)
                time.sleep(0.05)
                fQzGPNBDLfno = 1
            else:
                GPIO.output(16, True)
                time.sleep(0.05)
                fQzGPNBDLfno = 0
        else:
            shutil.copy2(DuVRhAAMEhiG[a], hvfYVfgVpFsj + HtaVsyPuNItp[a])
            YSjSriqAVNxY.append(HtaVsyPuNItp[a])
            if fQzGPNBDLfno == 0:
                GPIO.output(16, False)
                time.sleep(0.05)
                fQzGPNBDLfno = 1
            else:
                GPIO.output(16, True)
                time.sleep(0.05)
                fQzGPNBDLfno = 0
                
def ZeStZorYunQQ(destino):
    GXbSJlnbVytb = destino + '/PiBackup/'
    EdVwpRPABSnj = 0
    fQzGPNBDLfno = 0
    excludes = os.listdir(GXbSJlnbVytb)
    for dirName, subdirList, fileList in os.walk(GXbSJlnbVytb):
        subdirList[:] = [d for d in subdirList if d not in excludes]
        if len(fileList) > 0:
            print("\nprocessing exif from files...")
            for fname in fileList:
                path = os.path.join(GXbSJlnbVytb, dirName, fname)
                with exiftool.ExifToolHelper() as et:
                    make = et.get_tags(path, 'Make')
                    model = et.get_tags(path, 'Model')
                    pfQUBuCqCBsC = make[0]['EXIF:Make']
                    cnbFayrIbPgc = model[0]['EXIF:Model']
                    if pfQUBuCqCBsC==None:
                        fYayzeBoQXwo = GXbSJlnbVytb + 'other_files/'
                        destino_nuevo = fYayzeBoQXwo + fname
                        if not os.path.isdir(fYayzeBoQXwo):
                            os.mkdir(fYayzeBoQXwo)
                        shutil.move(path, destino_nuevo)
                    else:
                        fYayzeBoQXwo = GXbSJlnbVytb + str(pfQUBuCqCBsC) + " " + str(cnbFayrIbPgc) + '/'
                        destino_nuevo = fYayzeBoQXwo + fname
                        if not os.path.isdir(fYayzeBoQXwo):
                            os.mkdir(fYayzeBoQXwo)
                        shutil.move(path, destino_nuevo)
                    if fQzGPNBDLfno == 0:
                        GPIO.output(16, False)
                        time.sleep(0.05)
                        fQzGPNBDLfno = 1
                    else:
                        GPIO.output(16, True)
                        time.sleep(0.05)
                        fQzGPNBDLfno = 0
                EdVwpRPABSnj += 1
        print("\n("+ str(EdVwpRPABSnj) + " exif from files processed)")

def CevnMdEjRHAP(destino):
    GXbSJlnbVytb = destino + '/PiBackup/'
    DBiEYimuhzcB = 0
    DdSCZbJpSoYV = 0
    carpetas = os.listdir(GXbSJlnbVytb)
    carpetas.sort()
    for x in range(len(carpetas)):
        OmntrszsLzLr = GXbSJlnbVytb + carpetas[x] + '/'
        excludes = os.listdir(OmntrszsLzLr)
        for D, sD, f in os.walk(OmntrszsLzLr):
            sD[:] = [d for d in sD if d not in excludes]
            for file in f:
                path = os.path.join(OmntrszsLzLr + file)
                if file.endswith(('jpeg', 'JPEG', 'jpg', 'JPG', 'heic', 'HEIC', 'heif', 'HEIF')):
                    if DBiEYimuhzcB == 0:
                        APLzrTQIuILA = OmntrszsLzLr + 'JPG/'
                        if not os.path.isdir(APLzrTQIuILA):
                            os.mkdir(APLzrTQIuILA)
                        DBiEYimuhzcB = 1
                    shutil.move(path, APLzrTQIuILA + file)
                if file.endswith(('raf', 'RAF', 'crw', 'CRW', 'cr2', 'CR2', 'cr3', 'CR3', 'rw2', 'RW2', 'nef', 'NEF', 'nrw', 'NRW', 'orf', 'ORF', 'dng', 'DNG', 'ptx', 'PTX', 'pef', 'PEF', 'arw', 'ARW', 'srf', 'SRF', 'sr2', 'SR2', 'tiff', 'TIFF', 'thm', 'THM', 'fff', 'FFF', 'gpr', 'GPR')):
                    if DdSCZbJpSoYV == 0:
                        YKpmLtQKQcMn = OmntrszsLzLr + 'RAW/'
                        if not os.path.isdir(YKpmLtQKQcMn):
                            os.mkdir(YKpmLtQKQcMn)
                        DdSCZbJpSoYV = 1
                    shutil.move(path, YKpmLtQKQcMn + file)
    print("(files separated by extension)")
    

def eRMbMkhQgDZo(path_o, path_d):
    CLGHTwVOSJdH = 0
    while CLGHTwVOSJdH < 4:
        GPIO.output(16, False)
        time.sleep(0.8)
        GPIO.output(16, True)
        time.sleep(0.8)
        CLGHTwVOSJdH += 1
    GPIO.cleanup()
    cmd1 = 'sudo eject ' + path_o
    cmd2 = 'sudo eject ' + path_d
    os.system(cmd1)
    os.system(cmd2)
    print('\n' + "End (Disk unmounted!)")
    
def lpgedgRvscuN():
    print("***** PiBackup *****" + '\n')
    GLAzknYigBBj, scaMEaStcIXI = DZFdeMBxAsqe()
    lista_nom_o, lista_p_o, lista_nom_d, lista_p_d = yilyHcExNhch(GLAzknYigBBj, scaMEaStcIXI)
    NIVSdBFmxAAv, iryNaBvlWWyW = UysvgxXAmkye(lista_nom_o, lista_p_o, lista_nom_d, lista_p_d, scaMEaStcIXI)
    if len(NIVSdBFmxAAv) == 0:
        print("\nNo new files to backup")
    else:
        CYbBSxrfCBuR(NIVSdBFmxAAv, iryNaBvlWWyW, lista_nom_d, scaMEaStcIXI)
    ZeStZorYunQQ(scaMEaStcIXI)
    CevnMdEjRHAP(scaMEaStcIXI)
    eRMbMkhQgDZo(GLAzknYigBBj, scaMEaStcIXI)         
    
    
####################################### PIBACKUP #######################################
lpgedgRvscuN()