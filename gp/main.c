
// https://www.youtube.com/watch?v=iL--xqGgd0g
// https://www.youtube.com/watch?v=2YSztlmgpks
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <SDL2/SDL.h>

#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 600

#define BOARD_WIDTH 10
#define BOARD_HEIGHT 10

#define CELL_WIDTH ((float)SCREEN_WIDTH / BOARD_WIDTH)
#define CELL_HEIGHT ((float)SCREEN_HEIGHT / BOARD_HEIGHT)

int scc(int code) {
  if (code < 0) {
    fprintf(stderr, "SDL err:%s\n", SDL_GetError());
    exit(EXIT_FAILURE);
  }

  return code;
}

void *scp(void *ptr) {
  if (!ptr) {
    fprintf(stderr, "SDL err:%s\n", SDL_GetError());
    exit(EXIT_FAILURE);
  }

  return ptr;
}

void render_board_grid(SDL_Window *window, SDL_Renderer *renderer) {
  for (int x = 1; x <= BOARD_WIDTH; ++x) {
    scc(SDL_SetRenderDrawColor(renderer, 60, 60, 60, 255));
    scc(SDL_RenderDrawLine(renderer, x * CELL_WIDTH, 0, x * CELL_WIDTH,
                           SCREEN_WIDTH));
  }
  for (int y = 1; y <= BOARD_HEIGHT; ++y) {
    scc(SDL_SetRenderDrawColor(renderer, 60, 60, 60, 255));
    scc(SDL_RenderDrawLine(renderer, 0, y * CELL_HEIGHT, SCREEN_WIDTH,
                           y * CELL_HEIGHT));
  }
}

int main(int argc, char **argv) {
  if (SDL_Init(SDL_INIT_VIDEO) < 0) {
    printf("SDL Error: %s.\n", SDL_GetError());
    exit(EXIT_FAILURE);
  }

  SDL_Window *const window = scp(SDL_CreateWindow(
      "hunger", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_RESIZABLE));

  SDL_Renderer *const renderer =
      scp(SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED));

  scc(SDL_RenderSetLogicalSize(renderer, SCREEN_WIDTH, SCREEN_HEIGHT));

  int quit = 0;
  while (!quit) {
    SDL_Event event;
    while (SDL_PollEvent(&event)) {
      switch (event.type) {
      case SDL_QUIT: {
        quit = 1;
      } break;
      }
    }

    scc(SDL_SetRenderDrawColor(renderer, 30, 30, 30, 255));
    scc(SDL_RenderClear(renderer));

    render_board_grid(window, renderer);

    SDL_RenderPresent(renderer);
  }

  SDL_Quit();
  return 0;
}
