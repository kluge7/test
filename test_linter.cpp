#include <iostream>
#include <vector>
 
void TestFunction(int a, int b) {
  if(a>b) { std::cout << "a is greater than b"; }
  else
  {std::cout << "b is greater than or equal to a";}
}
 
int main() {
 std::vector<int> vec;
 vec.push_back(1);  vec.push_back(2);  vec.push_back(3); // Incorrect formatting (extra spaces on the same line)

 for(int i = 0; i < vec.size(); ++i) // Missing braces for loop
   std::cout << vec[i] << std::endl; 

   return 0;  // Incorrect indentation
}
