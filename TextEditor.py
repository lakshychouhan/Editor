import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QFont, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QTextEdit, QAction, QFileDialog

class CodeEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.code_highlighter = CodeHighlighter(self.document())
        self.setFontFamily("Courier New")
        self.setFontPointSize(12)
        self.setStyleSheet("background-color: #2b2b2b; color: #cccccc;")
        self.setTabStopWidth(80)
        self.setAcceptRichText(False)

class CodeHighlighter:
    def __init__(self, document):
        self.document = document
        self.highlighting_rules = []

        self.highlighting_enabled = True  # Add this line to store the highlighting state

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569cd6"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["if", "else", "while", "for", "break", "continue", "return"]
        for word in keywords:
            self.highlighting_rules.append((rf'\b{word}\b', keyword_format))

        self.highlighting_rules.append((r'#[^\n]*', QTextCharFormat().setForeground(QColor("#808080"))))

        self.current_block = None
        self.document.contentsChange.connect(self.on_contents_change)

    def apply_format_to_block(self, block, format):
        if self.highlighting_enabled and block.isValid() and format.isValid():
            cursor = QTextCursor(block)
            cursor.select(QTextCursor.BlockUnderCursor)
            cursor.setCharFormat(format)

    def on_contents_change(self):
        if self.current_block and self.current_block.text() == "":
            self.highlight_current_block()

    def highlight_current_block(self):
        if self.current_block:
            self.apply_format_to_block(self.current_block, QTextCharFormat().clear())
        cursor = QTextCursor(self.document.findBlockByNumber(self.document.blockCount() - 1))
        self.current_block = cursor.block()
        if self.current_block:
            self.apply_format_to_block(self.current_block, QTextCharFormat().setBackground(QColor("#2b2b2b")))

    # Add this method to set the highlighting state
    def set_highlighting_enabled(self, enabled):
        self.highlighting_enabled = enabled

class MultiTabbedEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.create_actions()
        self.create_menus()

        self.setWindowTitle("Multi-Tab Text Editor")
        self.setGeometry(100, 100, 800, 600)

    def create_actions(self):
        self.new_action = QAction("New", self)
        self.new_action.triggered.connect(self.new_tab)

        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_file)

        self.toggle_highlight_action = QAction("Toggle Syntax Highlighting", self)
        self.toggle_highlight_action.setCheckable(True)
        self.toggle_highlight_action.setChecked(True)
        self.toggle_highlight_action.triggered.connect(self.toggle_highlighting)

        self.highlight_action = QAction("Highlight Text", self)
        self.highlight_action.triggered.connect(self.highlight_text)

    def create_menus(self):
        self.file_menu = self.menuBar().addMenu("File")
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)

        self.edit_menu = self.menuBar().addMenu("Edit")
        self.edit_menu.addAction(self.toggle_highlight_action)
        self.edit_menu.addAction(self.highlight_action)

    def new_tab(self):
        editor = CodeEditor()
        self.central_widget.addTab(editor, f"Untitled-{self.central_widget.count() + 1}")

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                editor = CodeEditor()
                editor.setPlainText(content)
                self.central_widget.addTab(editor, file_path)

    def toggle_highlighting(self):
        enable_highlighting = self.toggle_highlight_action.isChecked()
        current_editor = self.central_widget.currentWidget()
        if current_editor:
            current_editor.code_highlighter.set_highlighting_enabled(enable_highlighting)

    def highlight_text(self):
        current_editor = self.central_widget.currentWidget()
        if current_editor:
            text_format = QTextCharFormat()
            text_format.setBackground(QColor("yellow"))

            cursor = current_editor.textCursor()
            cursor.mergeCharFormat(text_format)
            current_editor.setTextCursor(cursor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = MultiTabbedEditor()
    editor.show()
    sys.exit(app.exec_())
