# Yolo Marker HSV

This project implements a GUI application using PyQt5 and OpenCV for processing images. The user inputs a `class_number`, uses an `hsv.cfg` configuration file for HSV thresholding, processes images in the `source` folder, saves results to text files, and displays processed images.

## Project Structure

```
project_directory/
│
├── source/
│   ├── example1.jpg
│   ├── example2.png
│   └── ...
│
├── hsv.cfg
├── yolo_marker.py
└── README.md
```

- `source/`: Folder containing the image files.
- `hsv.cfg`: Configuration file for HSV range settings.
- `yolo_marker.py`: Main script for image processing and GUI.
- `README.md`: Documentation for the project.

## Configuration File (hsv.cfg)

The `hsv.cfg` file defines the HSV color range settings. It should have the following format:

```
H Min: 0  # Minimum Hue value
H Max: 180  # Maximum Hue value
S Min: 0  # Minimum Saturation value
S Max: 255  # Maximum Saturation value
V Min: 0  # Minimum Value (Brightness) value
V Max: 255  # Maximum Value (Brightness) value
```

Example `hsv.cfg`:

```
H Min: 0 
H Max: 180
S Min: 0 
S Max: 255 
V Min: 0 
V Max: 255
```

## Installation
To run this project, you need to install the required Python packages. You can use `pip` to install the dependencies listed in the `requirements.txt` file. Also you can manually install the dependencies as follows:

### Using `requirements.txt`
```bash
$ pip install -r requirements.txt
```

### Without `requirements.txt`
```bash
$ pip install opencv-python
$ pip install numpy
$ pip install PyQt5
```

## Running the Application

1. Ensure the `hsv.cfg` file is properly configured.
2. Place image files in the `source` folder.
3. Run the `yolo_marker.py` script to start the application.

```bash
python yolo_marker.py
```

4. Enter the `class_number` in the GUI and click `Start` to begin processing.

## Contributing
Feel free to submit issues, feature requests, and pull requests to improve the package.

## License
This project is licensed under the MIT License - see the [LICENSE][LICENSE] file for details.

## Contact
For any questions or feedback, please contact [menggu1234@naver.com][email].

[LICENSE]: https://github.com/mjlee111/Yolo_marker_hsv/blob/master/LICENSE
[email]: mailto:menggu1234@naver.com
