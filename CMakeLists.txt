cmake_minimum_required(VERSION 3.4...3.18)
project(SurgView)
add_subdirectory(pybind11)

set(SPEECHSDK_ROOT $ENV{SPEECHSDK_ROOT})
link_directories(${SPEECHSDK_ROOT}/lib/arm64 libasound.so.2)

pybind11_add_module(azure_speech speech.cpp)
target_link_libraries(azure_speech PRIVATE pthread Microsoft.CognitiveServices.Speech.core)
target_include_directories(azure_speech PRIVATE ${SPEECHSDK_ROOT}/include/cxx_api ${SPEECHSDK_ROOT}/include/c_api)


