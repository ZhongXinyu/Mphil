#include "library.H"
#include <iostream>

int main()
{
  double a = 2;
  double b = 7;
  double c = 3;
  
  std::cout << "Solution of quadratic equation " << a << "x^2 + " << b << "x + " << c << " = 0 is:" << std::endl;

  double d = quadratic_solve(a,b,c);
  std::cout << "x = " << d << std::endl;

  std::array<double,4> f{2,3,8,5};
  std::array<double,4> g{7,1,0,6};

  std::cout << "Now, " << d << "*( " << f[0] << "," << f[1] << "," << f[2] << "," << f[3] << " ) +";
  std::cout << "( " << g[0] << "," << g[1] << "," << g[2] << "," << g[3] << " )" << std::endl;
  
  const auto h = daxpy4(c, f, g);
  std::cout << " = (" << h[0] << "," << h[1] << "," << h[2] << "," << h[3] << ")" << std::endl;

  return 0;
}
