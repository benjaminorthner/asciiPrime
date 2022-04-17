# ------------------------------------------------------------------------------------
#
# define parameters
#
# ------------------------------------------------------------------------------------

# Compiler
CC = gcc

# Path to gmp library (default path alias is -lgmp)
GMP_LINK = -lgmp

# Required for ctypes use in Python
CTYPES_LINK = -shared -fPIC


# ------------------------------------------------------------------------------------
#
# make 
#
# ------------------------------------------------------------------------------------

primify:
	$(CC) -o primify.so primify.c $(GMP_LINK) $(CTYPES_LINK) 