import torch
import torchvision
from ultralytics import YOLO
import cv2 as cv
import os
import time
import supervision as sv
import numpy as np
from collections import defaultdict


# Object Detection Class for YOLO model and Camera
class HumanDetection:
    def __init__(self, capture_index):
        # self.labels = None
        self.capture_index = capture_index

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")
        self.model = self.load_model()

        self.CLASS_NAMES_DICT = self.model.model.names
        self.box_annotator = sv.BoxAnnotator(
            sv.ColorPalette.default(), thickness=3, text_thickness=3, text_scale=1.5
        )

    @staticmethod
    def load_model():
        model = YOLO("model.pt")
        model.fuse()

        return model

    def predict(self, frame):
        results = self.model(frame)

        return results

    def plot_bboxes(self, results, frame):
        xyxys = []
        confidences = []
        class_ids = []

        # Extract detections for person class
        for result in results:
            boxes = result.boxes.cpu().numpy()
            class_id = boxes.cls[0]
            conf = boxes.conf[0]
            xyxy = boxes.xyxy[0]

            if class_id == 0.0:
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))

        # Setup detections for visualization
        detections = sv.Detections(
            xyxy=results[0].boxes.xyxy.cpu().numpy(),
            confidence=results[0].boxes.conf.cpu().numpy(),
            class_id=results[0].boxes.cls.cpu().numpy().astype(int),
        )
        print(detections)
        # Format custom labels
        self.labels = [
            f"{self.CLASS_NAMES_DICT[class_id]} {confidence:0.2f}"
            for _, mask, confidence, class_id, tracker_id in detections
        ]

        # Annotate and display frame
        frame = self.box_annotator.annotate(
            scene=frame, detections=detections, labels=self.labels
        )

        return frame

    def __call__(self):
        cap = cv.VideoCapture(self.capture_index)
        assert cap.isOpened()

        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

        while True:
            startTime = time.time()
            ret, frame = cap.read()
            assert ret
            results = self.predict(frame)
            frame = self.plot_bboxes(results, frame)
            endTime = time.time()
            fps = 1 / np.round(endTime - startTime, 2)
            cv.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 70),
                cv.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                2,
            )

            cv.imshow("Human Detection", frame)

            if cv.waitKey(10) & 0xFF == ord("q"):
                break

        cap.release()
        cv.destroyAllWindows()


class Tracker():
    def __init__(self, capture_index):
        self.capture_index = capture_index

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")
        self.model = self.load_model()

        self.CLASS_NAMES_DICT = self.model.model.names
        self.box_annotator = sv.BoxAnnotator(
            sv.ColorPalette.default(), thickness=3, text_thickness=3, text_scale=1.5
        )

    def load_model(self):
        model = YOLO("model.pt")
        model.fuse()

        return model

    def __call__(self):
        cap = cv.VideoCapture(self.capture_index)
        assert cap.isOpened()

        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        track_history = defaultdict(lambda: [])
        while True:
            ret, frame = cap.read()
            assert ret
            results = self.model.track(frame, persist=True, tracker="bytetrack.yaml")

            boxes = results[0].boxes.xywh.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            annotated_frame = results[0].plot()
            for box, track_id in zip(boxes, track_ids):
                x, y, w, h = box
                track = track_history[track_id]
                track.append((float(x), float(y)))  # x, y center point
                if len(track) > 30:  # retain 90 tracks for 90 frames
                    track.pop(0)

                # Draw the tracking lines
                points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                cv.polylines(annotated_frame, [points], isClosed=False, color=(230, 230, 230), thickness=10)

            cv.imshow("tracker", annotated_frame)

            if cv.waitKey(10) & 0xff == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()

tracker = Tracker(capture_index=0)
tracker()