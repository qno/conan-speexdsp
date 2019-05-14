from bincrafters import build_template_default
import os, platform, copy

# see https://github.com/bincrafters/bincrafters-package-tools/blob/master/README.md
# see https://github.com/conan-io/conan-package-tools/blob/develop/README.md
os.environ["BINTRAY_REPOSITORY"]            = "conan-public"
os.environ["CONAN_UPLOAD"]                  = "https://api.bintray.com/conan/qno/conan-public"
os.environ["CONAN_USERNAME"]                = "qno"
os.environ["CONAN_PASSWORD"]                = os.environ["BINTRAY_API_KEY"] # set by azure job
os.environ["CONAN_LOGIN_USERNAME"]          = os.environ["BINTRAY_LOGIN"]   # set by azure job
os.environ["CONAN_STABLE_BRANCH_PATTERN"]   = "stable/*"
os.environ["CONAN_UPLOAD_ONLY_WHEN_STABLE"] = "0"
os.environ["CONAN_DOCKER_32_IMAGES"]        = "1"
os.environ["CONAN_CHANNEL"]                 = "testing"


def _is_static_msvc_build(build):
    if build.options["SpeexDSP:shared"] == True and build.settings["compiler"] == "Visual Studio":
      return False
    else:
      return True


if __name__ == "__main__":
    builder = build_template_default.get_builder()

    # taken from - https://github.com/bincrafters/conan-libcurl/blob/testing/7.64.1/build.py
    items = []
    for item in builder.items:
        # skip mingw cross-builds
        if not (platform.system() == "Windows" and item.settings["compiler"] == "gcc" and
                item.settings["arch"] == "x86"):
            new_build_requires = copy.copy(item.build_requires)
            if platform.system() == "Windows" and item.settings["compiler"] == "gcc":
                # add msys2 and mingw as a build requirement for mingw builds
                new_build_requires["*"] = new_build_requires.get("*", []) + \
                    ["mingw_installer/1.0@conan/stable",
                     "msys2_installer/latest@bincrafters/stable"]

            items.append([item.settings, item.options, item.env_vars,
                          new_build_requires, item.reference])
    builder.items = items

    builder.builds = filter(_is_static_msvc_build , builder.items)
    builder.run()
