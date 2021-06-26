import curses

def main(stdscr):
    stdscr.refresh()
    win1 = stdscr.derwin(10, 10, 0, 0)
    win1.box()
    win1.refresh()
    win2 = stdscr.derwin(10, 10, 11, 0)
    win2.box()
    win2.refresh()
    win2.mvwin(0, 11)
    win2.refresh()
    stdscr.refresh()
    stdscr.refresh()
    stdscr.getkey()

curses.wrapper(main)
