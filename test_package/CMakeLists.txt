cmake_minimum_required(VERSION 3.5)
project(LibSpeexDSPTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if ("${CMAKE_C_COMPILER_ID}" STREQUAL "GNU")
  set (CONAN_LIBS ${CONAN_LIBS} m)
endif ()

# the tests are taken over from libspeexdsp src folder
foreach (TEST testdenoise testecho testjitter testresample testresample2)

  add_executable(${TEST} ${TEST}.c)

  if (MSVC)
    # _USE_MATH_DEFINES needed for M_PI
    target_compile_definitions(${TEST} PRIVATE HAVE_CONFIG_H _USE_MATH_DEFINES)
  # this is a workaround and needs to be fixed by configure_file with CMake
  else () # GCC or Clang
    target_compile_definitions(${TEST} PRIVATE HAVE_STDINT_H)
  endif ()

  target_link_libraries(${TEST} ${CONAN_LIBS})

endforeach ()
