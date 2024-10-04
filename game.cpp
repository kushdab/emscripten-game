#include <emscripten.h>
#include <iostream>
#include <cstdlib>

int x = 50; // Starting x position
int y = 50; // Starting y position

// Function to be called every frame
void render() {
    // Clear the canvas
    printf("clear\n");
    // Drawing a rectangle
    printf("rect %d %d\n", x, y);
    x += rand() % 5; // Move the x position randomly
    y += rand() % 5; // Move the y position randomly
}

int main() {
    // Initialize random seed
    srand(time(0));
    
    // Start rendering loop
    emscripten_set_main_loop(render, 0, 1);
}
