#include <json/json.h>
#include <fstream>
#include <filesystem>
#include <json/value.h>
#include <iostream>

namespace fs = std::filesystem;

Json::Value readjson(const std::string &file) {
    std::ifstream jsonfile(file, std::ifstream::binary);
    Json::Value root;
    Json::CharReaderBuilder readerBuilder;
    std::string errs;

    if (!Json::parseFromStream(readerBuilder, jsonfile, &root, &errs)) {
        throw std::runtime_error("Failed to parse JSON file: " + file + ", error: " + errs);
    }

    return root;
}

void writejson(Json::Value &root, const std::string &file){
    Json::StreamWriterBuilder builder;
    builder["emitUTF8"] = true;

    std::ofstream output(file);
    std::unique_ptr<Json::StreamWriter> writer(builder.newStreamWriter());
    writer->write(root, &output);
    output.close();
}

Json::Value processTexts(const Json::Value& root, const Json::Value& patchData = Json::nullValue) {
    Json::Value outputArray(Json::arrayValue);

    Json::Value modifiedRoot = root;

    for (Json::Value& scene : modifiedRoot["scenes"]) {
        if (scene.isObject() && scene.isMember("texts") && scene["texts"].isArray()) {
            for (Json::Value& textArray : scene["texts"]) {
                if (textArray.isArray() && textArray.size() >= 3) {
                    Json::Value line(Json::arrayValue);

                    for (int i = 0; i < 3; ++i) {
                        if (patchData.isArray() && 
                            patchData.size() > outputArray.size() && 
                            patchData[outputArray.size()].isArray() && 
                            patchData[outputArray.size()][i].isString()) {
                            if (patchData[outputArray.size()][i].asString().empty()) {
                                line.append(Json::nullValue);
                                textArray[i] = Json::nullValue;
                            } else {
                                line.append(patchData[outputArray.size()][i].asString());
                                textArray[i] = patchData[outputArray.size()][i].asString();
                            }
                        } else if (textArray[i].isNull() || !textArray[i].isString()) {
                            line.append(Json::nullValue);
                            textArray[i] = Json::nullValue;
                        } else {
                            line.append(textArray[i].asString());
                        }
                    }
                    outputArray.append(line);
                }
            }
        }
    }
    if (patchData == Json::nullValue) return outputArray;
    else return modifiedRoot;
}


int main(int argc, char* argv[]){
    /*
    Json::Value root = readjson(argv[1]);

    if (fs::exists("patch.json")) {
        Json::Value patchRoot = readjson("patch.json");
        root = processTexts(root, patchRoot);
        writejson(root, "result.json");
    } 
    else {
        root = processTexts(root);
        writejson(root, "out.json");
    }
    */

    fs::path src_dir = argv[1];
    fs::path patch_dir = src_dir.parent_path() / "patch";
    bool mode_patch = true;

    if (!fs::exists(patch_dir)) {
        fs::create_directory(patch_dir);
        mode_patch = false;
    }


    try {
        for (const auto& entry : fs::recursive_directory_iterator(src_dir)) {
            if (entry.is_regular_file() && entry.path().extension() == ".json") {
                Json::Value root = readjson(entry.path().string());
                std::string new_filename = "patch_" + entry.path().filename().string();
                fs::path dest_path = patch_dir / new_filename;
                if (mode_patch){
                    Json::Value patchRoot = readjson(dest_path.string());
                    root = processTexts(root, patchRoot);
                    writejson(root, entry.path().string());
                }
                else{
                    root = processTexts(root);
                    writejson(root, dest_path.string());
                }
            }
        }
    } catch (const fs::filesystem_error& e) {
        std::cerr << "error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}