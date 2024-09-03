import sys
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Image Processor')
        
        layout = QVBoxLayout()
        
        self.class_number_input = QLineEdit(self)
        self.class_number_input.setPlaceholderText('Enter class number')
        layout.addWidget(self.class_number_input)
        
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_processing)
        layout.addWidget(self.start_button)
        
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)
        
        self.setLayout(layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_next_image)
        self.current_image_index = 0
        self.image_files = []
        self.config = {}
        self.class_number = None
        
    def read_cfg(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        config = {}
        for line in lines:
            key, value = line.strip().split(': ')
            config[key] = tuple(map(int, value.split()))
        return config

    def start_processing(self):
        self.class_number = self.class_number_input.text()
        if not self.class_number.isdigit():
            print('Invalid class number')
            return
        
        self.class_number = int(self.class_number)
        self.config = self.read_cfg('hsv.cfg')
        
        self.image_files = [f for f in os.listdir('source') if f.endswith(('.png', '.jpg', '.jpeg'))]
        if not self.image_files:
            print('No images found in source folder')
            return
        
        self.current_image_index = 0
        print('Processing started')
    
    def process_next_image(self):
        if self.current_image_index >= len(self.image_files):
            self.timer.stop()
            print('Processing complete')
            return
        
        file = self.image_files[self.current_image_index]
        self.current_image_index += 1
        
        image_path = os.path.join('source', file)
        img = cv2.imread(image_path)
        
        if img is None:
            print(f'Error reading image {image_path}')
            return
        
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        min_hsv = np.array([self.config['H Min'], self.config['S Min'], self.config['V Min']])
        max_hsv = np.array([self.config['H Max'], self.config['S Max'], self.config['V Max']])
        mask = cv2.inRange(hsv_img, min_hsv, max_hsv)
        result = cv2.bitwise_and(img, img, mask=mask)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            img_height, img_width = img.shape[:2]
            x_center = (x + w / 2) / img_width
            y_center = (y + h / 2) / img_height
            w_normalized = w / img_width
            h_normalized = h / img_height
            
            with open(os.path.join('source', file.split('.')[0] + '.txt'), 'w') as f:
                f.write(f"{self.class_number} {x_center} {y_center} {w_normalized} {h_normalized}\n")
        
        img_bgr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        
        h, w, ch = img_bgr.shape
        result_img = np.hstack((img_bgr, result_rgb))
        
        q_img = QImage(result_img.data, w * 2, h, w * 2 * ch, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        print(f'Processed {file}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
