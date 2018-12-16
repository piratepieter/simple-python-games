import cv2
import time

# Load the face classifier.
cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

# Load pirate hat.
img_hat = cv2.imread('hat.png', -1)
scale = 0.1
img_hat = cv2.resize(img_hat, (0, 0), fx=scale, fy=scale)
mask_hat = img_hat[:, :, 3] / 255.0

# Load pirate patch.
img_patch = cv2.imread('patch.png', -1)
scale = 0.07
img_patch = cv2.resize(img_patch, (0, 0), fx=scale, fy=scale)
mask_patch = img_patch[:, :, 3] / 255.0

# Open the video stream.
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = cv2.flip(frame, 1)

    # Look for faces.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw pirate attributes on each face.
    for (x, y, w, h) in faces:
        try:
            # The patch
            x_offset = x + 40
            y_offset = y - 20
            y_range = slice(y_offset, y_offset + img_patch.shape[0])
            x_range = slice(x_offset, x_offset + img_patch.shape[1])
            for c in range(0, 3):
                frame[y_range, x_range, c] = (
                    img_patch[:, :, c] * mask_patch[:, :] +
                    frame[y_range, x_range, c] * (1.0 - mask_patch[:, :])
                )

            # The hat.
            x_offset = x - 90
            y_offset = y - 80
            y_range = slice(y_offset, y_offset + img_hat.shape[0])
            x_range = slice(x_offset, x_offset + img_hat.shape[1])
            for c in range(0, 3):
                frame[y_range, x_range, c] = (
                    img_hat[:, :, c] * mask_hat[:, :] +
                    frame[y_range, x_range, c] * (1.0 - mask_hat[:, :])
                )
        except:
            pass

    # Display the resulting frame.
    cv2.imshow('Video', frame)

    # Define keys to save and quit.
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('pirate %s.png' % time.ctime(), frame)

    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
