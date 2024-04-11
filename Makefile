INC_DIR = include
OBJ_DIR = obj
SRC_DIR = src
CFLAGS = -std=c++11 -I$(INC_DIR)

TARGET = prng

PRE_OBJECTS = $(filter-out $(SRC_DIR)/$(TARGET).cpp,$(wildcard $(SRC_DIR)/*.cpp)) 
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(OBJ_DIR)/%.o,$(PRE_OBJECTS))
HEADERS = $(wildcard $(INC_DIR)/*.h)

$(TARGET): $(SRC_DIR)/$(TARGET).cpp $(OBJECTS) $(HEADERS)
	gcc -o $(TARGET) $(SRC_DIR)/$(TARGET).cpp $(OBJECTS) $(CFLAGS) -lstdc++

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	mkdir -p $(OBJ_DIR)
	gcc -c $< -o $@ $(CFLAGS)

clean:
	rm $(TARGET) $(OBJ_DIR)/*.o