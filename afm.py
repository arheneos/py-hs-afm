import struct
import datetime
import numpy as np


class ASDFrame:
    __slots__ = [
        'raw',
        'frameNum',
        'x',
        'y',
        'maxData',
        'minData',
        'xOffset',
        'yOffset',
        'xTilt',
        'yTilt',
        'irradiation',
        'bookedByte',
        'bookedShort',
        'bookedInt1',
        'bookedInt2',
        'zOffset',
        'scalingFactor',
        'image'
    ]

    def __init__(self, raw: bytes, x: int, y: int, offset: int, scaling_factor: float, normalize: bool):
        self.raw = raw
        self.x = x
        self.y = y
        self.zOffset = offset
        self.scalingFactor = scaling_factor
        self._read_header_(normalize=normalize)

    def _read_header_(self, normalize=False):
        self.frameNum = struct.unpack('<i', self.raw[0:4])
        self.raw = self.raw[4:]
        self.maxData = struct.unpack('<h', self.raw[0:2])[0]
        self.raw = self.raw[2:]
        self.minData = struct.unpack('<h', self.raw[0:2])[0]
        self.raw = self.raw[2:]
        self.xOffset = struct.unpack('<h', self.raw[0:2])
        self.raw = self.raw[2:]
        self.yOffset = struct.unpack('<h', self.raw[0:2])
        self.raw = self.raw[2:]
        self.xTilt = struct.unpack('<f', self.raw[0:4])
        self.raw = self.raw[4:]
        self.yTilt = struct.unpack('<f', self.raw[0:4])
        self.raw = self.raw[4:]
        self.irradiation = struct.unpack('<c', self.raw[0:1])
        self.raw = self.raw[1:]
        self.bookedByte = struct.unpack('<c', self.raw[0:1])
        self.raw = self.raw[1:]
        self.bookedShort = struct.unpack('<h', self.raw[0:2])
        self.raw = self.raw[2:]
        self.bookedInt1 = struct.unpack('<i', self.raw[0:4])
        self.raw = self.raw[4:]
        self.bookedInt2 = struct.unpack('<i', self.raw[0:4])
        self.raw = self.raw[4:]
        self.image = np.frombuffer(self.raw[0:2 * self.x * self.y], dtype=np.short)
        self.image = np.reshape(self.image, (self.y, self.x),)
        if normalize:
            self.image = (self.image + self.zOffset) * self.scalingFactor
        else:
            self.image = self.image + self.zOffset

    def __len__(self) -> int:
        return 32 + 2 * self.x * self.y

    def __bytes__(self):
        return self.raw


class ASDReader:
    __slots__ = [
        'filename',
        'raw',
        'fileVersion',
        'headSize',
        'frameHeaderSize',
        'encoding',
        'operatorNameLength',
        'commentSize',
        'rawType1ch',
        'rawType2ch',
        'frameNum',
        'currentFrameNum',
        'scanDirection',
        'asdFileName',
        'xPixel',
        'yPixel',
        'xScanRange',
        'yScanRange',
        'averageFlag',
        'averageNum',
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'xRoundDeg',
        'yRoundDeg',
        'frameAcquisTime',
        'sensorSens',
        'phaseSens',
        'offset',
        'booked12byte',
        'machineNum',
        'ADRange',
        'ADResolution',
        'xMaxScanRange',
        'yMaxScanRange',
        'xPiezoCoeff',
        'yPiezoCoeff',
        'zPiezoCoeff',
        'zDriveGain',
        'operatorName',
        'comment',
        'scalingFactor',
        'zOffset',
        'normalize'
    ]

    def __init__(self, filename: str, normalize: bool = True):
        self.filename = filename
        self.raw = open(filename, 'rb').read()
        self._read_header_()
        self.zOffset = -2048
        self.scalingFactor = 10 / 4096
        self.normalize = normalize

    def _read_header_(self):
        self.fileVersion = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.headSize = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.frameHeaderSize = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.encoding = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.operatorNameLength = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.commentSize = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.rawType1ch = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.rawType2ch = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.frameNum = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.currentFrameNum = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.scanDirection = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.asdFileName = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.xPixel = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.yPixel = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.xScanRange = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.yScanRange = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.averageFlag = struct.unpack('<c', self.raw[0:1])[0]
        self.raw = self.raw[1:]
        self.averageNum = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.year = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.month = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.day = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.hour = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.minute = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.second = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.xRoundDeg = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.yRoundDeg = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.frameAcquisTime = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.sensorSens = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.phaseSens = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.offset = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.booked12byte = struct.unpack('<iii', self.raw[0:12])
        self.raw = self.raw[12:]
        self.machineNum = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.ADRange = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.ADResolution = struct.unpack('<i', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.xMaxScanRange = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.yMaxScanRange = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.xPiezoCoeff = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.yPiezoCoeff = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.zPiezoCoeff = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.zDriveGain = struct.unpack('<f', self.raw[0:4])[0]
        self.raw = self.raw[4:]
        self.operatorName = struct.unpack(f'<{"c" * self.operatorNameLength}', self.raw[0:self.operatorNameLength])
        self.operatorName = ''.join([x.decode('ascii') for x in self.operatorName])
        self.raw = self.raw[self.operatorNameLength:]
        self.comment = struct.unpack(f'<{"c" * self.commentSize}', self.raw[0:self.commentSize])
        self.comment = ''.join([x.decode('ascii') for x in self.comment])
        self.raw = self.raw[self.commentSize:]

    def frame(self) -> [ASDFrame]:
        for _ in range(self.currentFrameNum):
            frame = ASDFrame(self.raw, self.xPixel, self.yPixel, self.zOffset, self.scalingFactor, self.normalize)
            yield frame
            self.raw = self.raw[len(frame):]

    def videos(self):
        pass

    def visualize(self, wait: int = 30) -> None:
        try:
            from cv2 import cv2
            for single in self.frame():
                frame = single.image
                frame = cv2.resize(frame, (self.xScanRange, self.yScanRange))
                frame -= np.min(frame)
                frame *= (255 / np.max(frame))
                frame = np.asarray(frame, dtype=np.uint8)
                cv2.imshow(self.filename, frame)
                cv2.waitKey(wait)
        except ModuleNotFoundError:
            raise "Please install opencv by `$pip install opencv-python`"

    def __repr__(self):
        return self.filename

    def creation_date(self) -> datetime.datetime:
        return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)

    def shape(self) -> (int, int, int):
        return self.currentFrameNum, self.yScanRange, self.xScanRange
