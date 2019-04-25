cmake_minimum_required (VERSION 3.5)
project (SpeexDSPTest)

set (CMAKE_CXX_STANDARD 11)

include (${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include (CheckIncludeFiles)
check_include_files (stdint.h HAVE_STDINT_H)
check_include_files (inttypes.h HAVE_INTTYPES_H)
check_include_files (sys/types.h HAVE_SYS_TYPES_H)

add_executable (speexdsptest speexdsptest.cpp)

if (HAVE_STDINT_H)
target_compile_definitions(speexdsptest PRIVATE HAVE_STDINT_H)
elseif (HAVE_INTTYPES_H)
target_compile_definitions(speexdsptest PRIVATE HAVE_INTTYPES_H)
elseif (HAVE_SYS_TYPES_H)
target_compile_definitions(speexdsptest PRIVATE HAVE_SYS_TYPES_H)
endif ()

conan_target_link_libraries (speexdsptest)
