/****************************************************
 ***** CONSTANTS
 ***************************************************/

#define BOOLEAN_SIZE 1
#define CHAR_SIZE 1
#define UNSIGNED_CHAR_SIZE 1
#define INT_SIZE 4
#define UNSIGNED_INT_SIZE 4
#define LONG_SIZE 4
#define UNSIGNED_LONG_SIZE 4
#define SHORT_SIZE 2
#define FLOAT_SIZE 4
#define DOUBLE_SIZE 8


/****************************************************
 ***** DECLARES ALL THE NECESSARY UNIONS
 ***************************************************/

union boolean_union {
    uint8_t b[BOOLEAN_SIZE];
    boolean v; //care with 'v'
};

union char_union {
    uint8_t b[CHAR_SIZE];
    char c;
};

union unsigned_char_union {
    uint8_t b[UNSIGNED_CHAR_SIZE];
    unsigned char uc;
};

union int_union {
    uint8_t b[INT_SIZE];
    int i;
};

union unsigned_int_union {
    uint8_t b[UNSIGNED_INT_SIZE];
    unsigned int ui;
};

union long_union {
    uint8_t b[LONG_SIZE];
    long l;
};

union unsigned_long_union {
    uint8_t b[UNSIGNED_LONG_SIZE];
    unsigned long ul;
};

union short_union {
    uint8_t b[SHORT_SIZE];
    short s;
};

union float_union {
    uint8_t b[FLOAT_SIZE];
    float f;
};

union double_union {
    uint8_t b[DOUBLE_SIZE];
    double d;
};
