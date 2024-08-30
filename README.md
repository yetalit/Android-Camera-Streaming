# Android Camera Streaming
 Stream camera feed of Android device via UDP using Java and Python.


https://github.com/user-attachments/assets/6e81f750-138e-4c2f-998b-0df393676396


## Dependencies
1. Numpy
2. Pillow 
3. OpenCV

## Usage
`src` folder contains the necessary files for Java Android app and a single Python script (server.py) for receiving camera frames.

Including these lines to your `AndroidManifest.xml` may be useful:
```xml
<uses-permission android:name="android.permission.INTERNET"/>
<uses-permission android:name="android.permission.CAMERA"/>
<uses-feature android:name="android.hardware.camera" android:required="true"/>
```
 
As frames are rendered using OpenCV, further image processing operations can also be done.
