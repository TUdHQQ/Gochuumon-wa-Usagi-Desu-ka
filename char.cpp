#include <iostream>
#include <fstream>
#include <unordered_set>
#include <string>

std::string readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    file.close();
    return content;
}

void writeFile(const std::string& filename, const std::string& content) {
    std::ofstream file(filename, std::ios::binary);
    file << content;
    file.close();
}

int main() {
    try {
        std::string input = readFile("text.txt");
        std::unordered_set<std::string> uniqueChars;
        std::string output;

        for (size_t i = 0; i < input.size();) {
            unsigned char c = input[i];
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

            std::string character = input.substr(i, charLen);

            if (uniqueChars.find(character) == uniqueChars.end()) {
                uniqueChars.insert(character);
                output += character;
            }

            i += charLen;
        }

        writeFile("text_out.txt", output);


    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
