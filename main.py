import bot
import time
import win32gui
import pyautogui as pg
import copy

sizex = 18
sizey = 14

def get_window(name):
    windows = []
    def add(hwnd, params):
        windows.append(hwnd)

    win32gui.EnumWindows(add, windows)
    for window in windows:
        if name in win32gui.GetWindowText(window):
            return window
    return None


def main():
    window = get_window("minesweeper")
    if window is None:
        print("Minesweeper window not found")
        return

    gamebot = bot.MineSweeperBot(sizex, sizey)
    win32gui.SetForegroundWindow(window)
    prev = []
    while True:
        time.sleep(0.5)
        pg.click(943, 595)
        time.sleep(0.5)
        stuck = 0
        while not gamebot.agent.gameOver:
            delta = time.time() - gamebot.agent.lastUpdate
            if delta < 0.5:
                time.sleep(0.5-delta)
            #("Getting Board")
            pg.moveTo(963, 315)
            gamebot.agent.get_board()
            while gamebot.next_move():
                pass
            if prev != gamebot.agent.opened:
                prev = copy.deepcopy(gamebot.agent.opened)
                stuck = 0
            if not gamebot.queue:
                gamebot.fill_queue()
                stuck += 1
                if stuck > 4:
                    gamebot.agent.gameOver = True
                elif stuck > 1:
                    print("Guessing")
                    gamebot.probability_guess()
            if gamebot.agent.mines == 0:
                gamebot.finish()
                gamebot.agent.gameOver = True

        gamebot.reset()
        time.sleep(0.5)
        pg.press('r')

if __name__ == "__main__":
    main()