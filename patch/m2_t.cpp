#include <json/json.h>
#include <fstream>
#include <filesystem>
#include <json/value.h>

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

    return 0;
}