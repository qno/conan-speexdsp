cmake_minimum_required(VERSION 3.5)
project(LibSpeexDSPTest)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include (CheckIncludeFiles)
check_include_files (stdint.h HAVE_STDINT_H)
check_include_files (inttypes.h HAVE_INTTYPES_H)
check_include_files (sys/types.h HAVE_SYS_TYPES_H)

if (NOT MSVC)
  set (CONAN_LIBS ${CONAN_LIBS} m)
endif ()

# the tests are taken over from libspeexdsp src folder
foreach (TEST testdenoise testecho testjitter testresample testresample2)

  add_executable(${TEST} ${TEST}.c)

  if (MSVC)
    # _USE_MATH_DEFINES needed for M_PI
    target_compile_definitions(${TEST} PRIVATE HAVE_CONFIG_H _USE_MATH_DEFINES)
  endif ()

  if (HAVE_STDINT_H)
    target_compile_definitions(${TEST} PRIVATE HAVE_STDINT_H)
  elseif (HAVE_INTTYPES_H)
    target_compile_definitions(${TEST} PRIVATE HAVE_INTTYPES_H)
  elseif (HAVE_SYS_TYPES_H)
    target_compile_definitions(${TEST} PRIVATE HAVE_SYS_TYPES_H)
  endif ()

  target_link_libraries(${TEST} ${CONAN_LIBS})

endforeach ()
