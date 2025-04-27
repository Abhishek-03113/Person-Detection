# Person Detection

A robust human detection system capable of detecting and tracking humans in real time.

## 🚀 About the Project

This project implements a real-time human detection and tracking system using computer vision techniques.  
It is built with Python and Flask for the web interface, and uses popular libraries like OpenCV and TensorFlow for the detection pipeline.

## 📁 Project Structure

```bash
.
├── Notebooks/         # Jupyter notebooks for experiments
├── instance/          # Instance files for Flask
├── static/            # Static assets (CSS, JS)
├── templates/         # HTML templates for Flask
├── HumanDetection.py  # Core detection and tracking logic
├── app.py             # Flask application
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## 🛠️ Technologies Used

- Python
- Flask
- OpenCV
- TensorFlow
- HTML/CSS (for frontend)

## 📦 Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Abhishek-03113/Person-Detection.git
    cd Person-Detection
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    ```bash
    python app.py
    ```

5. Open your browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## 📸 Features

- Real-time human detection using pre-trained models.
- Web interface to stream and view detections.
- Robust tracking even under slight occlusions.

## ✨ Future Improvements

- Improve detection accuracy with more advanced models (e.g., YOLOv8).
- Deploy using Docker for easier production use.
- Add support for multiple object categories.

## 🤝 Contributing

Contributions are welcome!  
Please open an issue first to discuss what you would like to change.

## 📄 License

This project is open-source under the MIT License.
