"""User interface to help test maya tool code. Will work from within Maya UI as
well as standalone and can be run from an external interpreter such as mayapy.

Example::

Todo:
"""
import sys
from nw_tools.Qt import QtWidgets, QtGui, QtCore
from nw_tools.ui.tools import get_maya_window, SuperWindow


class TestCodeUI(SuperWindow):
    # Class constants
    TITLE = 'Maya Unittest Pro - Nick Wolensky, 2017'
    WIDTH = 800
    HEIGHT = 400
    DOCKABLE = True  # Should only be applicable if application is run from within Maya

    def __init__(self, parent=None):
        super(TestCodeUI, self).__init__(parent)

    def add_toolbar_items(self):
        SuperWindow.add_toolbar_items(self)
        open_dir_action = QtWidgets.QAction('Open...', self)
        run_action = QtWidgets.QAction('Run...', self)
        stop_action = QtWidgets.QAction('Stop', self)

        for action in [open_dir_action, run_action, stop_action]:
            self.toolbar.addAction(action)

    def _create(self):
        SuperWindow._create(self)

        hbox = QtWidgets.QHBoxLayout(self.centralWidget())

        # label = QtWidgets.QLabel('Test Label')
        #
        # hbox.addWidget(label)

        # Create a tree outliner for package that I want to recursively go
        # through and test | Left Panel
        model = QtWidgets.QFileSystemModel()
        model.setRootPath(QtCore.QDir.currentPath())

        tree = QtWidgets.QTreeView()
        tree.setModel(model)

        # Create output section that tests get printed out to | Right Panel
        text_display = QtWidgets.QTextEdit('This is going to be the place '
                                           'where I display output from the '
                                           'unittests')

        hbox.addWidget(tree)
        hbox.addWidget(text_display)


if __name__ == '__main__':
    # Create the Qt Application
    app = QtWidgets.QApplication(sys.argv)

    # Build the UI window. Must keep a reference to the window class or else it
    # goes out of scope
    ui = TestCodeUI()
    ui.show()

    sys.exit(app.exec_())
