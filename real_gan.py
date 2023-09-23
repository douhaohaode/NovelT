import os
import cv2
from basicsr.archs.rrdbnet_arch import RRDBNet

from realesrgan import RealESRGANer

sam_checkpoint = "RealESRGAN_x4plus_anime_6B.pth"

model_path = os.path.join('models', sam_checkpoint)


def inference_gan(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    # if len(img.shape) == 3 and img.shape[2] == 4:
    #     #img_mode = 'RGBA'
    # else:
    #     #img_mode = None

    upsampler = RealESRGANer(
        scale=4,
        model_path=model_path,
        half=False,
        model=RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4),
    )

    output, _ = upsampler.enhance(img, outscale=4)

    cv2.imwrite(path, output)
    return path
