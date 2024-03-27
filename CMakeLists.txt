cmake_minimum_required(VERSION 3.27)
project(heatmap)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED YES)

set(SOURCE_FILES main.cpp)

add_executable(xorshift ${SOURCE_FILES})

