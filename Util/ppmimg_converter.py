import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

def convert_image_to_ppm(input_image_path, output_ppm_path):
    try:
        # 이미지 읽기 (OpenCV를 이용하여)
        image = cv2.imread(input_image_path)

        # 이미지의 높이, 너비, 채널 수 가져오기
        height, width, channels = image.shape

        if channels == 3:  # RGB 이미지인 경우
            max_val = 255
        else:
            raise ValueError("PPM 포맷은 3채널 RGB 이미지만 지원합니다.")

        # PPM 파일에 데이터를 쓰기 (P3 텍스트 기반 포맷)
        with open(output_ppm_path, 'w') as ppm_file:
            # PPM 헤더 작성
            ppm_file.write(f'P3\n')  # 텍스트 기반 PPM 포맷
            ppm_file.write(f'{width} {height}\n')
            ppm_file.write(f'{max_val}\n')

            # 각 픽셀의 RGB 값을 PPM 파일에 쓰기
            for row in range(height):
                for col in range(width):
                    r, g, b = image[row, col]
                    ppm_file.write(f'{r} {g} {b} ')
                ppm_file.write('\n')

        messagebox.showinfo("성공", f"PPM 파일로 변환 완료: {output_ppm_path}")
    except Exception as e:
        messagebox.showerror("오류", f"이미지 변환 중 오류 발생: {str(e)}")

def convert_ppm_to_jpg(ppm_image_path, output_jpg_path):
    try:
        # PPM 이미지 불러오기
        image = Image.open(ppm_image_path)

        # JPG 파일로 저장
        image.save(output_jpg_path, format='JPEG')

        messagebox.showinfo("성공", f"JPG 파일로 변환 완료: {output_jpg_path}")
    except Exception as e:
        messagebox.showerror("오류", f"PPM에서 JPG로 변환 중 오류 발생: {str(e)}")

def open_image_for_ppm():
    # 파일 다이얼로그를 통해 이미지를 선택 (PPM 변환)
    input_image_path = filedialog.askopenfilename(
        title="이미지 파일 선택", 
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if input_image_path:
        save_ppm(input_image_path)

def open_image_for_jpg():
    # 파일 다이얼로그를 통해 PPM 파일 선택 (JPG 변환)
    ppm_image_path = filedialog.askopenfilename(
        title="PPM 파일 선택", 
        filetypes=[("PPM files", "*.ppm")]
    )
    if ppm_image_path:
        save_jpg(ppm_image_path)

def save_ppm(input_image_path):
    # 파일 다이얼로그를 통해 PPM 파일 저장 경로 선택
    output_ppm_path = filedialog.asksaveasfilename(
        title="PPM 파일 저장", 
        defaultextension=".ppm", 
        filetypes=[("PPM files", "*.ppm")]
    )
    if output_ppm_path:
        convert_image_to_ppm(input_image_path, output_ppm_path)

def save_jpg(ppm_image_path):
    # 파일 다이얼로그를 통해 JPG 파일 저장 경로 선택
    output_jpg_path = filedialog.asksaveasfilename(
        title="JPG 파일 저장", 
        defaultextension=".jpg", 
        filetypes=[("JPG files", "*.jpg")]
    )
    if output_jpg_path:
        convert_ppm_to_jpg(ppm_image_path, output_jpg_path)

# GUI 설정
def create_gui():
    root = tk.Tk()
    root.title("이미지 PPM/JPG 변환기")
    root.geometry("300x200")

    # PPM 변환 버튼
    open_ppm_button = tk.Button(root, text="Image to PPM", command=open_image_for_ppm)
    open_ppm_button.pack(pady=20)

    # JPG 변환 버튼
    open_jpg_button = tk.Button(root, text="PPM to Image", command=open_image_for_jpg)
    open_jpg_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
