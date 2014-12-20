#include "foo/foo.h"
#include "gtest/gtest.h" // from module googletest

TEST(FooTest, test1) {
    EXPECT_EQ(foo::bar, 42); // from foo.h
}

TEST(FooTest, test2) {
    EXPECT_EQ(foo::foofun(2), 9);
}
