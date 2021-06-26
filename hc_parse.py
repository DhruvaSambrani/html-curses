import xml.etree.ElementTree as ET
import curses


class HCDiv:
    def __init__(self, _id, orientation, weight, children=None, attr=None):
        self.id = _id
        self.orientation = orientation
        self.weight = weight
        self.parent = None
        self.window = None
        self.children = [] if children is None else children
        self.attr = {} if attr is None else attr

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def isDiv(self):
        return True

    def isPara(self):
        return False

    def _make_window(self):
        parwin = self.parent.window
        parorient = self.parent.orientation
        parenty, parentx = self.parent.window.getmaxyx()
        width, height = 0, 0
        if parorient == 'V':
            width = self.weight // self.parent._inner_weight() * parentx
            height = parenty
        else:
            width = parentx
            height = self.weight // self.parent._inner_weight() * parenty
        self.window = self.parent.window.derwin(height, width, 0, 0)

    def _inner_weight(self):
        return sum(c.weight for c in self.children)

    def _place_child(self, childidx):
        weight_till_now = sum(
            child.weight for child in self.children[:childidx])
        if self.orientation == 'V':
            startx = (weight_till_now * self.window.getmaxyx()
                      [1]) // self._inner_weight()+childidx
            starty = 0
        else:
            startx = 0
            starty = (weight_till_now * (self.window.getmaxyx()
                      [0])) // self._inner_weight() + childidx
        #if childidx == 1:
        #    raise Exception(str(startx)+str(starty))
        self.children[childidx].window.mvwin(starty, startx)

    def draw(self):
        self._make_window()
        for i in range(len(self.children)):
            self.children[i].draw()
            self._place_child(i)
        self.window.refresh()

    def siblings(self):
        return self.parent.children

    def refresh(self):
        for child in self.children:
            child.refresh()
        self.window.refresh()

class HCParagraph:
    def __init__(self, _id, content, weight):
        self.content = content
        self.id = _id
        self.weight = weight
        self.parent = None
        self.window = None

    def isDiv(self):
        return False

    def isPara(self):
        return True

    def _make_window(self):
        parwin = self.parent.window
        parorient = self.parent.orientation
        parenty, parentx = self.parent.window.getmaxyx()
        if parorient == 'V':
            width = (self.weight * parentx) // self.parent._inner_weight()
            height = parenty
        else:
            width = parentx
            height = (self.weight * parenty) // self.parent._inner_weight()
        #raise Exception(width, height)
        self.window = self.parent.window.derwin(height, width, 0, 0)

    def draw(self):
        self._make_window()
        self.window.addstr(self.content)
        #self.window.box()

    def refresh(self):
        self.window.refresh()

__screen = None


def init(stdscr):
    global __screen
    __screen = HCDiv("__screen", "V", 0)
    __screen.window = stdscr


def parse_to_dom(xmldict):
    if xmldict.tag == 'div' or xmldict.tag == 'hcml':
        obj = HCDiv(
            xmldict.attrib['id'],
            xmldict.attrib['orientation'],
            xmldict.attrib.get(
                'weight',
                1))
        children = [parse_to_dom(child) for child in xmldict]
        for child_dom in children:
            obj.addChild(child_dom)
        return obj
    elif xmldict.tag == 'p':
        return HCParagraph(
            xmldict.attrib['id'],
            xmldict.text,
            xmldict.attrib.get(
                'weight',
                1))
    else:
        raise ValueError(xmldict.tag + " not understood!")


def parse(text):
    xmlroot = ET.fromstring(text)
    assert xmlroot.tag == 'hcml'
    domroot = parse_to_dom(xmlroot)
    __screen.addChild(domroot)
    return domroot


def parse_file(fd):
    xmlstr = ""
    with open(fd) as f:
        xmlstr = f.read()
    return parse(xmlstr)
