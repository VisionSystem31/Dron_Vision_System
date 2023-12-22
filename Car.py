import cv2
from ultralytics import YOLO


def main():
    model = YOLO("Model_Traffic_M01.pt")

    cap = cv2.VideoCapture("DJI_0956.MP4")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
        
    Start_Line_X1 = 650
    Start_Line_Y1 = 0
    Start_Line_X2 = 160

    End_Line_X1 = 1270
    End_Line_Y1 = 0
    End_Line_X2 = 1720

    classes = model.names
    print(classes)
    while True:
        ret, frame = cap.read()        
        
        if not ret:
            continue

        height, width, _ = frame.shape
        End_Line_Y2 = height
        Start_Line_Y2 = height
        results = model.track(frame, verbose=True, agnostic_nms=True, persist=True, conf=0.02, imgsz=640)

        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
            ids = results[0].boxes.id.cpu().numpy().astype(int)
            confidences = results[0].boxes.conf.cpu().numpy()
            
            for box, id, class_id, confidence in zip(boxes, ids, class_ids, confidences):
                x1, y1, x2, y2 = box

                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                inside_start = (center_y- Start_Line_Y1) * (Start_Line_X2 - Start_Line_X1) - (center_x- Start_Line_X1) * (Start_Line_Y2 - Start_Line_Y1) < 0
                inside_end = (center_y- End_Line_Y1) * (End_Line_X2 - End_Line_X1) - (center_x- End_Line_X1) * (End_Line_Y2 - End_Line_Y1) > 0

                if inside_start and inside_end:
                    if class_id == 2:   #Car
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)
                        cv2.putText(frame, f"ID #{id} {str(classes[class_id])} {confidence:.2f}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 255), -1)

                    if class_id == 0 or class_id == 3:   #motorcycle
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
                        cv2.putText(frame, f"ID #{id} {str(classes[3])} {confidence:.2f}", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                center_x = 0
                center_y = 0
        
        cv2.line(frame, (Start_Line_X1, Start_Line_Y1), (Start_Line_X2, Start_Line_Y2), (0, 255, 255), 3)
        cv2.line(frame, (End_Line_X1, End_Line_Y1), (End_Line_X2, End_Line_Y2), (0, 255, 255), 3)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__=="__main__":
    main()