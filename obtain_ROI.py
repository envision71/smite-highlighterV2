import os
import cv2 as cv
import numpy as np
import tensorflow as tf
import helper
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

CONFIG_PATH = r"workspace\tensorflow\models\my_ssd_mobnet\pipeline.config"
CHECKPOINT_PATH = r'workspace\tensorflow\models\my_ssd_mobnet/'
category_index = label_map_util.create_category_index_from_labelmap(r'workspace\label_map.pbtxt')

   
# Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-16')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections

def get_ROI_from_pictures(ImagePath):
    still = cv.imread(ImagePath, cv.IMREAD_UNCHANGED)
    dictBox = get_ROI(still)
    pass

def get_ROI(frame):

    #prepare frame for tensorflow
    image_np = np.array(frame)
    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    helper.detections = detections

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                    for key, value in detections.items()}

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()
    im_height, im_width, im_channels = frame.shape
    
    # viz_utils.visualize_boxes_and_labels_on_image_array(
    #             image_np_with_detections,
    #             detections['detection_boxes'],
    #             detections['detection_classes']+label_id_offset,
    #             detections['detection_scores'],
    #             category_index,
    #             use_normalized_coordinates=True,
    #             max_boxes_to_draw=5,
    #             min_score_thresh=.5,
    #             agnostic_mode=False)

    #prepare dict for storing bbox's
    boxes = detections['detection_boxes']
    scores = detections['detection_scores']
    classes = detections['detection_classes']

    #loop to fill in bbox info
    dictBox = helper.dictBox
    if scores is not None:
        for index,score in enumerate(scores):
            for label, boxInfo in dictBox.items():
                #print((classes[index].item()) == (int(label)))
                if (classes[index].item()) == (int(label)):
                #get the bbox with the highes score for each item
                    if score > boxInfo["score"]:
                        boxInfo["score"] = score
                        boxInfo["label"] = helper.get_Label(str(classes[index]))
                        ymin, xmin, ymax, xmax = tuple(boxes[index].tolist())
                        (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                    ymin * im_height, ymax * im_height)
                        boxInfo["box"] = int(left), int(right), int(top), int(bottom)
                                        # x1            x2          y1      y2
                        grayImage = cv.cvtColor(frame[int(top):int(bottom),int(left):int(right)], cv.COLOR_BGR2GRAY)
                        if boxInfo["label"] == "Kills":	
                            helper.compareImageDict.update({boxInfo["label"]:np.array(grayImage)})
                        if boxInfo["label"] == "loading":
                            helper.compareImageDict.update({boxInfo["label"]:np.array(grayImage)})
                        if boxInfo["label"] == "victory":
                            helper.compareImageDict.update({boxInfo["label"]:np.array(grayImage)})
                        if boxInfo["label"] == "defeat":
                            helper.compareImageDict.update({boxInfo["label"]:np.array(grayImage)})

    if not dictBox["0"]["box"]:
        return dictBox
    else:
        return dictBox

    
def main():
    while True:
        cap = cv.VideoCapture(r'workspace\videos\full vod_Trim6_Trim.mp4')
        frame = cv.imread(r'E:\python projects\obj detection v2\workspace\images\test\pc overlay 1.jpg')
        ret, frame = cap.read()

        cv.imshow('object detection3',  frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

if __name__ == "__main__":
    main()