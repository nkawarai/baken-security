from PIL import ImageChops
import numpy as np

class ImageUtil:
    @staticmethod
    def are_same_image(image1, image2):
        """引数に与えられた画像が同一であればTRUEを返す。"""
        if np.sum(np.array(ImageChops.difference(image1, image2).getdata())) == 0:
            return True
        return False
