"""User interface to help test maya tool code. Will work from within Maya UI as
well as standalone and can be run from an external interpreter such as mayapy.

Example::

Todo:
"""
import os
import sys
path = 'C:/00_git/bpt-artists/src/'
if path not in sys.path:
    sys.path.append(path)

from nw_tools.Qt import QtWidgets, QtGui, QtCore
from nw_tools.ui.tools import get_maya_window, SuperWindow


class Tree(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(Tree, self).__init__(parent)

        self.parent = parent

    def mouseDoubleClickEvent(self, event):
        self.parent.update_system_tree()


class TestCodeUI(SuperWindow):
    # Class constants
    TITLE = 'Maya Unittest Pro - Nick Wolensky, 2017'
    WIDTH = 800
    HEIGHT = 400
    # Should only be applicable if application is run from within Maya
    DOCKABLE = True

    def __init__(self, parent=None):
        super(TestCodeUI, self).__init__(parent)

    def _init_ui(self):
        SuperWindow._init_ui(self)

        self._add_widgets()
        self._add_signals()

    def add_toolbar_items(self):
        SuperWindow.add_toolbar_items(self)
        self.open_dir_action = QtWidgets.QAction('Open...', self)
        self.run_action = QtWidgets.QAction('Run...', self)
        self.stop_action = QtWidgets.QAction('Stop', self)

        for action in [self.open_dir_action,
                       self.run_action,
                       self.stop_action]:
            self.toolbar.addAction(action)

    def _add_widgets(self):
        split = QtWidgets.QSplitter(self.centralWidget())
        split.resize(self.WIDTH, self.HEIGHT)
        split.setHandleWidth(2)

        # Create a tree outliner for package that I want to recursively go
        # through and test | Left Panel
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(QtCore.QDir.currentPath())

        # self.tree = QtWidgets.QTreeView()
        self.tree = Tree(self)
        self.tree.setModel(self.model)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        # Create output section that tests get printed out to | Right Panel
        text_display = QtWidgets.QTextEdit('This is going to be the place '
                                           'where I display output from the '
                                           'unittests')

        split.addWidget(self.tree)
        split.addWidget(text_display)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 2)

    def _add_signals(self):
        # Open command
        self.open_dir_action.triggered.connect(self.update_system_tree)
        # Run command
        self.run_action.triggered.connect(self.get_selected_dir)
        # Stop command
        self.stop_action.triggered.connect(self.dir_up)

    def get_selected_dir(self):
        index = self.tree.currentIndex()
        return self.model.filePath(index)

    def _update_system_tree(self, directory):
        self.tree.setRootIndex(self.model.index(directory))

    def update_system_tree(self):
        self._update_system_tree(self.get_selected_dir())

    def dir_up(self):
        par_dir = os.path.abspath(os.path.join(self.get_selected_dir(),
                                               os.pardir))
        print par_dir
        self._update_system_tree(par_dir)

    def open_file_dialog(self):
        pass

    def dragEnterEvent(self, event):
        pass

    def mouseDoubleClickEvent(self, event):
        print 'hello'
        self.update_system_tree()


if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # Build the UI window. Must keep a reference to the window class or else it
    # goes out of scope
    ui = TestCodeUI()

    sys.exit(app.exec_())
