import numpy as np
import time
import cv2
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class findFaceGetPulse(object):

    def __init__(self, bpm_limits=[], data_spike_limit=250,
                 face_detector_smoothness=10):

        self.frame_in = np.zeros((10, 10))
        self.frame_out = np.zeros((10, 10))
        self.fps = 0
        self.buffer_size = 250
        self.data_buffer = []
        self.times = []
        self.ttimes = []
        self.samples = []
        self.freqs = []
        self.fft = []
        self.slices = [[0]]
        self.t0 = time.time()
        self.bpms = []
        self.bpm = 0
        dpath = resource_path("haarcascade_frontalface_default.xml")
        if not os.path.exists(dpath):
            print("Cascade file not present!")
        self.face_cascade = cv2.CascadeClassifier(dpath)

        self.face_rect = [235, 187, 224, 224]
        self.last_center = np.array([0, 0])
        self.last_wh = np.array([0, 0])
        self.output_dim = 13
        self.trained = False

        self.idx = 1
        self.find_faces = True

    def find_faces_toggle(self):
        self.find_faces = not self.find_faces
        return self.find_faces

    def get_faces(self):
        return

    def shift(self, detected):
        x, y, w, h = detected
        center = np.array([x + 0.5 * w, y + 0.5 * h])
        shift = np.linalg.norm(center - self.last_center)

        self.last_center = center
        return shift

    def draw_rect(self, rect, col=(0, 255, 0)):
        x, y, w, h = rect
        cv2.rectangle(self.frame_out, (x, y), (x + w, y + h), col, 1)

    def get_subface_coord(self, fh_x, fh_y, fh_w, fh_h):
        x, y, w, h = self.face_rect
        return [int(x + w * fh_x - (w * fh_w / 2.0)),
                int(y + h * fh_y - (h * fh_h / 2.0)),
                int(w * fh_w),
                int(h * fh_h)]

    def get_subface_means(self, coord):
        x, y, w, h = coord
        subframe = self.frame_in[y:y + h, x:x + w, :]
        v1 = np.mean(subframe[:, :, 0])
        v2 = np.mean(subframe[:, :, 1])
        v3 = np.mean(subframe[:, :, 2])
#        print(int((v1+v2+v3)/3))

        return (v1 + v2 + v3) / 3.

    def train(self):
        self.trained = not self.trained
        return self.trained

    def track(self):
        detected = list(self.face_cascade.detectMultiScale(self.gray,
                                                           scaleFactor=1.3,
                                                           minNeighbors=4,
                                                           minSize=(50, 50),
                                                           flags=cv2.CASCADE_SCALE_IMAGE))

        if len(detected) > 0:
            detected.sort(key=lambda a: a[-1] * a[-2])
#            self.face_rect = detected[-1]

            if self.shift(detected[-1]) > 10:
                self.face_rect = detected[-1]

    def run(self, cam):
        self.times.append(time.time() - self.t0)
        self.frame_out = self.frame_in
        self.gray = cv2.equalizeHist(cv2.cvtColor(self.frame_in,
                                                  cv2.COLOR_BGR2GRAY))

        col = (255, 255, 255)
        self.find_faces = False
        if self.find_faces:
#            self.track()
            forehead1 = self.get_subface_coord(0.5, 0.15, 0.25, 0.15)
        else:
#            self.track()
            forehead1 = self.get_subface_coord(0.5, 0.15, 0.25, 0.15)
            vals = self.get_subface_means(forehead1)

            self.data_buffer.append(vals)
            L = len(self.data_buffer)
            if L > self.buffer_size:
                self.data_buffer = self.data_buffer[-self.buffer_size:]
                self.times = self.times[-self.buffer_size:]
                L = self.buffer_size

            processed = np.array(self.data_buffer)
            self.samples = processed
            if L >= self.buffer_size:
                self.output_dim = processed.shape[0] # возвращает длину строки

                self.fps = float(L) / (self.times[-1] - self.times[0])
                even_times = np.linspace(self.times[0], self.times[-1], L) # возвращает последовательность равномерно расставленных временных меток
#                interpolated = np.interp(even_times, self.times, processed)
                interpolated = processed
                interpolated = np.hamming(L) * interpolated # поэлементное умножение
                interpolated = interpolated - np.mean(interpolated) # вычитаем среднее (делаем вокруг нуля), получаем статический временной ряд
                raw = np.fft.rfft(interpolated) # преобразование фурье
                phase = np.angle(raw) # вычисляем фазу
                self.fft = np.abs(raw)
                self.freqs = float(self.fps) / L * np.arange(L / 2 + 1)

                freqs = 60. * self.freqs
                idx = np.where((freqs > 50) & (freqs < 180))

                pruned = self.fft[idx]
                phase = phase[idx]

                pfreq = freqs[idx]
                self.freqs = pfreq
                self.fft = pruned
                idx2 = np.argmax(pruned)

                self.bpm = self.freqs[idx2]
                self.idx += 1

            file = open("C://USERS/USER/desktop/01-02.txt", "a")
            file.write(str(int(self.bpm))+"\n")
            file.close()
