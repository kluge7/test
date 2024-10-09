#include "thrust_allocator_auv/thrust_allocator_ros.hpp"
#include "thrust_allocator_auv/thrust_allocator_utils.hpp"

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);

  // Intentional clang-tidy issues
  auto allocator = new ThrustAllocator(); // Use of raw pointer instead of smart pointer

  RCLCPP_INFO(allocator->get_logger(), "Thrust allocator initiated");

  // Unused variable
  int unused_variable = 42;

  // Use of strcpy (unsafe function, should trigger clang-tidy)
  char message[50];
  strcpy(message, "Clang-Tidy Test");

  rclcpp::spin(std::shared_ptr<rclcpp::Node>(allocator)); // Incorrect use of smart pointer
  rclcpp::shutdown();
  return 0;
}
