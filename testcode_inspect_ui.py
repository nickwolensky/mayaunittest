"""User interface to help test maya tool code. Will work from within Maya UI as
well as standalone and can be run from an external interpreter such as mayapy.

Example::

Todo:
"""
import os
import sys
# path = 'C:/00_git/bpt-artists/src/'
# if path not in sys.path:
#     sys.path.append(path)

from nw_tools.Qt import QtWidgets, QtGui, QtCore
from nw_tools.ui.tools import get_maya_window, SuperWindow


class Tree(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(Tree, self).__init__(parent)

        self.parent = parent
        self.create_actions()

    def create_actions(self):
        self.walk_up_action = QtWidgets.QAction('Walk up directory', self)
        self.walk_up_action.triggered.connect(self.parent.walk_up)

    def mouseDoubleClickEvent(self, event):
        self.parent.walk_down()

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction(self.walk_up_action)
        menu.exec_(event.globalPos())


class TestCodeUI(SuperWindow):
    # Class constants
    TITLE = 'Maya Unittest Pro - Nick Wolensky, 2017'
    WIDTH = 800
    HEIGHT = 400
    # Should only be applicable if application is run from within Maya
    DOCKABLE = True

    def __init__(self, parent=None):
        self.current_dir = QtCore.QDir.rootPath()
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
        split.setHandleWidth(3)
        split.setContentsMargins(2, 2, 2, 2)

        btn_widg = QtWidgets.QWidget()
        vbox = QtWidgets.QVBoxLayout()
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setContentsMargins(0, 0, 0, 0)
        btn_widg.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 2, 0)

        # Create a tree outliner for package that I want to recursively go
        # through and test | Left Panel
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(self.current_dir)

        self.tree = Tree(self)
        self.tree.setModel(self.model)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        self._update_system_tree(self.current_dir)

        # Create output section that tests get printed out to | Right Panel
        text_display = QtWidgets.QTextEdit('This is going to be the place '
                                           'where I display output from the '
                                           'unittests')

        self.btn = QtWidgets.QPushButton('^')
        self.btn.setFixedWidth(25)
        btn_row.addWidget(self.btn)
        btn_row.addStretch(0)
        vbox.addLayout(btn_row)
        vbox.addWidget(self.tree)

        split.addWidget(btn_widg)
        split.addWidget(text_display)
        split.setStretchFactor(0, 0)
        split.setStretchFactor(1, 2)

    def _add_signals(self):
        # Open command
        # self.open_dir_action.triggered.connect(self.update_system_tree)
        # Run command
        self.run_action.triggered.connect(self.get_selected_dir)
        # Stop command
        # self.stop_action.triggered.connect(self.dir_up)

        # Move up button
        self.btn.clicked.connect(self.walk_up)

    def get_selected_dir(self):
        index = self.tree.currentIndex()
        return self.model.filePath(index)

    def _update_system_tree(self, directory):
        self.tree.setRootIndex(self.model.index(directory))
        self.current_dir = directory

    def walk_up(self):
        par_dir = os.path.abspath(os.path.join(self.current_dir, os.pardir))
        self._update_system_tree(par_dir)

    def walk_down(self):
        self._update_system_tree(self.get_selected_dir())

    def open_file_dialog(self):
        pass

    def dragEnterEvent(self, event):
        pass


if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # Build the UI window. Must keep a reference to the window class or else it
    # goes out of scope
    ui = TestCodeUI()

    sys.exit(app.exec_())
