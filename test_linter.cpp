#include <iostream>
#include <vector>

const int MAX_SIZE = 10; // Magic number example

void TestFunction(int a, int b) {
  int result = 0; // Unused variable (could be flagged by clang-tidy)
  if(a>b) { 
    std::cout << "a is greater than b"; 
  }
  else { 
    std::cout << "b is greater than or equal to a"; 
  }

  if (a = b) { // Assignment instead of comparison (potential bug)
    std::cout << "a is equal to b"; 
  }

  for (int i = 0; i < MAX_SIZE; i++) { // Loop without braces (could be flagged for readability)
    std::cout << i;
  }
}

int main() {
 std::vector<int> vec;
 vec.push_back(1);  
 vec.push_back(2);  
 vec.push_back(3);  // Magic numbers

 for(int i = 0; i < vec.size(); ++i) // Missing braces for loop (bad practice)
   std::cout << vec[i] << std::endl;

 for(int i = 0; i < vec.size(); i++) { // ++i preferred over i++ for performance
   std::cout << vec[i] << std::endl; 
 }

 return 0;  // Incorrect indentation
}
