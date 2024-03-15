import sys
import os
from baken_image import BakenImage

REQUIRED_ARGS_CNT = 2

# コマンドライン引数
if len(sys.argv) - 1 < REQUIRED_ARGS_CNT:
    print(f"エラー: 馬券画像が格納されているフォルダのパスを引数に指定してください。")
    print(f"使い方: python {sys.argv[0]} 画像フォルダパス 出力フォルダパス")
    sys.exit(1)

img_folder_path = sys.argv[1]
output_folder_path = sys.argv[2]

if not os.path.exists(img_folder_path):
    print("エラー:入力画像フォルダが存在しません。")
    sys.exit(1)

if not os.path.exists(output_folder_path):
    os.mkdir(output_folder_path)

png_filepaths = [os.path.join(img_folder_path, f)
              for f in os.listdir(img_folder_path)
              if f.endswith('.png')]

for file_path in png_filepaths:
    output_file_path = os.path.join(output_folder_path, os.path.basename(file_path))
    baken_image = BakenImage(file_path)
    baken_image.trim_unnesessary_parts()
    if not baken_image.is_jra_baken_image():
        print(f"JRA馬券画像ではありません:{file_path}")
        continue

    baken_image.mask_lower_betting_price()   
    if (baken_image.is_box_baken() or baken_image.is_nagashi_baken() or baken_image.is_formation_baken()):
        #ボックス/フォーメーション/流しは画像保存して終了
        baken_image.save(output_file_path)
        continue

    if baken_image.is_tansho_baken() or baken_image.is_fukusho_baken():
        #単複馬券はマスク位置が異なる
        baken_image.mask_right_betting_price(True)
        baken_image.save(output_file_path)
        continue

    baken_image.mask_right_betting_price()
    baken_image.save(output_file_path)