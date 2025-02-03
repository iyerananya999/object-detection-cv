# import cv2
# import numpy as np

# # Load video
# cap = cv2.VideoCapture("ObjectTracking\highway_video.mp4")

# # Create background subtractor for motion detection
# fgbg = cv2.createBackgroundSubtractorMOG2()

# # Create MultiTracker
# tracker = cv2.legacy.MultiTracker_create()

# object_id = 0
# objects = {}

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Apply background subtraction
#     fgmask = fgbg.apply(frame)
    
#     # Find contours
#     contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     new_objects = []
#     for cnt in contours:
#         if cv2.contourArea(cnt) > 500:
#             x, y, w, h = cv2.boundingRect(cnt)
#             new_objects.append((x, y, w, h))
    
#     # Track existing objects
#     success, boxes = tracker.update(frame)
    
#     existing_boxes = [(int(b[0]), int(b[1]), int(b[2]), int(b[3])) for b in boxes]
    
#     # Add new objects if they don't overlap with existing ones
#     for obj in new_objects:
#         if not any(abs(obj[0] - e[0]) < 50 and abs(obj[1] - e[1]) < 50 for e in existing_boxes):
#             tracker.add(cv2.legacy.TrackerCSRT_create(), frame, obj)
#             objects[object_id] = obj
#             object_id += 1
    
#     # Draw bounding boxes and IDs
#     for i, newbox in enumerate(tracker.getObjects()):
#         x, y, w, h = [int(v) for v in newbox]
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.putText(frame, f"ID {i}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
#     # Display the results
#     cv2.imshow("Tracking", frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2

# Load video
cap = cv2.VideoCapture("ObjectTracking/highway_video.mp4")

# Create a background subtractor (detects moving objects)
fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video when it ends
        continue

    # Apply background subtraction
    fgmask = fgbg.apply(frame)

    # Find contours of moving objects
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) > 800:  # Filter out small objects
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw box
            cv2.putText(frame, "Car", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Car Detection", frame)  # Show video

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
