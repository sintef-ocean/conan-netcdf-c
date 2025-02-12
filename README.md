[![Linux GCC](https://github.com/sintef-ocean/conan-netcdf-c/workflows/Linux%20GCC/badge.svg)](https://github.com/sintef-ocean/conan-netcdf-c/actions?query=workflow%3A"Linux+GCC")
[![Windows MSVC](https://github.com/sintef-ocean/conan-netcdf-c/workflows/Windows%20MSVC/badge.svg)](https://github.com/sintef-ocean/conan-netcdf-c/actions?query=workflow%3A"Windows+MSVC")

[Conan.io](https://conan.io) recipe for [netCDF](https://www.unidata.ucar.edu/software/netcdf).

## How to use this package

1. Add remote to conan's package [remotes](https://docs.conan.io/2/reference/commands/remote.html)

   ```bash
   $ conan remote add sintef https://package.smd.sintef.no
   ```

2. Using [*conanfile.txt*](https://docs.conan.io/2/reference/conanfile_txt.html) and *cmake* in your project.

   Add *conanfile.txt*:
   ```
   [requires]
   netcdf/4.3.2-rc2-1921dc6687a5eea13936718d5a7aeb9bd04abf0b@sintef/stable

   [tool_requires]
   cmake/[>=3.25.0]

   [options]

   [layout]
   cmake_layout

   [generators]
   CMakeDeps
   CMakeToolchain
   VirtualBuildEnv
   ```
   Insert into your *CMakeLists.txt* something like the following lines:
   ```cmake
   cmake_minimum_required(VERSION 3.15)
   project(TheProject CXX)

   find_package(netCDF REQUIRED)

   add_executable(the_executor code.cpp)
   target_link_libraries(the_executor netCDF::netcdf)
   ```
   Install and build e.g. a Release configuration:
   ```bash
   $ conan install . -s build_type=Release -pr:b=default
   $ source build/Release/generators/conanbuild.sh
   $ cmake --preset conan-release
   $ cmake --build build/Release
   $ source build/Release/generators/deactivate_conanbuild.sh
   ```

## Package options

Option | Default | Domain
-------|---------|--------------
fPIC   | True    | [True, False]

## Known recipe issues

(Add known issues/shortcomings here)
