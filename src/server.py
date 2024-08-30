import cv2
import numpy as np
import socket
import io
from PIL import Image

# Setup the UDP
C_IP = '192.168.1.1'
C_PORT = 46463
S_PORT = 46464
chunkSize = 1018
# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('', S_PORT))
for _ in range(5):
    udp_socket.sendto(b'', (C_IP, C_PORT))

data = bytearray()
pIndex = -1
cIndex = -1
receivedBytes = 0
print("UDP: Server is about to wait to receive...")
while True:
    try:
        buffer = bytearray(chunkSize + 6)  # Buffer to store incoming packet data
        packet, _ = udp_socket.recvfrom_into(buffer)
        globalIndex = int.from_bytes(buffer[0:1], "big")
        if globalIndex == pIndex:
            continue
        if globalIndex != cIndex:
            data.clear()
            pIndex = cIndex
            cIndex = globalIndex
            receivedBytes = 0
            size = int.from_bytes(buffer[3:6], "big")
            data = bytearray(size)

        data[int.from_bytes(buffer[1:3], "big") * chunkSize: (int.from_bytes(buffer[1:3],
                                                                             "big") * chunkSize) + packet - 6] = buffer[
                                                                                                                 6:packet]
        receivedBytes += packet - 6
        # Check if end of image data is reached
        if receivedBytes == len(data):
            # End of image data reached
            print("Received complete data: " + str(receivedBytes) + " bytes")
            cameraFacing = int.from_bytes(data[0:1], "big")
            data[:1] = b''
            try:
                # Read the image data into a PIL Image
                image = Image.open(io.BytesIO(data))

                # Check if the image was successfully loaded
                if image:
                    # Convert PIL Image to OpenCV Mat
                    open_cv_image = np.array(image)
                    # Convert RGB to BGR
                    img = open_cv_image[:, :, ::-1].copy()

                    # Apply necessary transformations
                    if cameraFacing == 0:
                        img = cv2.flip(img, 1)
                    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
                    # Display the image using OpenCV
                    cv2.imshow("Stream", img)
                    if cv2.waitKey(1) == 27:  # If 'Esc' is entered break the loop
                        break
                else:
                    print("Failed to read the image")
            except Exception as e:
                print("Error:", e)
    except Exception as e:
        print("Error:", e)

# Release the resources
udp_socket.close()
cv2.destroyAllWindows()
