from bincrafters import build_template_default
import os

def _is_static_msvc_build(build):
  if build.options["SpeexDSP:shared"] == False and build.settings["compiler"] == "Visual Studio":
    return False
  else:
    return True

if __name__ == "__main__":
  print "XXXX environment: {}".format(os.environ)
  builder = build_template_default.get_builder()
  builder.builds = filter(_is_static_msvc_build , builder.items)
  builder.run()
