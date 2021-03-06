#Sample Python File
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

if __name__ == '__main__':
    import os
    import sys

    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.setWidth(500)
    view.setHeight(500)
    view.setTitle('Hello PyQt')
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    view.setSource(QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__),'main.qml')))

    view.show()
    qml_rectangle = view.rootObject()

    sys.exit(app.exec_())