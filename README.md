# MinVideo Tools
- These are tools for the MinVideo Format (.minv/.miv).
- Extract Frames from MinVideo, and convert them to *.png Images.
- Convert Extracted frames into `*.gif`, and then into `*.mp4`.

## Usage:
```
python MinImageTool.py
       get-frames      [yourMinVideoFilePATH]   [yourOutputPATH]            - Gets the Frames from a MinVideo File.
       convert-frames  [yourMinImageFolderPATH] [yourPNGOutputPATH]         - Converts Frames from MinVideo *.mimg to *.png Images.
       png-2-gif       [yourPNGFolderPATH]      [yourOutputGIFNameAndPATH]  - Converts *.png Frames extracted from *.minv to *.gif running at a fixed 30FPS. 
       gif-2-mp4       [yourGIF_PATH]           [yourOutputMP4NameAndPATH]  - Converts the Generated *.gif into a Compressed H.264 Codec MP4 File.
       extract-frame   [yourMinVideoFilePATH]   [frameYouWantExtracted]     - Extracts a specified Fream from *.minv instead of Extracting all Frames.
       upscale         [yourPNGImagePATH]       [yourScaling]               - Upscales *.png Images to get a more clearer Image than the Extracted MinVideo Frames.
```

## Extra Formats:
### MinImage:
- MinImage is a format designed to be cross-compatible with MinVideo.
- Basically just Frame Information and Data that has a some Traditional Header Information.
- Simple, uncompressed images, no algorithm encoding with pure `RGB` Formatting.
```
Header Data is a total of 0x20 (32) Bytes at the beginning of the File.
Bytes 0x00 - 0x03 is the Name of The Header (mimg).
Bytes 0x04 - 0x05 Defines the Start of the Header Information.
Bytes 0x06 - 0x07 is the Mode which the file should be read.
- 0x01 is Raw BGR
- 0x02 is Raw RGB
- 0x03 is Raw ETC2_BGR
- 0x04 is Raw ETC2_RGB
Bytes 0x08 - 0x0B is the Width.
Bytes 0x0C - 0x0F is the Height.
Bytes 0x10 - 0x13 is the Width Checksum.
Bytes 0x14 - 0x17 is the Height Checksum.
Bytes 0x18 - 0x1B is the Frame Count of the Video.
Bytes 0x1C - 0x20 is the Defining the End of the Header Data.
```

### MinGIF:
- MinGIF is a format designed to be cross-compatible with MinVideo.
- Which is basically a bunch of images showed in Rapid succession (such as a GIF).
- Simple and Uncompressed. No encoding alg, just pure `RGB` Formatting.
```
Header Data is a total of 0x20 (32) Bytes at the beginning of the File.
This format copies over the majority of Formatting/Header from *.mimg
Bytes 0x00 - 0x03 is the Name of The Header (mgif).
Bytes 0x04 - 0x05 Defines the Start of the Header Information.
Bytes 0x06 - 0x07 is the Mode which the file should be read.
- 0x01 is Raw BGR
- 0x02 is Raw RGB
- 0x03 is Raw ETC2_BGR
- 0x04 is Raw ETC2_RGB
Bytes 0x08 - 0x0B is the Width.
Bytes 0x0C - 0x0F is the Height.
Bytes 0x10 - 0x13 is the Width Checksum.
Bytes 0x14 - 0x17 is the Height Checksum.
Bytes 0x18 - 0x1B is the Frame Count of the Video.
Bytes 0x1C - 0x20 is the Defining the End of the Header Data.
```
