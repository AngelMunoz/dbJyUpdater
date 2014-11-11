'''
Created on Aug 8, 2014

@author: DanielTuna
'''
from javax.swing import JScrollPane, JCheckBox, UIManager
from javax.swing import JFileChooser
from javax.swing import JButton
from javax.swing import JPanel
from javax.swing import JFrame
from javax.swing import JTextArea
from javax.swing import JLabel
from javax.swing import JTextField
from javax.swing.filechooser import FileNameExtensionFilter
from importarDatosJy3_0 import actualizar_24h_db,actualizar_ampm_db
import sys

nimbus = 'com.sun.java.swing.plaf.nimbus.NimbusLookAndFeel'
UIManager.setLookAndFeel(nimbus)



class DatabaseUpater(JFrame):

    def __init__(self):
        super(DatabaseUpater, self).__init__()

        self.initUI()

    def initUI(self):
        self.hFormat = True
        
        self.panel = JPanel()
        self.panel.setLayout(None)
        self.getContentPane().setLayout(None)

        self.btnUpdateDb = JButton('Update Database', actionPerformed=self.updateDb)
        self.btnUpdateDb.setBounds(12, 215, 150, 25)
        self.btnUpdateDb.setEnabled(False)
        self.getContentPane().add(self.btnUpdateDb)
             
        self.btnExit = JButton('Exit', actionPerformed=self.bye)
        self.btnExit.setBounds(323, 215, 97, 25)
        self.getContentPane().add(self.btnExit)
        
        self.btnAddFile = JButton('Add File', actionPerformed=self.addFile)
        self.btnAddFile.setBounds(270, 48, 150, 25)
        self.getContentPane().add(self.btnAddFile)
        
        self.lblFilePath = JLabel("File Path:")
        self.lblFilePath.setBounds(12, 16, 60, 16)
        self.getContentPane().add(self.lblFilePath)
        
        self.txtFileName = JTextField()
        self.txtFileName.setBounds(72, 13, 350, 25)
        self.txtFileName.setColumns(10)
        self.getContentPane().add(self.txtFileName)
        
        
        self.chkAmPm = JCheckBox('AM-PM Hour Format',True, actionPerformed = self.hourFormat)
        self.chkAmPm.setBounds(267, 82, 177, 25)
        self.getContentPane().add(self.chkAmPm)
        
        self.scrPane = JScrollPane()
        self.scrPane.setBounds(12, 48, 227, 154)
        self.getContentPane().add(self.scrPane)
        
        self.txaContent = JTextArea()
        self.txaContent.setEditable(False)
        self.scrPane.setViewportView(self.txaContent)
        
             
        self.setTitle("File chooser")
        self.setBounds(100,100,450,300)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setLocationRelativeTo(None)
        self.setVisible(True)
        self.setDefaultLookAndFeelDecorated(True)
	self.setResizable(False)

    def addFile(self, e):

        chooseFile = JFileChooser()
        filter = FileNameExtensionFilter("Text files", ["txt"])
        chooseFile.addChoosableFileFilter(filter)

        ret = chooseFile.showDialog(self.panel, "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            text = self.readFile(file)
            self.txaContent.setText(text)
            self.txtFileName.setText(file.getCanonicalPath())
            self.btnUpdateDb.setText('Update Database')
            self.btnUpdateDb.setEnabled(True)

    def readFile(self, file):
        filename = file.getCanonicalPath()
        f = open(filename, "r")
        text = f.read()
        return text
    
    def hourFormat(self,e):
        source = e.getSource()
        isSelected = source.isSelected()
        
        if isSelected:
            self.hFormat = True
        else:
            self.hFormat = False
    
    def bye(self,e):
        sys.exit(0)

    def updateDb(self,e):
        if self.hFormat:
            self.btnUpdateDb.setEnabled(False)
            actualizar_ampm_db(self.txtFileName.getText())
            self.btnUpdateDb.setText('Database Updated')
            
            
        else:
            self.btnUpdateDb.setEnabled(False)
            actualizar_24h_db(self.txtFileName.getText())
            self.btnUpdateDb.setText('Database Updated')

