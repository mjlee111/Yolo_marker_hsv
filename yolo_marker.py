import sys
import cv2
import numpy as np
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Image Processor')
        
        # Layout
        layout = QVBoxLayout()
        
        # Class Number Input
        self.class_number_input = QLineEdit(self)
        self.class_number_input.setPlaceholderText('Enter class number')
        layout.addWidget(self.class_number_input)
        
        # Start Button
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.process_images)
        layout.addWidget(self.start_button)
        
        # Image Display
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)
        
        self.setLayout(layout)
        
    def read_cfg(self, filepath):
        with open(filepath, 'r') as file:
            lines = file.readlines()
        config = {}
        for line in lines:
            key, value = line.strip().split(': ')
            config[key] = tuple(map(int, value.split()))
        return config

    def process_images(self):
        class_number = self.class_number_input.text()
        if not class_number.isdigit():
            print('Invalid class number')
            return
        
        class_number = int(class_number)
        config = self.read_cfg('hsv.cfg')
        
        min_hsv = np.array([config['H Min'], config['S Min'], config['V Min']])
        max_hsv = np.array([config['H Max'], config['S Max'], config['V Max']])
        
        source_folder = 'source'
        files = [f for f in os.listdir(source_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        for file in files:
            image_path = os.path.join(source_folder, file)
            img = cv2.imread(image_path)
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
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
                
                with open(os.path.join(source_folder, file.split('.')[0] + '.txt'), 'w') as f:
                    f.write(f"{class_number} {x_center} {y_center} {w_normalized} {h_normalized}\n")
                
            # Display Images
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            
            h, w, ch = img_bgr.shape
            result_img = np.hstack((img_bgr, result_rgb))
            
            q_img = QImage(result_img.data, w * 2, h, w * 2 * ch, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
