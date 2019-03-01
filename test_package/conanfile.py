import os

from conans import ConanFile, CMake, tools


class SpeexdspTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            for test in ["testdenoise", "testecho", "testjitter", "testresample", "testresample2"]:
                if test == "testjitter":
                    self.output.info("running '{}'".format(test))
                    self.run(".{}{}".format(os.sep, test))
                else:
                    self.output.warn("skip running '{}' - as it can't be executed within this test environment".format(test))
