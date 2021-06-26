import hc_parse
import curses

def main(stdscr):
    stdscr.refresh()
    hc_parse.init(stdscr)
    dom = hc_parse.parse_file("test.hcml")
    dom.draw()
    dom.refresh()
    stdscr.refresh()
    stdscr.getch()
    
curses.wrapper(main)
