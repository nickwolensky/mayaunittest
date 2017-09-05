"""Helper functions for window creation in my toolset. I am going to want to
have some windows function from outside of Maya while others will work natively
from within Maya. An example of a window that will hopefully function in both
domains is my TestCodeUI class.

Example::

Todo:
    - Add functions that can be used to create a default set of menus at the
      top of my custom windows. I will want to at least create a helper menu
      that includes an about section with my info and a link to my
      documentation that I will eventually create using Sphinx.
"""
try:
    import maya.OpenMayaUI as OpenMayaUI
    from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
except ImportError:
    print 'Starting up from a session outside of Autodesk Maya.'
# from shiboken import wrapInstance
from nw_tools.Qt import QtWidgets, QtGui, QtCore
from nw_tools.Qt import c_binding

wrapInstance = c_binding.wrapInstance


def get_maya_window():
    """Find the open maya window application. This allows the newly
    created window to always sit on top of the application even when
    focus is changed.
    """
    maya_win_ptr = OpenMayaUI.MQtUtil.mainWindow()
    if maya_win_ptr is None:
        raise RuntimeError('No Maya window found.\n')
    maya_win = wrapInstance(long(maya_win_ptr), QtWidgets.QMainWindow)

    assert isinstance(maya_win, QtWidgets.QMainWindow)

    return maya_win


try:  # A switch to figure out which BaseWindow class to create
    class _BaseWindow(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):
        """BaseWindow inheriting from the MayaQWidgetDockableMixin class. This
        is only created if being run from within a Maya GUI session (or maybe
        from within maya.standalone)
        """

        MAYA2014 = 201400
        MAYA2015 = 201500
        MAYA2016 = 201600
        MAYA2016_5 = 201650
        MAYA2017 = 201700
        MAYA2018 = 201800

        def __init__(self, *args, **kwargs):
            super(_BaseWindow, self).__init__(*args, **kwargs)

except NameError:
    class _BaseWindow(QtWidgets.QMainWindow):
        """BaseWindow created if being run from within an external interpreter.
        """
        def __init__(self, *args, **kwargs):
            super(_BaseWindow, self).__init__(*args, **kwargs)


class SuperWindow(_BaseWindow):
    """Super class of a window. This can be inherited from all of my custom
    user interfaces to give them similar functionality when it comes to
    interacting with Maya or being run from an external interpreter. When
    creating a new window, inherit from this class rather than the BaseWindow
    class.

    Args:
        parent (QtWidget): A main window to make this a child of
            In the case of Maya, the Maya UI
    """
    TITLE = 'This is a testing window!'
    WIDTH = 500
    HEIGHT = 500
    DOCKABLE = True

    def __init__(self, *args, **kwargs):
        super(SuperWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle(self.TITLE)
        self.resize(self.WIDTH, self.HEIGHT)
        self.centered()

        # Create the menubar for the window
        menubar = QtWidgets.QMenuBar()
        self.setMenuBar(menubar)

        # Create the toolbar for the window
        self.toolbar = QtWidgets.QToolBar()
        self.addToolBar(self.toolbar)

        widg = QtWidgets.QWidget()
        self.setCentralWidget(widg)

        # Run the creation method
        self._create()

    def centered(self):
        """Center the widget in the center of the screen."""
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def floatingChanged(self, isFloating):
        """Force focus on window."""
        self.setFocus()

    def add_menu_items(self):
        # Top Help menu
        help_menu = QtWidgets.QMenu('&Help')
        self.menuBar().addMenu(help_menu)
        # Child Actions
        about_action = QtWidgets.QAction('&About', self)
        docs_action = QtWidgets.QAction('&Documenation...', self)
        # Add the actions
        for action in [about_action, docs_action]:
            help_menu.addAction(action)

    def add_toolbar_items(self):
        pass

    def _create(self):
        # Set the default menubar
        self.add_menu_items()
        self.add_toolbar_items()

        # # Use this method to show the user interface as well
        # self.show()

    def destroy(self):
        QtWidgets.QMainWindow.destroy(self)
