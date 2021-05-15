from conans import ConanFile, CMake, tools
import os


class NetcdfConan(ConanFile):
    name = "netcdf"
    version = "4.3.2-rc2-1921dc6687a5eea13936718d5a7aeb9bd04abf0b"
    license = "NetCDF"
    author = "Jarle Ladstein jarle.ladstein@sintef.no"
    url = "https://github.com/Unidata/netcdf-c.git"
    description = "NetCDF is a set of software libraries and self-describing, machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. NetCDF was developed and is maintained at Unidata. Unidata provides data and software tools for use in geoscience education and research. Unidata is part of the University Corporation for Atmospheric Research (UCAR) Community Programs (UCP). Unidata is funded primarily by the National Science Foundation."
    topics = ("conan", "netcdf", "netCDF", "netcdf-c", "data")
    settings = "os", "compiler", "build_type", "arch"
    options = { "fPIC": [True, False] }
    default_options = { "fPIC": True }
    generators = ["cmake_paths", "cmake_find_package"]
    source_subfolder = "netcdf-c"
    exports = ["patches/*"]

    _cmake = None

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        self.requires("hdf5/1.8.21@")

    def source(self):
        self.run("git clone --no-checkout https://github.com/Unidata/netcdf-c.git {0}".format(self.source_subfolder))
        self.run("cd {0} && git checkout 1921dc6687a5eea13936718d5a7aeb9bd04abf0b".format(self.source_subfolder))
        os.remove("{}/cmake/modules/FindZLIB.cmake".format(self.source_subfolder))
        for patch in os.listdir("patches"):
            tools.patch(patch_file=os.path.join("patches", patch),
                        base_path=self.source_subfolder, strip=1)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["ENABLE_NETCDF_4"] = True
        self._cmake.definitions["ENABLE_DAP"] = False
        self._cmake.definitions["BUILD_UTILITIES"] = True
        self._cmake.definitions["ENABLE_TESTS"] = False
        self._cmake.definitions["BUILD_SHARED_LIBS"] = False
        #self._cmake.definitions["ENABLE_DYNAMIC_LOADING"] = True
        self._cmake.definitions["BUILD_SHARED_LIBS"] = False
        #self._cmake.definitions[""] =
        if self.settings.os != 'Windows':
            self._cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        self._cmake.configure(source_folder=self.source_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("COPYRIGHT", dst="licenses",
                  src=self.source_subfolder, keep_path=False)
        #self.copy("*.h", dst="include", src="hello")
        #self.copy("*hello.lib", dst="lib", keep_path=False)
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["netcdf"]
