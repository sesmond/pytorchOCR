cmake_minimum_required(VERSION 3.13)
project(psenetncnn)
set(INC_DIR /usr/include
        /usr/local/cuda/include #cuda的include位置 修改为正确的地方
        /home/litchi/project/ncnn/build/install/include # ncnn的安装位置
        )
set(LINK_DIR /usr/lib
        /usr/lib/x86_64-linux-gnu/
        /usr/local/cuda/lib64 #cuda的lib位置 修改为正确的地方
        /home/litchi/project/ncnn/build/install/lib/libncnn.a #ncnn.a所在位置
        )
set(OpenCV_DIR /usr/local/share/OpenCV) #opencv的位置
find_package(OpenCV REQUIRED)
find_package(OpenMP REQUIRED)
if(OPENMP_FOUND)
        message("OPENMP FOUND")
        set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()
# 头文件搜索目录
include_directories(${INC_DIR}${OpenCV_INCLUDE_DIRS})
# 库文件搜索目录
link_directories(${LINK_DIR}${OpenCV_LIBS})

set(CMAKE_CXX_STANDARD 14)
#生成可执行文件(对应一个cpp文件的main函数)
add_executable(psenetncnn main.cpp)

# 要链接的动态库, 参数指明库的名字即可，比如libxxxx1.so, 指明是xxxx1即可！！！
target_link_libraries(psenetncnn
        ${OpenCV_LIBS}
        ${LINK_DIR}
        )
