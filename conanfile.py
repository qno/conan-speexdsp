from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os


class SpeexDSPConan(ConanFile):
    name = "SpeexDSP"
    version = "1.2rc3"
    license = "BSD"
    author = "Xiph.Org Foundation"
    url = "https://github.com/qno/conan-speexdsp"
    description = "SpeexDSP is a patent-free, Open Source/Free Software DSP library."

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    _pkg_name = "speexdsp-1.2rc3"
    _libname = "speexdsp"

    def source(self):
        url = "http://downloads.xiph.org/releases/speex/{}.tar.gz".format(self._pkg_name)
        self.output.info("Downloading {}".format(url))
        tools.get(url)
        self._createCMakeLists()


    def configure(self):
        if self._isVisualStudioBuild() and self.options.shared:
            raise ConanInvalidConfiguration("This library doesn't support dll's on Windows")

    def build(self):
        if self._isVisualStudioBuild():
            cmake = CMake(self)
            cmake.configure(source_dir=self._pkg_name)
            cmake.build()
        else:
            config_args = []
            if self.options.shared:
                config_args = ["--disable-static"]
            else:
                config_args = ["--disable-shared"]
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(configure_dir=self._pkg_name, args=config_args)
            autotools.make()
            autotools.install()

    def package(self):
        self.copy("include/speex/*.h", dst=".", src=self._pkg_name)
        self.copy("speexdsp_config_types.h", dst="include/speex", src=".")
        if self._isVisualStudioBuild():
            self.copy("win32/config.h", dst="include", src=self._pkg_name)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self._libname]
        if self._isVisualStudioBuild():
            # in include/win32 config.h is provided
            self.cpp_info.includedirs = ["include", "include/win32"]

    def _isVisualStudioBuild(self):
        return self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"

    def _createCMakeLists(self):
        content = '''\
# THIS FILE WAS GENERATED BY CONAN RECIPE. DO NOT EDIT THIS FILE!
cmake_minimum_required(VERSION 3.5)
project(SpeexDSP)

if (NOT MSVC)
  message(FATAL_ERROR "Abort proccessing - this CMake project has only support for MS Visual Studio!")
endif ()

# the following checks and configure_file steps are trying somehow to reproduce the steps from
# https://github.com/xiph/speexdsp/blob/887ac103dbbd0533ed501fc3dd599c876cc0eec7/configure.ac#L280
# this is not 100% exactly the same, but as this CMakeLists.txt is only for used for MSVC compiler, the
# obtained types for the typdefs are correct. It even just works without to configure the
# speexdsp_config_types.h.in at all for building with Visual Studio.

include (CheckTypeSize)
include (CheckIncludeFiles)

check_include_files (stdint.h HAVE_STDINT_H)
check_include_files (inttypes.h HAVE_INTTYPES_H)
check_include_files (sys/types.h HAVE_SYS_TYPES_H)

check_type_size ("int16_t" INT16_T)
message ("size: ${{INT16_T}}")
check_type_size ("short" SHORT16)
message ("size: ${{SHORT16}}")
check_type_size ("int" INT16)
message ("size: ${{INT16}}")
if (HAVE_INT16_T)
  set (SIZE16 "int16_t")
elseif (HAVE_SHORT16)
  set (SIZE16 "short")
elseif (HAVE_INT16)
  set (SIZE16 "int")
endif ()
if (NOT DEFINED SIZE16)
  message (configure of speexdsp_config_types.h.in will fail - WARNING "SIZE16 type check failed")
endif ()

check_type_size ("uint16_t" UINT16_T)
message ("size: ${{UINT16_T}}")
check_type_size ("u_int16_t" U_INT16_T)
message ("size: ${{U_INT16_T}}")
check_type_size ("unsigned short" USHORT16)
message ("size: ${{USHORT16}}")
check_type_size ("unsigned int" UINT16)
message ("size: ${{UINT16}}")
if (HAVE_UINT16_T)
  set (USIZE16 "uint16_t")
elseif (HAVE_U_INT16_T)
  set (USIZE16 "u_int16_t")
elseif (HAVE_USHORT16)
  set (USIZE16 "unsigned short")
elseif (HAVE_UINT16)
  set (USIZE16 "unsigned int")
endif ()
if (NOT DEFINED USIZE16)
  message (configure of speexdsp_config_types.h.in will fail - WARNING "USIZE16 type check failed")
endif ()

check_type_size ("int32_t" INT32_T)
message ("size: ${{INT32_T}}")
check_type_size ("int" INT32)
message ("size: ${{INT32}}")
check_type_size ("long" LONG)
message ("size: ${{LONG}}")
check_type_size ("short" SHORT32)
message ("size: ${{SHORT32}}")
if (HAVE_INT32_T)
  set (SIZE32 "int32_t")
elseif (HAVE_INT32)
  set (SIZE32 "int")
elseif (HAVE_LONG)
  set (SIZE32 "long")
elseif (HAVE_SHORT32)
  set (SIZE32 "short")
endif ()
if (NOT DEFINED SIZE32)
  message (configure of speexdsp_config_types.h.in will fail - WARNING "SIZE32 type check failed")
endif ()

check_type_size ("uint32_t" UINT32_T)
message ("size: ${{UINT32_T}}")
check_type_size ("u_int32_t" U_INT32_T)
message ("size: ${{U_INT32_T}}")
check_type_size ("unsigned short" USHORT32)
message ("size: ${{USHORT32}}")
check_type_size ("unsigned int" UINT32)
message ("size: ${{UINT32}}")
check_type_size ("unsigned long" ULONG)
message ("size: ${{ULONG}}")
set (USIZE32 FALSE)
if (HAVE_UINT32_T)
  set (USIZE32 "uint32_t")
elseif (HAVE_U_INT32_T)
  set (USIZE32 "u_int32_t")
elseif (HAVE_USHORT32)
  set (USIZE32 "unsigned short")
elseif (HAVE_UINT32)
  set (USIZE32 "unsigned int")
elseif (HAVE_ULONG)
  set (USIZE32 "unsigned long")
endif ()
if (NOT DEFINED USIZE32)
  message (WARNING "configure of speexdsp_config_types.h.in will fail - USIZE32 type check failed")
endif ()

message ("determined 'SIZE16' type as  '${{SIZE16}}'")
message ("determined 'USIZE16' type as '${{USIZE16}}'")
message ("determined 'SIZE32' type as  '${{SIZE32}}'")
message ("determined 'USIZE32' type as '${{USIZE32}}'")

configure_file(include/speex/speexdsp_config_types.h.in speexdsp_config_types.h)

include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)
conan_basic_setup()
set(LIBSPEEXDSP "{}")

set(SOURCES libspeexdsp/buffer.c
            libspeexdsp/fftwrap.c
            libspeexdsp/filterbank.c
            libspeexdsp/jitter.c
            libspeexdsp/kiss_fft.c
            libspeexdsp/kiss_fftr.c
            libspeexdsp/mdf.c
            libspeexdsp/preprocess.c
            libspeexdsp/resample.c
            libspeexdsp/scal.c
            libspeexdsp/smallft.c)
add_library(${{LIBSPEEXDSP}} ${{SOURCES}})
target_include_directories(${{LIBSPEEXDSP}} PRIVATE include libspeexdsp win32 ${{CMAKE_CURRENT_BINARY_DIR}})
target_compile_definitions(${{LIBSPEEXDSP}} PRIVATE D_LIB HAVE_CONFIG_H)
if (HAVE_STDINT_H)
    target_compile_definitions(${{LIBSPEEXDSP}} PRIVATE HAVE_STDINT_H)
  elseif (HAVE_INTTYPES_H)
    target_compile_definitions(${{LIBSPEEXDSP}} PRIVATE HAVE_INTTYPES_H)
  elseif (HAVE_SYS_TYPES_H)
    target_compile_definitions(${{LIBSPEEXDSP}} PRIVATE HAVE_SYS_TYPES_H)
  endif ()
'''.format(self._libname)

        self.output.info("create CMakeLists.txt file")
        cmake_file = os.path.join(self._pkg_name, "CMakeLists.txt")
        f = open(cmake_file, "w+")
        f.write(content)
        f.close()
