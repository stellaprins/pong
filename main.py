from pong.states import Game
import pygame
import asyncio

async def main():
    Game().run()
    pygame.quit()
    await asyncio.sleep(0)
    

asyncio.run(main())
    
