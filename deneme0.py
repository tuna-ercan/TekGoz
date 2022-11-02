import cv2
import mediapipe as mp
import tekgozl

mp_face_detection = mp.solutions.face_detection
tek_goz = tekgozl.TekGoz('/dev/ttyUSB0')

kP_X = 0.05
kP_Y = 0.05

cam_angle_x = 53
cam_angle_y = 43

safe_zone_x = 8 # Angle
safe_zone_y = 6 

def tek_goz_control_XY(x, y):
  angle_dif_x = x*cam_angle_x*kP_X #Getting the angle value ****** (*-1) ????
  angle_dif_y = y*cam_angle_y*kP_Y

  if(abs(angle_dif_x)>safe_zone_x and tek_goz.limits["T"][0] < (tek_goz.getT() + angle_dif_x) < tek_goz.limits["T"][1]):

    tek_goz.setT(tek_goz.getT() + angle_dif_x)
    tek_goz.send_command()

  if(abs(angle_dif_y)>safe_zone_y and tek_goz.limits["WP"][0] < (tek_goz.getWP() + angle_dif_x) < tek_goz.limits["WP"][1]):

    tek_goz.setWP(tek_goz.getWP() + angle_dif_y) 
    tek_goz.send_command()

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
      cv2.putText(image, str(int(noseX-width/2)), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
      cv2.putText(image, str(int(height/2-noseY)), (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)

      tek_goz_control_XY((noseX-width/2)/width, (height/2-noseY)/height)


    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
