cmake_minimum_required(VERSION 3.13)
project(PackageTest CXX)

find_package(netCDF REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example netCDF::netcdf)
