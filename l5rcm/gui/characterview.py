#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Daniele Simonetti

import sys

from OpenGL import GL
from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml  import qmlRegisterType, QQmlComponent, QQmlEngine

if __name__ == '__main__':
	# Create the application instance.
	app = QGuiApplication(sys.argv)

	view = QQuickView()
	view.setSource(QUrl.fromLocalFile("main.qml"));
	view.show();

	try:
		app.exec_()
	except KeyboardInterrupt:
		app.exit(0)



