/* Export functions here */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>



/* Function pointers to hold the value of the glibc functions */
static  ssize_t (*real_write)(int fd, const void *buf, size_t count) = NULL;
static  ssize_t (*real_read)(int fd, const void *buf, size_t count) = NULL;

/* wrapping write function call */
ssize_t write(int fd, const void *buf, size_t count)
{

    /* printing out the number of characters */
    //printf("write:chars#:%lu\n", count);
    /* reslove the real write function from glibc
     * and pass the arguments.
     */
    real_write = dlsym(RTLD_NEXT, "write");
    real_write(fd, buf, count);

}

ssize_t read(int fd, const void *buf, size_t count)
{
    /* printing out the number of characters */
    //printf("read:chars#:%lu\n", count);
    /* reslove the real write function from glibc
     * and pass the arguments.
     */
    real_read = dlsym(RTLD_NEXT, "read");
    real_read(fd, buf, count);

}
