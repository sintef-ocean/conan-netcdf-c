from os import path
from conan import ConanFile
from conan.tools.files import copy, rm, rmdir
from conan.tools.files import apply_conandata_patches, export_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.scm import Git

required_conan_version = ">=1.54"


class NetcdfConan(ConanFile):
    name = "netcdf"
    version = "4.3.2-rc2-1921dc6687a5eea13936718d5a7aeb9bd04abf0b"
    license = "NetCDF"
    author = "Jarle Ladstein jarle.ladstein@sintef.no"
    url = "https://github.com/Unidata/netcdf-c.git"
    description = "NetCDF is a set of software libraries and self-describing, machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. NetCDF was developed and is maintained at Unidata. Unidata provides data and software tools for use in geoscience education and research. Unidata is part of the University Corporation for Atmospheric Research (UCAR) Community Programs (UCP). Unidata is funded primarily by the National Science Foundation."
    topics = ("conan", "netcdf", "netCDF", "netcdf-c", "data")
    settings = "os", "compiler", "build_type", "arch"
    options = {"fPIC": [True, False], "shared": [True, False]}
    default_options = {"fPIC": True, "shared": False}
    package_type = "library"  # Does have applications, but ok https://github.com/conan-io/conan/pull/12970

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.options["*"].shared = self.options.shared
        if self.settings.os == "Windows":
            self.options["hdf5/*"].shared = False
        self.settings.rm_safe("compiler.libcxx")
        self.settings.rm_safe("compiler.cppstd")
        self.options["hdf5"].threadsafe = True
        self.options["hdf5"].enable_unsupported = True

    def layout(self):
        cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("hdf5/1.8.21", transitive_libs=True)

    def source(self):
        git = Git(self)
        sources = self.conan_data["sources"][self.version]
        git.fetch_commit(sources["url"], sources["commit"])

    def generate(self):
        tc = CMakeToolchain(self)

        tc.variables["ENABLE_NETCDF_4"] = True
        tc.variables["ENABLE_DAP"] = False
        tc.variables["ENABLE_TESTS"] = False
        tc.variables["BUILD_UTILITIES"] = True
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def _patch_sources(self):
        rm(self, "FindZLIB.cmake", path.join(self.source_folder, "cmake", "modules"))
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        copy(self, "COPYRIGHT", self.source_folder, "licenses", keep_path=False)
        rm(self, "nc-config", path.join(self.package_folder, "bin"))
        rm(self, "*.settings", path.join(self.package_folder, "lib"))
        rmdir(self, path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "netCDF")
        self.cpp_info.set_property("cmake_target_name", "netCDF::netcdf")
        self.cpp_info.set_property("pkg_config_name", "netcdf")
        self.runenv_info.prepend_path("PATH", path.join(self.package_folder, "bin"))
        self.cpp_info.libs = ["netcdf"]
