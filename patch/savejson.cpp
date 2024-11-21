#include <json/json.h>
#include <fstream>
#include <json/value.h>

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

int main(int argc, char* argv[]){
    Json::Value root = readjson(argv[1]);
    writejson(root, "qwq.json");
    return 0;
}