import os
from conans import ConanFile, tools, CMake


class PyBind11Conan(ConanFile):
    name = "pybind11"
    version = "2.3.0"
    settings = "os", "compiler", "arch", "build_type"
    description = "Seamless operability between C++11 and Python"
    homepage = "https://github.com/pybind/pybind11"
    license = "BSD Style: https://github.com/pybind/pybind11/blob/master/LICENSE"
    url = "https://github.com/conan-community/conan-pybind11"
    no_copy_sources = True

    def source(self):
        tools.get("%s/archive/v%s.tar.gz" % (self.homepage, self.version))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PYBIND11_TEST"] = False
        cmake.configure(source_folder="pybind11-%s" % self.version)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("*LICENSE", keep_path=False)
        os.unlink(os.path.join(self.package_folder, "share", "cmake", "pybind11", "pybind11Config.cmake"))
        os.unlink(os.path.join(self.package_folder, "share", "cmake", "pybind11", "pybind11ConfigVersion.cmake"))
        pybind11tools_path = os.path.join(self.package_folder, "share", "cmake", "pybind11", "pybind11Tools.cmake")
        tools.replace_in_file(pybind11tools_path, "PYBIND11_INCLUDE_DIR", "pybind11_INCLUDE_DIRS")

    def package_info(self):
        base_path = os.path.join("share", "cmake", "pybind11")
        self.cpp_info.builddirs = [base_path]
        self.cpp_info.build_modules = [
            os.path.join(base_path, "pybind11Tools.cmake"),
            os.path.join(base_path, "FindPythonLibsNew.cmake")
        ]

    def package_id(self):
        self.info.header_only()