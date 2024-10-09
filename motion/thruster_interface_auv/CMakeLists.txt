cmake_minimum_required(VERSION 3.8)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(thruster_interface_auv)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(vortex_msgs REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  find_package(ament_clang_tidy REQUIRED)

  # Enable Clang-Tidy and other linters
  ament_lint_auto_find_test_dependencies()

  # Configure Clang-Tidy to use .clang-tidy file in the source directory
  ament_clang_tidy(SETTINGS_FILE ${CMAKE_SOURCE_DIR}/.clang-tidy)
endif()

ament_python_install_package(thruster_interface_auv)

install(DIRECTORY
  launch
  resources
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  thruster_interface_auv/thruster_interface_auv_node.py
  thruster_interface_auv/thruster_interface_auv_driver_lib.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
