CC = g++
CFLAGS = -Iinclude -Wall -Wextra -std=c++11
SRC = solver.cpp
OBJ = $(SRC:.cpp=.o)
TARGET = solver

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) -o $@ $^

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(TARGET)