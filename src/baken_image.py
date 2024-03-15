from PIL import Image
from image_util import ImageUtil

class BakenImage:
    TRIM_MARGIN = 4
    MASK_RIGHT_IMG_POSX = 929
    MASK_RIGHT_IMG_POSY = 338

    NAGSHI_BAKEN_MARK_IMG_PATH = "./resource/nagashi_604_20_1284_120.png"
    BOX_BAKEN_MARK_IMG_PATH = "./resource/box_604_20_1284_120.png"
    FORMATION_BAKEN_MARK_IMG_PATH = "./resource/formation_604_20_1284_120.png"
    JRA_LOGO_IMG_PATH = "./resource/jralogo_20_750_160_810.png"
    TANSHO_BAKEN_MARK_IMG_PATH = "./resource/tansho_380_5_590_740.png"
    FUKUSHO_BAKEN_MARK_IMG_PATH = "./resource/fukusho_380_5_590_740.png"
    MASK_LOWER_IMG_PATH = "./resource/mask.png"
    MASK_RIGHT_IMG_PATH = "./resource/mask2.png"

    def __init__(self, file_path):
        """コンストラクタ"""
        self.image = Image.open(file_path)
    
    def trim_unnesessary_parts(self):
        """不要な領域をトリミングする"""
        image = self.image
        # 画像の幅と高さを取得
        width, height = image.size
        # 画像をRGBモードに変換（必要に応じて）
        image = image.convert("RGB")

        left = 9999
        right = 0
        top = 9999
        bottom = 0

        # left(左上x座標)
        for x in range(width):
            # ピクセルのRGB値を取得
            r, g, b = image.getpixel((x, height / 2))
            if (r, g, b) != (255, 255, 255):
                left = x
                break

        #right(右上x座標)
        for x in range(width - 1, 0, -1):
            # ピクセルのRGB値を取得
            r, g, b = image.getpixel((x, height / 2))
            if (r, g, b) != (255, 255, 255):
                right = x
                break

        # top(左上y座標)
        for y in range(height):
            # ピクセルのRGB値を取得
            r, g, b = image.getpixel((width / 2, y))
            if (r, g, b) != (255, 255, 255):
                top = y
                break

        # bottom
        for y in range(height - 1, 0, -1):
            # ピクセルのRGB値を取得
            r, g, b = image.getpixel((width / 2, y))
            if (r, g, b) != (255, 255, 255):
                bottom = y
                break
        
        self.image = self.image.crop((left + self.TRIM_MARGIN, top + self.TRIM_MARGIN, right - self.TRIM_MARGIN, bottom - self.TRIM_MARGIN))

    def mask_lower_betting_price(self):
        """下部の金額をマスクする"""
        mask_image = Image.open(self.MASK_LOWER_IMG_PATH)
        self.image.paste(mask_image, (self.image.width - mask_image.width, self.image.height - mask_image.height))

    def mask_right_betting_price(self, isTanpuku = False):
        """右部の金額をマスクする"""
        if isTanpuku:
            mask_image = Image.open(self.MASK_RIGHT_IMG_PATH)
            self.image.paste(mask_image, (self.MASK_RIGHT_IMG_POSX, self.MASK_RIGHT_IMG_POSY + 50))
        else:
            mask_image = Image.open(self.MASK_RIGHT_IMG_PATH)
            self.image.paste(mask_image, (self.MASK_RIGHT_IMG_POSX, self.MASK_RIGHT_IMG_POSY))

    def is_jra_baken_image(self):
        """JRA馬券画像ならTRUEを返す"""
        jralogo_img = Image.open(self.JRA_LOGO_IMG_PATH)
        cropped_img = self.image.crop((20, 750, 160, 810))
        return ImageUtil.are_same_image(jralogo_img, cropped_img)

    def is_nagashi_baken(self):
        """流し馬券ならTRUEを返す"""
        nagashi_img = Image.open(self.NAGSHI_BAKEN_MARK_IMG_PATH)
        cropped_img = self.image.crop((604, 20, 1284, 120))
        return ImageUtil.are_same_image(nagashi_img, cropped_img)

    def is_formation_baken(self):
        """フォーメーション馬券ならTRUEを返す"""        
        formation_img = Image.open(self.FORMATION_BAKEN_MARK_IMG_PATH)
        cropped_img = self.image.crop((604, 20, 1284, 120))
        return ImageUtil.are_same_image(formation_img, cropped_img)

    def is_box_baken(self):
        """ボックス馬券ならTRUEを返す"""
        box_img = Image.open(self.BOX_BAKEN_MARK_IMG_PATH)
        cropped_img = self.image.crop((604, 20, 1284, 120))
        return ImageUtil.are_same_image(box_img, cropped_img)
    
    def is_tansho_baken(self):
        """単勝馬券ならTRUEを返す"""
        tansho_img = Image.open(self.TANSHO_BAKEN_MARK_IMG_PATH)
        cropped_img = self.image.crop((380, 5, 590, 740))
        return ImageUtil.are_same_image(tansho_img, cropped_img)
    
    def is_fukusho_baken(self):
        """複勝馬券ならTRUEを返す"""
        fukusho_img = Image.open(self.FUKUSHO_BAKEN_MARK_IMG_PATH)
        cropped_img = self.image.crop((380, 5, 590, 740))
        return ImageUtil.are_same_image(fukusho_img, cropped_img)
    
    def save(self, filePath):
        """画像を保存する"""        
        self.image.save(filePath)
        return


