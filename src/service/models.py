from PIL import Image
import requests
from io import BytesIO
import numpy as np
import cv2
import torch

import src.ai.session.clothes as clothes_session


def load_image(img_url: str, transformation):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")

    tensor = transformation(img)
    tensor = np.array(tensor)
    tensor = np.expand_dims(tensor, axis=0)
    tensor = torch.Tensor(tensor)
    return tensor, img


def cls_model_postprocess(output, labels):
    probabilities = output[0]
    predicted_class_id = np.argmax(probabilities)
    confidence = probabilities[predicted_class_id]
    top1_class_name, top1_score = labels[predicted_class_id], confidence.item()
    return {
        "top1ClassName": top1_class_name,
        "top1Score": top1_score,
    }


def detection_model_postprocess(output, input_shape, img_shape, labels):
    confidence_thres = 0.25
    iou_thres = 0.5

    # Transpose and squeeze the output to match the expected shape
    outputs = np.transpose(np.squeeze(output[0]))

    # Get the number of rows in the outputs array
    rows = outputs.shape[0]

    # Lists to store the bounding boxes, scores, and class IDs of the detections
    boxes = []
    scores = []
    class_ids = []

    # Calculate the scaling factors for the bounding box coordinates
    img_width, img_height = img_shape
    input_width, input_height = input_shape

    x_factor = img_width / input_width
    y_factor = img_height / input_height

    # Iterate over each row in the outputs array
    for i in range(rows):
        # Extract the class scores from the current row
        classes_scores = outputs[i][4:]

        # Find the maximum score among the class scores
        max_score = classes_scores[np.argmax(classes_scores)]

        # If the maximum score is above the confidence threshold
        if max_score >= confidence_thres:
            # Get the class ID with the highest score
            class_id = np.argmax(classes_scores)

            # Extract the bounding box coordinates from the current row
            x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]

            # Calculate the scaled coordinates of the bounding box
            left = int((x - w / 2) * x_factor)
            top = int((y - h / 2) * y_factor)
            width = int(w * x_factor)
            height = int(h * y_factor)

            # Add the class ID, score, and box coordinates to the respective lists
            class_ids.append(class_id.item())
            scores.append(max_score.item())
            boxes.append([left, top, width, height])

    # Apply non-maximum suppression to filter out overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, scores, confidence_thres, iou_thres)

    # Iterate over the selected indices after non-maximum suppression
    result = {'scores': [], "class_names": []}
    for i in indices:
        # Get the box, score, and class ID corresponding to the index
        box = boxes[i]
        score = scores[i]
        class_id = class_ids[i]
        result['scores'].append(score)
        result['class_names'].append(labels[class_id])

        # Draw the detection on the input image
        # self.draw_detections(input_image, box, score, class_id)

    # Return the modified input image
    if (len(result["scores"]) == 0):
        return {"top1ClassName": None, "top1Score": None}

    top1_idx = np.argmax(result['scores'])
    top1_className = result['class_names'][top1_idx]
    top1_score = result['scores'][top1_idx]

    return {"top1ClassName": top1_className, "top1Score": top1_score}

def clothes_equipment(url: str):
    tensor, img = load_image(url, clothes_session.transformation)

    input_shape = list(clothes_session.input_shape)
    img_shape = list(img.size)

    output = clothes_session.session(tensor)
    return detection_model_postprocess(output, input_shape, img_shape, clothes_session.labels)
