#include <iostream>
#include <fstream>
#include <sstream>
#include <filesystem>
#include <vector>
#include <string>
#include <cstdint>
#include <chrono>
#include <thread>
#include <algorithm>

void help() {
    std::cout << "\nExample Usage:\n";
    std::cout << "MinImmageTool.exe get-frames [YourMinVideoPath/File] [YourOptionalOutputPath]\n";
    std::cout << "^                 ^          ^                       ^\n";
    std::cout << "Executable Name   Command    MinVideo Path           Optional Output Path\n\n";
    std::cout << "Accepted Flags:\n\n 'get-frames'        - Gets the Frames from a MinVideo File.\n 'help'              - Displays this Message.\n\n";
}

void frames_to_image(const std::string& file, const std::string& outpath) {
    std::filesystem::create_directories(outpath);
    std::ifstream f(file, std::ios::binary);
    if (!f) {
        std::cerr << "Error opening file.\n";
        return;
    }

    f.seekg(0x10);
    std::streampos length = f.tellg();
    f.seekg(0, std::ios::end);
    length = f.tellg() - length;
    f.seekg(0x00);

    std::vector<uint8_t> width_bytes(0x08);
    f.read(reinterpret_cast<char*>(width_bytes.data()), 0x08);

    std::vector<uint8_t> height_bytes(0x08);
    f.read(reinterpret_cast<char*>(height_bytes.data()), 0x08);

    uint32_t widthint = *reinterpret_cast<uint32_t*>(width_bytes.data());
    uint32_t heightint = *reinterpret_cast<uint32_t*>(height_bytes.data());
    uint32_t frame_size = heightint * widthint;
    uint32_t data_size = frame_size * 3;

    double get_fram_num = static_cast<double>(length) / data_size;
    uint32_t frame_number = static_cast<uint32_t>(get_fram_num);
    std::cout << "\nTotal Number of Frames: " << frame_number << ".\n";
    std::cout << "Video Frame Area/Size: " << frame_size << ".\n";
    std::cout << "Data Size of Images: " << data_size << ".\n";
    std::cout << "Width and Height: " << widthint << "*" << heightint << ".\n";
    std::cout << "Output Path: " << outpath << "\n\n";

    f.seekg(0x10);
    uint32_t iteration = 1;

    while (true) {
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
        std::vector<uint8_t> chunk(data_size);
        f.read(reinterpret_cast<char*>(chunk.data()), data_size);
        f.seekg(data_size * iteration + 0x10);
        if (!f)
            break;  // End of file

        std::ostringstream filename;
        filename << outpath << "/frame_" << iteration << ".mimg";
        std::ofstream chunk_file(filename.str(), std::ios::binary);
        chunk_file.write("mimg\x0A\x0D\x00\x01", 8);
        chunk_file.write(reinterpret_cast<char*>(&widthint), 4);
        chunk_file.write(reinterpret_cast<char*>(&heightint), 4);
        chunk_file.write(reinterpret_cast<char*>(&widthint), 4);
        chunk_file.write(reinterpret_cast<char*>(&heightint), 4);
        chunk_file.write(reinterpret_cast<char*>(&frame_number), 4);
        chunk_file.write("\xFF\x0A\x0D\xFF", 4);
        chunk_file.write(reinterpret_cast<char*>(chunk.data()), data_size);
        iteration++;
    }
    std::cout << "Finished Frame Export.\n";
}

void get_frames(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "MinVideo Path is Required\n";
        exit(1);
    }

    std::string path = argv[2];

    std::replace(path.begin(), path.end(), '\\', '/');
    if (path.front() == '\"' && path.back() == '\"') {
        path = path.substr(1, path.size() - 2);
    }

    std::string out_path;
    if (argc >= 4) {
        out_path = argv[3];
        std::replace(out_path.begin(), out_path.end(), '\\', '/');
        if (out_path.front() == '\"' && out_path.back() == '\"') {
            out_path = out_path.substr(1, out_path.size() - 2);
        }
    } else {
        out_path = "./out";
    }

    frames_to_image(path, out_path);
}

int main(int argc, char* argv[]) {
    if (argc <= 1) {
        exit(1);
    }

    if (std::string(argv[1]) == "get-frames") {
        get_frames(argc, argv);
    } else if (std::string(argv[1]) == "help") {
        help();
    }

    return 0;
}
