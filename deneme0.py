import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()
    (height, width) = image.shape[:2]
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    # Draw the face detection annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      width = cap.get(3)  # float `width`
      height = cap.get(4)  # float `height`

      #boundingBox = results.detections[0].location_data.relative_bounding_box
      #cv2.circle(image, (int((boundingBox.xmin + boundingBox.width/2)*width),int((boundingBox.ymin + boundingBox.height/2)*height)), 30, (0, 0, 255), -1)
      nose = mp_face_detection.get_key_point(results.detections[0], mp_face_detection.FaceKeyPoint.NOSE_TIP)
      noseX = int(nose.x*width)
      noseY = int(nose.y*height)
      cv2.circle(image, (noseX, noseY), 15, (0, 0, 255), -1)
      cv2.circle(image, (int(width/5), int(height/2)), 5, (255,0,0), -1)
      cv2.circle(image, (int(4*width/5), int(height/2)), 5, (255,0,0), -1)
      cv2.putText(image, str(int(width/2-noseX)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
