import numpy as np


def is_parent(class_hierarchy, class1, class2):
    # Check if class1 is the parent class of class2 based on the class hierarchy using NumPy
    # ...
    pass


def nms(bounding_boxes, confidence_score, classes, class_hierarchy, score_threshold, iou_threshold):
    # If no bounding boxes, return empty list
    if len(bounding_boxes) == 0:
        return [], []

    # Confidence scores of bounding boxes
    score = np.array(confidence_score)
    selected_idx = np.where(score > score_threshold)[0]
    score = score[selected_idx]
    classes = classes[selected_idx]
    # Bounding boxes
    boxes = np.array(bounding_boxes)
    boxes = boxes[selected_idx]

    # coordinates of bounding boxes
    start_x = boxes[:, 0]
    start_y = boxes[:, 1]
    end_x = boxes[:, 2]
    end_y = boxes[:, 3]

    # Picked bounding boxes
    picked_boxes = []
    picked_score = []

    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(score)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]
        class_index = classes[index]

        # Pick the bounding box with largest confidence score
        picked_boxes.append(bounding_boxes[index])
        picked_score.append(confidence_score[index])

        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        ratio = intersection / \
            (areas[index] + areas[order[:-1]] - intersection)
        above_idx_class = np.where(ratio > iou_threshold)

        # keep the box that class_index is parent
        keep_idx = []
        for idx in above_idx_class:
            if is_parent(class_hierarchy, class_index, classes[idx]):
                keep_idx.append(idx)

        left = np.where(ratio < iou_threshold)
        left = np.concatenate(left, np.array(keep_idx))

        for idx_left in order:
            if idx_left not in left:
                order = np.delete(order, idx_left, 0)

    return picked_boxes, picked_score
