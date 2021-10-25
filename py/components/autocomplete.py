from .textfield import *
from .flatbutton import *


class QtMaterialAutoCompleteStateMachine(QStateMachine):

    shouldOpen = Signal()
    shouldClose = Signal()
    shouldFade = Signal()

    def __init__(self, menu: QWidget):
        QStateMachine.__init__(self, menu)

        self.m_menu = QWidget(menu)
        self.m_closedState = QState()
        self.m_openState = QState()
        self.m_closingState = QState()

        assert menu

        self.addState(self.m_closedState)
        self.addState(self.m_openState)
        self.addState(self.m_closingState)
        self.setInitialState(self.m_closedState)

        transition = QSignalTransition()

        transition = QSignalTransition(self, self.shouldOpen)
        transition.setTargetState(self.m_openState)
        self.m_closedState.addTransition(transition)

        transition = QSignalTransition(self, self.shouldClose)
        transition.setTargetState(self.m_closedState)
        self.m_openState.addTransition(transition)

        transition = QSignalTransition(self, self.shouldFade)
        transition.setTargetState(self.m_closingState)
        self.m_openState.addTransition(transition)

        self.m_closedState.assignProperty(menu, "_visible", false)
        self.m_openState.assignProperty(menu, "_visible", true)

        effect = QGraphicsOpacityEffect()
        menu.setGraphicsEffect(effect)

        self.m_openState.assignProperty(effect, "opacity", 1)
        self.m_closingState.assignProperty(effect, "opacity", 0)
        self.m_closedState.assignProperty(effect, "opacity", 0)

        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(240)
        self.addDefaultAnimation(animation)

        transition = QSignalTransition(self, self.finished)
        transition.setTargetState(self.m_closedState)
        self.m_closingState.addTransition(transition)


class QtMaterialAutoComplete:
    ...


class QtMaterialAutoCompletePrivate(QtMaterialTextFieldPrivate):
    def __init__(self, q: QtMaterialAutoComplete):
        self.q: QtMaterialAutoComplete = q
        self.menu: QWidget = QWidget()
        self.frame: QWidget = QWidget()
        self.stateMachine: QtMaterialAutoCompleteStateMachine = None
        self.menuLayout: QVBoxLayout = QVBoxLayout()
        self.dataSource: QStringList = QStringList()
        self.maxWidth = 0

        QtMaterialTextFieldPrivate.__init__(self, q)

    def init(self) -> None:

        self.stateMachine = QtMaterialAutoCompleteStateMachine(self.menu)

        self.menu.setParent(self.q.parentWidget())
        self.frame.setParent(self.q.parentWidget())

        self.menu.installEventFilter(self.q)
        self.frame.installEventFilter(self.q)

        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(11)
        effect.setColor(QColor(0, 0, 0, 50))
        effect.setOffset(0, 3)

        self.frame.setGraphicsEffect(effect)
        self.frame.setVisible(false)

        self.menu.setLayout(self.menuLayout)
        self.menu.setVisible(false)
        self.menu.setStyleSheet('background:blue;')

        self.menuLayout.setContentsMargins(0, 0, 0, 0)
        self.menuLayout.setSpacing(0)

        self.q.textEdited.connect(self.q.updateResults)

        self.stateMachine.start()


class QtMaterialAutoComplete(QtMaterialTextField):
    itemSelected = Signal(QString)

    def __init__(self, parent: QWidget = None):
        QtMaterialTextField.__init__(self, parent=parent, p=0)
        self.d = QtMaterialAutoCompletePrivate(self)
        self.d.init()

    def setDataSource(self, data: QStringList) -> None:
        self.d.dataSource = data
        self.update()

    def updateResults(self, text: QString) -> None:

        results = QStringList()
        trimmed = QString(text.strip())

        if not trimmed.isEmpty():
            lookup = QString(trimmed.toLower())
            for i in self.d.dataSource:
                if lookup in i:
                    results.push_back(i)
        
        diff: int = results.length() - self.d.menuLayout.count()
        
        font = QFont("Roboto", 12, QFont.Normal)

        if diff > 0:
            for c in range(diff):
                item = QtMaterialFlatButton()
                item.setFont(font)
                item.setTextAlignment(Qt.AlignLeft)
                item.setCornerRadius(0)
                item.setHaloVisible(false)
                item.setFixedHeight(50)
                item.setOverlayStyle(Material.TintedOverlay)
                self.d.menuLayout.addWidget(item)
                item.installEventFilter(self)

        elif diff < 0:
            for c in range(-diff):
                widget: QWidget = self.d.menuLayout.itemAt(0).widget()
                if widget:
                    self.d.menuLayout.removeWidget(widget)
                    del widget

        fm = QFontMetrics(font)
        self.d.maxWidth = 0

        for i in range(results.count()):
            item = self.d.menuLayout.itemAt(i).widget()
            if isinstance(item, QtMaterialFlatButton):
                text: QString = results[i]
                rect: QRect = fm.boundingRect(text)
                self.d.maxWidth = max(self.d.maxWidth, rect.width())
                item.setText(text)

        if not results.count():
            self.d.stateMachine.shouldClose.emit()
        else:
            self.d.stateMachine.shouldOpen.emit()

        self.d.menu.setFixedHeight(results.length() * 50)
        self.d.menu.setFixedWidth(max(self.d.maxWidth + 24, self.width()))
        self.d.menu.update()
        self.d.menu.setVisible(true)

    def event(self, event: QEvent) -> bool:
        e = event.type()
        if e in [QEvent.Move, QEvent.Resize]:
            self.d.menu.move(self.pos() + QPoint(0, self.height() + 6))

        elif e == QEvent.ParentChange:
            widget: QWidget = self.parent()

            if widget:
                self.d.menu.setParent(widget)
                self.d.frame.setParent(widget)

        return QtMaterialTextField.event(self, event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        e = event.type()
        if self.d.frame == watched:
            if e == QEvent.Paint:
                painter = QPainter(self.d.frame)
                painter.fillRect(self.d.frame.rect(), Qt.white)

        elif self.d.menu == watched:

            if e in [QEvent.Resize, QEvent.Move]:
                self.d.frame.setGeometry(self.d.menu.geometry())

            elif e == QEvent.Show:
                self.d.frame.show()
                self.d.menu.raise_()

            elif e == QEvent.Hide:
                self.d.frame.hide()
        else:
            if e == QEvent.MouseButtonPress:
                self.d.stateMachine.shouldFade.emit()

                if type(watched) == QtMaterialFlatButton:
                    text: QString = watched.text()
                    self.setText(text)
                    self.itemSelected.emit(text)

        return QtMaterialTextField.eventFilter(self, watched, event)
