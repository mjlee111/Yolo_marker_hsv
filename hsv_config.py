import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QSize

class HSVThresholdingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('HSV Thresholding App')
        self.setGeometry(100, 100, 1080, 720)

        self.image = None
        self.hsv_image = None

        self.initUI()

    def initUI(self):
        # Create a layout for the whole window
        main_layout = QVBoxLayout()

        # Create a horizontal layout for the images
        image_layout = QHBoxLayout()

        # Create QLabel widgets for displaying images
        self.original_label = QLabel()
        self.binary_label = QLabel()

        # Add labels to the horizontal layout
        image_layout.addWidget(self.original_label)
        image_layout.addWidget(self.binary_label)

        # Add horizontal layout to the main layout
        main_layout.addLayout(image_layout)

        # Create a layout for sliders
        sliders_layout = QVBoxLayout()

        # Create sliders and labels
        self.h_min_label = QLabel('H Min:')
        self.h_min_slider = self.create_slider(0, 255, self.update_image_processing, 0)
        self.h_max_label = QLabel('H Max:')
        self.h_max_slider = self.create_slider(0, 255, self.update_image_processing, 255)
        self.s_min_label = QLabel('S Min:')
        self.s_min_slider = self.create_slider(0, 255, self.update_image_processing, 0)
        self.s_max_label = QLabel('S Max:')
        self.s_max_slider = self.create_slider(0, 255, self.update_image_processing, 255)
        self.v_min_label = QLabel('V Min:')
        self.v_min_slider = self.create_slider(0, 255, self.update_image_processing, 0)
        self.v_max_label = QLabel('V Max:')
        self.v_max_slider = self.create_slider(0, 255, self.update_image_processing, 255)

        # Add sliders and labels to the sliders layout
        sliders_layout.addWidget(self.h_min_label)
        sliders_layout.addWidget(self.h_min_slider)
        sliders_layout.addWidget(self.h_max_label)
        sliders_layout.addWidget(self.h_max_slider)
        sliders_layout.addWidget(self.s_min_label)
        sliders_layout.addWidget(self.s_min_slider)
        sliders_layout.addWidget(self.s_max_label)
        sliders_layout.addWidget(self.s_max_slider)
        sliders_layout.addWidget(self.v_min_label)
        sliders_layout.addWidget(self.v_min_slider)
        sliders_layout.addWidget(self.v_max_label)
        sliders_layout.addWidget(self.v_max_slider)

        # Create control buttons
        self.load_image_button = QPushButton('Load Image')
        self.load_image_button.clicked.connect(self.load_image)

        self.save_button = QPushButton('Save HSV Config')
        self.save_button.clicked.connect(self.save_hsv_config)

        # Add control buttons and sliders to the main layout
        main_layout.addWidget(self.load_image_button)
        main_layout.addLayout(sliders_layout)
        main_layout.addWidget(self.save_button)

        # Create a container widget and set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_slider(self, min_val, max_val, callback, val):
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(val)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.valueChanged.connect(callback)
        return slider

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is None:
                raise FileNotFoundError(f"The image file '{file_path}' could not be loaded.")
            self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            self.update_image(self.image, self.original_label)
            self.update_image_processing()

    def update_image(self, image, label):
        if image is None:
            return

        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image to fit within window size of 540x720 for each image
        max_width = 540
        max_height = 720
        height, width, _ = image_rgb.shape
        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        resized_image_rgb = cv2.resize(image_rgb, (new_width, new_height))
        
        # Convert to QImage
        q_image = QImage(resized_image_rgb.data, new_width, new_height, 3 * new_width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap)
        
        # Update size to fit the new image size
        label.setFixedSize(QSize(new_width, new_height))

    def update_image_processing(self):
        if self.image is None:
            return

        h_min = self.h_min_slider.value()
        h_max = self.h_max_slider.value()
        s_min = self.s_min_slider.value()
        s_max = self.s_max_slider.value()
        v_min = self.v_min_slider.value()
        v_max = self.v_max_slider.value()

        hsv_min = np.array([h_min, s_min, v_min])
        hsv_max = np.array([h_max, s_max, v_max])

        mask = cv2.inRange(self.hsv_image, hsv_min, hsv_max)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output_image = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Create a 3-channel image for display

        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(output_image, (x, y), (x+w, y+h), (0, 255, 0), 2)

            with open('bounding_boxes.txt', 'w') as f:
                f.write(f'{x}, {y}, {w}, {h}\n')

        self.update_image(output_image, self.binary_label)

    def save_hsv_config(self):
        if self.image is None:
            return

        h_min = self.h_min_slider.value()
        h_max = self.h_max_slider.value()
        s_min = self.s_min_slider.value()
        s_max = self.s_max_slider.value()
        v_min = self.v_min_slider.value()
        v_max = self.v_max_slider.value()

        config = f'H Min: {h_min}\nH Max: {h_max}\nS Min: {s_min}\nS Max: {s_max}\nV Min: {v_min}\nV Max: {v_max}\n'
        with open('hsv.cfg', 'w') as f:
            f.write(config)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image(self.image, self.original_label)
        self.update_image_processing()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HSVThresholdingApp()
    window.show()
    sys.exit(app.exec_())
