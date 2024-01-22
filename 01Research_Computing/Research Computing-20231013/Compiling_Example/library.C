#include <cblas.h>
#include "library.H"
#include <cmath>
#include <limits>

// Solve the equation ax + b = 0
double linear_solve(double a, double b)
{
  return -b/a;
}

// Solve the equation a*x*x + b*x + c = 0
// Return the smaller of the real roots.
// If there are no real roots, return infinity.
double quadratic_solve(double a, double b, double c)
{
  double disc = b*b-4*a*c;
  if(disc < 0)
  {
    return std::numeric_limits<double>::infinity();
  }
  else
  {
    return (-b - sqrt(b*b-4*a*c) )/(2*a);
  }
}

std::array<double, 4> daxpy4(const double alpha, const std::array<double, 4>& x, const std::array<double, 4>& y)
{
  std::array<double, 4> z = y;
  cblas_daxpy(4, alpha, &x[0], 1, &z[0], 1);
  return z;
}
