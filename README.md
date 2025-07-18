# accident-detection-emergency-call
# Accident Detection and Emergency Call System

This project is designed to detect road accidents using camera input and immediately initiate an emergency alert or call. It combines real-time video processing with machine learning to identify accident scenarios and notify responders.

**Demo video **



https://github.com/user-attachments/assets/6180fcf1-6f5f-4a9d-8762-70529ad5004c


## 🚀 Features

- Real-time video analysis using OpenCV
- Accident detection using trained ML model
- Automatic emergency call/alert trigger
- Modular Python scripts: camera input, detection logic, and alert handling

## 🛠️ Technologies Used

- Python 3
- OpenCV
- TensorFlow/Keras
- NumPy
- JSON (for model structure)

## 📁 Folder Structure

```
accident-detection-emergency-call/
├── camera.py                 # Handles video input from webcam or camera
├── detection.py             # Contains the accident detection logic
├── main.py                  # Main entry point for the system
├── model.json               # Saved model architecture
├── train.py                 # Script to train the model
├── Road-Accident-Detection-Alert-System-main/ (possibly older version or ref)
└── README.md
```

## 🔧 How to Run the Project

1. **Install dependencies:**

   ```bash
   pip install opencv-python tensorflow numpy
   ```

2. **Run the main script:**

   ```bash
   python main.py
   ```

3. **To train the model (optional):**

   ```bash
   python train.py
   ```

## 📞 Emergency Alert Logic

- On detecting an accident, the system can trigger an alert function (email/SMS/call) using a service like Twilio or integrated GSM module.

## 📌 Notes
- Ensure camera access is allowed.
- Use real-world footage carefully and responsibly during testing.

---

**Developed by:** *Thejas B J*\
*Project for academic/experimental use.
