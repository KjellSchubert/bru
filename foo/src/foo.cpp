#include "foo/foo.h"
#include <iostream>

namespace foo {
    
int foofun(float x) {
    int retval = 7 + static_cast<int>(x);
    std::cout << "foofun returning " << retval << "\n";
    return retval;
}

}