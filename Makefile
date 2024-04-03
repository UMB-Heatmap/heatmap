INC_DIR = include
OBJ_DIR = obj
SRC_DIR = src

INCLUDE = -I$(INC_DIR)

PRE_OBJECTS = $(wildcard $(INC_DIR)/*.cpp)
OBJECTS = $(patsubst $(INC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(PRE_OBJECTS))

prng: $(SRC_DIR)/prng.cpp $(OBJECTS)
	gcc -o prng $(SRC_DIR)/prng.cpp $(OBJECTS) -lstdc++ -std=c++11

$(OBJ_DIR)/%.o: $(INC_DIR)/%.cpp
	mkdir -p $(OBJ_DIR)
	gcc -c $< -o $@ $(INCLUDE)

clean:
	rm prng $(OBJ_DIR)/*.o
