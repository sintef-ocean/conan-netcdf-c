from conans import ConanFile, CMake, tools


class NetcdfConan(ConanFile):
    name = "netcdf"
    version = "4.3.2-rc2-1921dc6687a5eea13936718d5a7aeb9bd04abf0b"
    license = "<Put the package license here>"
    author = "Jarle Ladstein jarle.ladstein@sintef.no"
    url = "https://github.com/Unidata/netcdf-c.git"
    description = "<Description of Netcdf here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    source_subfolder = "netcdf-c"

    _cmake = None

    def requirements(self):
        self.requires("hdf5/1.8.21@sintef/stable")

# Add build requirements: pkgconfig?

    def source(self):
        self.run("git clone --no-checkout https://github.com/Unidata/netcdf-c.git {0}".format(self.source_subfolder))
        self.run("cd {0} && git checkout 1921dc6687a5eea13936718d5a7aeb9bd04abf0b".format(self.source_subfolder))
        tools.replace_in_file("{}/CMakeLists.txt".format(self.source_subfolder),
                "project(netCDF C)",
        '''project(netCDF C)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()''')
        for patch in ["patches/CMakeLists.txt.patch", "patches/liblib_CMakeLists.txt.patch"]:
            tools.patch(patch_file = patch, base_path = self.source_subfolder, strip=1)
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["ENABLE_NETCDF_4"] = True
        self._cmake.definitions["ENABLE_DAP"] = False
        self._cmake.definitions["BUILD_UTILITIES"] = True
        self._cmake.definitions["ENABLE_TESTS"] = False
        self._cmake.definitions["BUILD_SHARED_LIBS"] = False
        self._cmake.definitions["ENABLE_DYNAMIC_LOADING"] = True
        #self._cmake.definitions[""] = 
        self._cmake.configure(source_folder="{0}".format(self.source_subfolder))
        return self._cmake

    def build(self):
        print("{0}".format(self.source_subfolder))
        cmake = self._configure_cmake()
        cmake.build()

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        print("test package")
        #self.copy("*.h", dst="include", src="hello")
        #self.copy("*hello.lib", dst="lib", keep_path=False)
        #self.copy("*.dll", dst="bin", keep_path=False)
        #self.copy("*.so", dst="lib", keep_path=False)
        #self.copy("*.dylib", dst="lib", keep_path=False)
        #self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["netcdf-c"]
        #self.cpp_info.libs = ["hello"]

    def configure(self):
        del self.settings.compiler.libcxx
