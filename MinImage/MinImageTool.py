import sys
import os
import struct
import time
from PIL import Image

def convert_to_png():
    folder_path:str = sys.argv[2]
    folder_out:str = sys.argv[3]
    if "\\" in folder_path:
        folder_path = folder_path.replace("\\","/")
    if '"' in folder_path:
        folder_path = folder_path.replace('"','')
    if "\\" in folder_out:
        folder_out = folder_out.replace("\\","/")
    if '"' in folder_out:
        folder_out = folder_out.replace('"','')

    os.makedirs(folder_out,exist_ok=True)
    with open(f"{folder_path}\\frame_1.mimg",'rb') as fff:
        fff.seek(0x08)
        width_bytes = fff.read(0x04)
        fff.seek(0x0C)
        height_bytes = fff.read(0x04)
        width = int.from_bytes(width_bytes,byteorder='little')
        height = int.from_bytes(height_bytes,byteorder='little')
        fff.seek(0x18)
        get_frame_count = fff.read(0x04)
        frame_count = int.from_bytes(get_frame_count,byteorder='little')
        fff.close()

    for i in range(1,frame_count+1):
        with open(f'{folder_path}\\frame_{i}.mimg','rb+') as f:
            f.seek(0x20)
            raw_data = f.read()

        image = Image.frombytes('RGB', (width, height), raw_data)
        b, g, r = image.split()
        bgr_image = Image.merge('RGB', (r, g, b))
        bgr_image.save(f'{folder_out}/frame_{i}.png')

def help():
    print(f"\nExample Usage:\n")
    print(f" python MinImmageTool.py get-frames [YourMinVideoPath/File] [YourOptionalOutputPath]")
    print("        ^                ^          ^                    ^")
    print("        Script Name      Command    MinVideo Path      Optional Output Path\n\n")
    print(f"Accepted Flags:\n\n 'get-frames'        - Gets the Frames from a MinVideo File.\n 'convert-frames'    - Converts Frames from MinVideo into *.png\n\n")

def frames_to_image(file,outpath):
    os.makedirs(outpath,exist_ok=True)
    with open(file,'rb+') as f:
        f.seek(0x10)
        length = len(f.read())
        f.seek(0x00)
        width_bytes = f.read(0x08)
        f.seek(0x08)
        height_bytes = f.read(0x08)
        heightint,widthint = int.from_bytes(height_bytes,byteorder='little'),int.from_bytes(width_bytes,byteorder='little')
        frame_size = heightint*widthint # Get frame area
        data_size = frame_size*3 # 3 bytes per pixel (bgr) * Frame Area
        get_fram_num = length/data_size
        w = struct.unpack('<I', width_bytes[:4])[0]
        h = struct.unpack('<I', height_bytes[:4])[0]
        header_data = b'mimg\x0A\x0D\x00\x01'
        end_header_data = b'\xFF\x0A\x0D\xFF'
        f.seek(0x10)
        itteration = 1
        frame_number = round(get_fram_num)
        frame_num_bytes = frame_number.to_bytes(4,byteorder='little')
        print(f'\nTotal Number of Frames: {frame_number}.')
        print(f"Video Frame Area/Size: {frame_size}.")
        print(f"Data Size of Images: {data_size}.")
        print(f'Width and Height: {w}*{h}.')
        print(f"Output Path: {outpath}\n")
        while 1==1:
            time.sleep(0.01)
            chunk = f.read(data_size)
            f.seek(data_size*itteration+16)
            if not chunk:
                break  # End of file
            with open(f'{outpath}\\frame_{itteration}.mimg', 'wb') as chunk_file:
                chunk_file.write(header_data);chunk_file.write(w.to_bytes(4, byteorder='little'));chunk_file.write(h.to_bytes(4, byteorder='little'));chunk_file.write(w.to_bytes(4, byteorder='little'));chunk_file.write(h.to_bytes(4, byteorder='little'));chunk_file.write(frame_num_bytes);chunk_file.write(end_header_data);chunk_file.write(chunk)
            itteration += 1
        print(f"Finished Frame Export.")

def get_frames():
    if len(sys.argv) < 3:
        print("MinVideo Path is Required")
        exit(1)
    path = sys.argv[2]

    if "\\" in path:
        path = path.replace("\\","/")
    
    if '"' in path:
        path = path.replace('"','')

    try:
        out_path = sys.argv[3]
        if "\\" in out_path:
            out_path = out_path.replace("\\","/")

        if '"' in out_path:
            out_path = out_path.replace('"','')
        frames_to_image(path,out_path)
        
    except IndexError:
        out_path='.\\out'
        frames_to_image(path,out_path)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit(1)

    match sys.argv[1]:
        case "get-frames":
            get_frames()

        case "convert-frames":
            convert_to_png()
        
        case "help":
            help()
            