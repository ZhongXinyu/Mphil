#include "library.H"
#include <iostream>

int main()
{
  double a = 9;
  double b = 7;
  
  std::cout << "Solution of linear equation " << a << "x + " << b << " = 0 is:" << std::endl;

  double c = linear_solve(a,b);
  std::cout << "x = " << c << std::endl;

  std::array<double,4> f{2,5,8,9};
  std::array<double,4> g{9,1,0,2};

  std::cout << "Now, " << c << "*( " << f[0] << "," << f[1] << "," << f[2] << "," << f[3] << " ) +";
  std::cout << "( " << g[0] << "," << g[1] << "," << g[2] << "," << g[3] << " )" << std::endl;
  
  const auto h = daxpy4(c, f, g);
  std::cout << " = (" << h[0] << "," << h[1] << "," << h[2] << "," << h[3] << ")" << std::endl;

  return 0;
}
