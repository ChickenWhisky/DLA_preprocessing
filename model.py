import layoutparser as lp
import cv2

# Load a pre-trained model (Detectron2)
model = lp.models.Detectron2LayoutModel(
    'lp://PubLayNet/mask_rcnn_X_101_32x8d_FPN_3x/config',
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

# Load an image using OpenCV
image_path = "img/double_0.png"
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(f"Failed to load image from path: {image_path}")

# Detect layout
layout = model.detect(image)

# Visualize the detected layout
lp.draw_box(image, layout, box_width=3).show()

