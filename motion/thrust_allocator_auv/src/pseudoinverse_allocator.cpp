#include "thrust_allocator_auv/pseudoinverse_allocator.hpp"

PseudoinverseAllocator::PseudoinverseAllocator(Eigen::MatrixXd T_pinv)
    : T_pinv_(std::move(T_pinv))
{
}

Eigen::VectorXd auto PseudoinverseAllocator::calculate_allocated_thrust(const Eigen::VectorXd& tau) -> Eigen::VectorXd
{
    Eigen::VectorXd u = T_pinv * tau;
    return u;
}
