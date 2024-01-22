#include <string>
using namespace std;

class MyClass {       // The class
    public:             // Access specifier
        int mmyNum;        // Attribute (int variable)
        string mmyString;  // Attribute (string variable)
        MyClass (int myNum, string myString, string myExtra){
            mmyNum = myNum;
            mmyString = myString;
        };

        float GetNum()
        {
            return (float)mmyNum;
        }
};

float inttofloat(int x)
{
    MyClass m = MyClass (x, "a", "eta");
    return m.GetNum();
};