# MinVideo Tools
- Theseare tools for MinVideo format (.minv/.miv)

## Extra Formats:
### MinImage:
- MinImage is a format designed to be cross-compatible with MinVideo.
- Basically just Frame Information and Data that has a some Traditional Header Information.
- Simple, uncompressed images, no algorithm encoding with pure `BGR/RGB` formatting.
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
