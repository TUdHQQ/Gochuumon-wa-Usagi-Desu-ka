#include <iostream>
#include <fstream>
#include <unordered_set>
#include <string>
#include <filesystem>

int main() {
    try {
        std::unordered_set<std::string> uniqueChars;
        std::string directoryPath = "./patch"; // 设置要读取的目录路径

        for (const auto& entry : std::filesystem::recursive_directory_iterator(directoryPath)) {
            if (entry.is_regular_file()) {
                std::ifstream file(entry.path(), std::ios::binary);
                if (file.is_open()) {
                    std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
                    file.close();

                    for (size_t i = 0; i < content.size();) {
                        unsigned char c = content[i];
                        size_t charLen = 1;
                        if ((c & 0x80) == 0x00) {
                            charLen = 1; 
                        } else if ((c & 0xE0) == 0xC0) {
                            charLen = 2; 
                        } else if ((c & 0xF0) == 0xE0) {
                            charLen = 3; 
                        } else if ((c & 0xF8) == 0xF0) {
                            charLen = 4; 
                        }

                        std::string character = content.substr(i, charLen);
                        uniqueChars.insert(character);
                        i += charLen;
                    }
                }
            }
        }

        std::ofstream outFile("text.txt", std::ios::binary);
        for (const std::string& character : uniqueChars) {
            outFile << character;
        }
        outFile.close();

    } catch (const std::exception& e) {
        std::cerr << "错误：" << e.what() << std::endl;
        return 1;
    }

    return 0;
}