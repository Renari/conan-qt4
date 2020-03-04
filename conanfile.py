from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class Qt4Conan(ConanFile):
    name = "Qt4"
    version = "4.8.5"
    description = "Keep it short"
    topics = ("conan", "libQt4", "Qt 4.8.5 Library")
    url = "https://download.qt.io/archive/qt/4.8"
    homepage = "https://www.qt.io/"
    license = "LGPL-3.0"
    requires = ["fontconfig/2.13.92@tdelame/stable",
                "freetype/2.9.1@tdelame/stable",
                "libSM/1.2.3@tdelame/stable",
                "libICE/1.0.10@tdelame/stable"]

    # Options may need to change depending on the packaged library
    settings = "os", "arch", "build_type"

    _source_subfolder = "src"
    _build_subfolder = "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "qt-everywhere-opensource-src-4.8.5"
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=["-confirm-license",
                                      "-opensource",
                                      "-static",
                                      "-qt3support",
                                      "-qt-zlib",
                                      "-qt-libtiff",
                                      "-qt-libpng",
                                      "-qt-libmng",
                                      "-qt-libjpeg",
                                      "-nomake", "examples",
                                      "-nomake", "demo"])
            autotools.make()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", src="src/include", dst="include", keep_path=True)
        self.copy(pattern="*", src="src/bin", dst="bin", keep_path=True)
        self.copy(pattern="*", src="src/plugins", dst="plugins", keep_path=True)
        self.copy(pattern="*", src="src/mkspecs", dst="mkspecs", keep_path=True)
        self.copy(pattern="*", src="src/doc", dst="doc", keep_path=True)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        with open('qt.conf', 'w') as f:
            f.write('[Paths]\nPrefix = ..')
        self.copy("qt.conf", dst="bin")

    def package_info(self):
        include_dir = os.path.join(self._source_subfolder, "include")
        print(include_dir)
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]
