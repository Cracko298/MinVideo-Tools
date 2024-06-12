import sys, os, struct, time, re
import moviepy.editor as mp
from PIL import Image

def upscale_images():
    directory = sys.argv[2]
    scale_factor = int(sys.argv[3])
    files = os.listdir(directory)
    
    for file in files:
        if file.startswith("frame_") and file.endswith(".png"):
            file_path = os.path.join(directory, file)
            
            # Open the image
            with Image.open(file_path) as img:
                width, height = img.size
                new_width = width * scale_factor
                new_height = height * scale_factor
                upscaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                upscaled_img.save(file_path)
                print(f"Upscaled {file} to {new_width}x{new_height}")

def png_to_gif():
    png_path = sys.argv[2]
    try:
        gif_out_path = sys.argv[3]
    except IndexError:
        gif_out_path = f".\\output_{os.path.basename(png_path)}.gif"
    if "\\" in png_path:
        png_path = png_path.replace("\\","/")
    if '"' in png_path:
        png_path = png_path.replace('"','')
    if "\\" in gif_out_path:
        gif_out_path = gif_out_path.replace("\\","/")
    if '"' in gif_out_path:
        gif_out_path = gif_out_path.replace('"','')
    
    frame_list = []
    for file in os.listdir(png_path):
        if 'frame' in file:
            frame_list.append(f"{png_path}/{file}")

    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else 0

    sorted_png_path = sorted(frame_list, key=lambda x: extract_number(os.path.basename(x)))
    frames = [Image.open(frame) for frame in sorted_png_path]

    frames[0].save(
        'output.gif',
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=33, #defualt is 30fps
        loop=0
    )

def gif_to_mp4():
    clip = mp.VideoFileClip(".\\output.gif")
    clip.write_videofile(".\\mp4_output.mp4")


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
        r, g, b = image.split()
        bgr_image = Image.merge('RGB', (r, g, b))
        bgr_image.save(f'{folder_out}/frame_{i}.png')

def help():
    print(f"\nExample Usage:\n")
    print(f" python MinImmageTool.py get-frames [YourMinVideoPath/File] [YourOptionalOutputPath]")
    print("        ^                ^          ^                       ^")
    print("        Script Name      Command    MinVideo Path           Optional Output Path\n\n")
    print(f"Accepted Flags:\n\n 'get-frames'        - Gets the Frames from a MinVideo File.\n 'convert-frames'    - Converts Frames from MinVideo *.mimg into *.png\n 'png-2-gif'         - Converts *.png Frames extracted from *.minv into a *.gif File called 'output.gif'\n                       in the current running Directory.\n 'gif-2-mp4'         - Converts the Generated *.gif into a Compressed *.mp4 in H.264 Codec.\n 'extract-frame'     - Extracts a specified Frame from *.minv instead of Extracting all Frames.\n 'upscale'           - Upscales *.png Images to get a more clearer Image than the Extracted MinVideo Frames.\n\n")

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
        frame_size = heightint*widthint
        data_size = frame_size*3
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
        print(f"Data Size of Images: {round(data_size/1000,5)}kb.")
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

def extract_frame():
    minv_file = sys.argv[2]
    frame_number = int(sys.argv[3])
    outpath = ".\\"
    os.makedirs(outpath, exist_ok=True)
    with open(minv_file, 'rb') as f:
        f.seek(0x10)
        length = len(f.read())
        f.seek(0x00)
        width_bytes = f.read(0x08)
        f.seek(0x08)
        height_bytes = f.read(0x08)
        heightint, widthint = int.from_bytes(height_bytes, byteorder='little'), int.from_bytes(width_bytes, byteorder='little')
        frame_size = heightint * widthint
        data_size = frame_size * 3
        total_frames = length // data_size
        w = struct.unpack('<I', width_bytes[:4])[0]
        h = struct.unpack('<I', height_bytes[:4])[0]
        header_data = b'mimg\x0A\x0D\x00\x01'
        end_header_data = b'\xFF\x0A\x0D\xFF'
        
        if frame_number > total_frames or frame_number <= 0:
            print(f"Frame number {frame_number} is out of range. There are only {total_frames} frames.")
            return

        print(f'\nTotal Number of Frames: {total_frames}.')
        print(f"Video Frame Area/Size: {frame_size}.")
        print(f"Data Size of Images: {round(data_size / 1000, 5)}kb.")
        print(f'Width and Height: {w}*{h}.')
        print(f"Output Path: {outpath}\n")

        f.seek(0x10 + data_size * (frame_number - 1))
        chunk = f.read(data_size)
        if chunk:
            with open(f'{outpath}\\frame_{frame_number}.mimg', 'wb') as chunk_file:
                chunk_file.write(header_data)
                chunk_file.write(w.to_bytes(4, byteorder='little'))
                chunk_file.write(h.to_bytes(4, byteorder='little'))
                chunk_file.write(w.to_bytes(4, byteorder='little'))
                chunk_file.write(h.to_bytes(4, byteorder='little'))
                chunk_file.write(frame_number.to_bytes(4, byteorder='little'))
                chunk_file.write(end_header_data)
                chunk_file.write(chunk)
            print(f"Extracted Frame {frame_number}.")
        else:
            print(f"Failed to read frame {frame_number} data.")

def get_frames():
    if len(sys.argv) < 3:
        print("MinVideo Path is Required")
        sys.exit(1)
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
        sys.exit(1)

    match sys.argv[1]:
        case "get-frames":
            get_frames()

        case "convert-frames":
            convert_to_png()

        case "png-2-gif":
            png_to_gif()

        case "gif-2-mp4":
            gif_to_mp4()

        case "extract-frame":
            extract_frame()

        case "upscale":
            upscale_images()
        
        case "help":
            help()
        
            