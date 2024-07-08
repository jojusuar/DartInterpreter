from PyQt5.QtWidgets import QApplication, QWidget, QPlainTextEdit, QTextBrowser, QVBoxLayout, QHBoxLayout, QPushButton
import lexico
import sintactico
import sys
import os

app = QApplication(sys.argv)

# Ventana principal
window = QWidget()
window.setWindowTitle('Verificador de Dart')
window.setGeometry(100, 100, 800, 600)

layout = QVBoxLayout(window)
buttonRow = QHBoxLayout(window)

text_input = QPlainTextEdit(window)
text_input.setPlaceholderText('Escribe código Dart aquí')

text_output = QTextBrowser(window)

layout.addWidget(text_input)
layout.addLayout(buttonRow)
layout.addWidget(text_output)


# Botón de validación
validationButton = QPushButton('Validar', window)

def cleanup(layout):
    os.remove(layout)

# Acción de validar
def on_button_click():
    sintactico.variables = {}
    lexico.illegal = []
    syntaxOK = semanticsOK = False
    input_text = text_input.toPlainText()
    lexOutput = lexico.testTokens(input_text, 'app')
    illegalTokens = lexOutput[0]
    lexLog = lexOutput[1]
    syntaxLog = ''
    semanticsLog = ''
    # resultados del análisis léxico
    text_output.append('*********************************************')
    if len(illegalTokens) == 0:
        text_output.append('Análisis léxico exitoso!')
        output = sintactico.validate_algorithm(input_text, 'app')
        syntaxOK, semanticsOK, syntaxLog, semanticsLog = output[0], output[1], output[2], output[3]
        # resultados del análisis sintáctico
        if syntaxOK:
            text_output.append('Análisis sintáctico exitoso!')
            #resultados del análisis semántico
            if semanticsOK:
                text_output.append('Análisis semántico exitoso!')
                text_output.append('El código ha sido validado correctamente!\n')
            else:
                text_output.append('Análisis semántico fallido!')
                semanticsLogFile = open(semanticsLog, 'r')
                for line in semanticsLogFile:
                    text_output.append(line.rstrip())
                text_output.append('')
        else:
            text_output.append('Análisis sintáctico fallido!')
            syntaxLogFile = open(syntaxLog, 'r')
            for line in syntaxLogFile:
                text_output.append(line.rstrip())
            text_output.append('')
        cleanup(lexLog)
        cleanup(syntaxLog)
        cleanup(semanticsLog)
    else:
        text_output.append('Análisis léxico fallido!')
        for token in illegalTokens:
            text_output.append(f'Caracter ilegal: {token}')
        cleanup(lexLog)
    
validationButton.clicked.connect(on_button_click)

# botón para limpiar la consola
cleanButton = QPushButton('Limpiar consola', window)

def on_clean_click():
    text_output.setText('')

cleanButton.clicked.connect(on_clean_click)

buttonRow.addWidget(validationButton)
buttonRow.addWidget(cleanButton)

def resizeEvent(event):
    text_input.resize(window.width() - 40, window.height() - 40)

window.resizeEvent = resizeEvent
window.setLayout(layout)
window.show() 


app.exec()