import sys
import glob
import os
import random
from itertools import cycle  # Import cycle from itertools
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QScreen
from PyQt5.QtCore import QTimer, Qt

class PictureViewerApp(QMainWindow):
    def __init__(self, image_folder):
        super().__init__()
        self.image_folder = image_folder
        self.setWindowTitle("Random Picture Viewer")
        
        # Get the screen size
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()  # This gives us the available geometry, taking into account taskbars and other desktop items.
        width = rect.width()
        height = rect.height()

        # Use the screen size to set the window size (with some margins)
        window_width = width * 0.8  # 80% of the screen width
        window_height = height * 0.8  # 80% of the screen height
        self.setGeometry((width - window_width) / 2, (height - window_height) / 2, window_width, window_height)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.load_images(self.image_folder)
        self.show_next_image()

        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_image)
        self.timer.start(150000)  # Milliseconds

    def load_images(self, image_folder):
        self.image_paths = glob.glob(os.path.join(image_folder, '*'))
        random.shuffle(self.image_paths)
        self.image_paths_cycle = cycle(self.image_paths)
        self.history = []
        if not self.image_paths:
            self.display_no_images_found()

    def show_next_image(self):
        if self.image_paths:
            image_path = next(self.image_paths_cycle)
            self.history.append(image_path)
            self.display_image(image_path)

    def show_previous_image(self):
        if self.history:
            self.history.pop()  # Remove the current image
            if self.history:
                previous_image_path = self.history.pop()  # Get the previous image
                self.display_image(previous_image_path)

    def display_no_images_found(self):
        self.image_label.setText("No images found in the specified folder.")

    def display_image(self, image_path):
        try:
            image = QImage(image_path)
            pixmap = QPixmap.fromImage(image)
            
            # Set a maximum size for images to be scaled to,
            # preserving their aspect ratio.
            max_pixmap_width = self.width() * 0.95
            max_pixmap_height = self.height() * 0.95
            
            # Scale the pixmap to the new size.
            scaled_pixmap = pixmap.scaled(max_pixmap_width, max_pixmap_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)  # Center the image in the label
        except Exception as e:
            print(f"Failed to load image: {e}")
            self.timer.singleShot(2000, self.show_next_image)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.show_previous_image()
        elif event.key() == Qt.Key_Right:
            self.show_next_image()

# This is the part where we actually start the application
def main():
    app = QApplication(sys.argv)
    image_folder = '/home/pefbrute/.config/autokey/data/My Phrases/Скрипты и прочее/Хранилище'  # Replace with your image folder path
    viewer = PictureViewerApp(image_folder)
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
