'''
Created on Aug 7, 2014
 @author Angel Daniel Munoz Gonzalez
 @email angel.dtmunoz@gmail.com
 @School Universidad Tecnologica de Ciudad Juarez
 
'''
from __future__ import with_statement
from com.ziclix.python.sql import zxJDBC
from com.ziclix.python import *
from javax.swing import JOptionPane, UIManager
import csv
import sys
_nimbus = 'com.sun.java.swing.plaf.nimbus.NimbusLookAndFeel'
    
UIManager.setLookAndFeel(_nimbus)

_sentinel = object()
def next(it, default=_sentinel):
    '''
        Emulates The next() built in Function
    '''
    try:
        return it.next()
    except StopIteration:
        if default is _sentinel:
            raise
        return default
    
def TimeMismatchException():
    '''
        Exception to be raised when The Time Format is Different from what the method has defined in itself
    '''
    raise TypeError('Time Mismatch Exception')

def DataMismatchException():
    '''
        Exception to be raised when The File Doe not contain The Data Required by the Database
    '''
    raise TypeError('File Does not contain required data')

def ExistsInDB():
    '''
        Exception to be raised when The File has a record where Date and Time already exist in the database
        There can be several records with the same date or the same hour,
        but not more than one with the same date and time
    '''
    raise TypeError('Record Exists already in the Database')

def onDataMismatch(t):
    '''
        Error handler when the Data in File is different from the data required by the Database
    '''
    JOptionPane.showMessageDialog(None, 'File Does not contain required data', 'Data Mismatch', JOptionPane.ERROR_MESSAGE)

def onDateMismatch24h(q):
    '''
        Warning Shown When The Time Format is not Set to 24H Format
    '''
    JOptionPane.showMessageDialog(None, 'Time Is Not Set to 24H Format', 'Time Mismatch File', JOptionPane.WARNING_MESSAGE)
    
def onDateMismatchAmPm(q):
    '''
        Warning Shown When The Time Format is not Set to 12H AM-PM Format
    '''
    JOptionPane.showMessageDialog(None, 'Time Is Not Set to 12H AM-PM Format', 'Time Mismatch File', JOptionPane.WARNING_MESSAGE)

def onComsFailure(e):
        '''
           Error raised when it is Impossible to Comunicate with the Database due to Server Down or Inexistent Database in Server
        '''
        JOptionPane.showMessageDialog(None, 'Unable to Access Database', 'Database Comunication Error', JOptionPane.ERROR_MESSAGE)

def onNonExistentTable(t):
    '''
           Error raised when The Table to Insert Records Does not Exist
    '''
    JOptionPane.showMessageDialog(None, 'Table "Registros" Does not Exist', 'Database Comunication Error', JOptionPane.ERROR_MESSAGE)    

def onExistsInDB(i):
    '''
        Error shown to the user where the file contains a record that already exists in the database
    '''
    JOptionPane.showMessageDialog(None, 'Duplicate Record Found and File Will not be processed', 'Duplicate Record Found', JOptionPane.ERROR_MESSAGE)

def ampmformat (hhmm):
    """
        This method converts time in 24h format to 12h format
        Example:   "00:32" is "12:32 AM"
               "13:33" is "01:33 PM"
    """
    ampm = hhmm.split (":")
    if (len(ampm) == 0) or (len(ampm) > 3):
        return hhmm

    # is AM? from [00:00, 12:00[
    hour = int(ampm[0]) % 24
    isam = (hour >= 0) and (hour < 12)

    # 00:32 should be 12:32 AM not 00:32
    if isam:
        ampm[0] = ('12' if (hour == 0) else "%02d" % (hour))
    else:
        ampm[0] = ('12' if (hour == 12) else "%02d" % (hour-12))

    return ':'.join (ampm) + (' AM' if isam else ' PM')
  


def dirId(dirVie):
    '''
        This Method assigns an Id for the Wind Direction Marked in the File
    '''
    if dirVie is 'N':
        return 1
    elif dirVie == 'NNE':
        return 2
    elif dirVie == 'NE':
        return 3
    elif dirVie == 'ENE':
        return 4
    elif dirVie == 'E':
        return 5
    elif dirVie == 'ESE':
        return 6
    elif dirVie == 'SE':
        return 7
    elif dirVie == 'SSE':
        return 8
    elif dirVie == 'S':
        return 9
    elif dirVie == 'SSW':
        return 10
    elif dirVie == 'SW':
        return 11
    elif dirVie == 'WSW':
        return 12
    elif dirVie == 'W':
        return 13
    elif dirVie == 'WNW':
        return 14
    elif dirVie == 'NW':
        return 15
    elif dirVie == 'NNW':
        return 16



def actualizar_ampm_db(archivo):
    """
    This method Updates the Database From a Previously Selected File which Contains 12h AM-PM Time Format
    """

    
    try:
        conn = zxJDBC.connect("jdbc:mysql://localhost/realinfo_test",  # @UndefinedVariable
              "root", "admin", 
              "org.gjt.mm.mysql.Driver")
    
    except sql.zxJDBC.Error, e:
        print e
        onComsFailure(e)
        sys.exit(0)
        
    cursor = conn.cursor()
    use_db = 'USE REALINFO_TEST;'
    cursor.execute(use_db)
    
    with open(archivo, 'r') as f:
        read_data = csv.reader(f, delimiter=';') 
        print 'archivo abierto'
        #especificamos que la primera linea no es necesario leerla
        header = next(read_data)
        print header
        #con un for Circulamos por cada una de las lineas del archivo
        print "Observando y Agregando el Contenido..."
        for row in read_data:
            #print row
            #almacenamos cada dato en una variable en cada iteracion
            try:
                id_registro, fecha, presion_rel, temp_int, humedad_int,\
                temp_ext, humedad_ext, punto_cond, viento_frio, velocidad_viento,\
                dir_viento, racha, lluvia_rel, lluvia_total = row
            except ValueError, t:
                onDataMismatch(t)
                print 'cerrando archivo...'
                f.close()
                print 'archivo cerrado'
                print 'cerrando conexion...'
                conn.close()
                print 'conexion cerrada'
                sys.exit(0)

            try:
                if len(fecha) < 19:
                    TimeMismatchException()
            except TypeError, q:
                onDateMismatchAmPm(q)
                print 'cerrando archivo...'
                f.close()
                print 'archivo cerrado'
                print 'cerrando conexion...'
                conn.close()
                print 'conexion cerrada'
                sys.exit(0)
                
            fecha2 = fecha.split()
            hora = fecha2.pop(1)
            tiempo = fecha2.pop(1)
            hora += ' '
            hora += tiempo
            fechaF1 = fecha2.pop(0)
            fechaF2 = fechaF1.split('.')
            fechaF3 = ''
            fechaF3 += '%s-%s-%s' % (fechaF2.pop(2), fechaF2.pop(0), fechaF1.split('.').pop(1))


            query = "SELECT DIR_VIENTO FROM REGISTROS WHERE FECHA=\'%s\' AND HORA=\'%s\'" % (fechaF3, hora)
            cursor.execute(query)
            resultado = cursor.fetchall()    
            
            try:
                if len(resultado) <= 0:
                    pass
                else:
                    ExistsInDB()
            except TypeError, i:
                onExistsInDB(i)
                print 'cerrando archivo...'
                f.close()
                print 'archivo cerrado'
                print 'cerrando conexion...'
                conn.close()
                print 'conexion cerrada'
                sys.exit(0)


            if dir_viento == 'N':
                dir_id = 1
            else:
                dir_id = dirId(dir_viento)
                '''
                Bug Aqui, Cuando dir_viento = 'N' no asigna el valor correcto
                '''   
                insert_values = """INSERT INTO REGISTROS(FECHA, HORA, PRESION_RELATIVA_inHg, TEMPERATURA_INTERIOR_F, HUMEDAD_INTERIOR, TEMPERATURA_EXTERIOR_F, HUMEDAD_EXTERIOR, PUNTO_CONDENSACION, VIENTO_FRIO, VELOCIDAD_VIENTO, DIR_VIENTO,DIR_ID, RACHA, LLUVIA_RELATIVA, LLUVIA_TOTAL)
                           VALUES(\'%s\', \'%s\', %f, %f, %f, %f, %f, %f, %f, %f, \'%s\',%f, %f, %f, %f);""" % (
                                            fechaF3,
                                            hora,
                                            float(presion_rel),
                                            float(temp_int),
                                            float(humedad_int),
                                            float(temp_ext),
                                            float(humedad_ext),
                                            float(punto_cond),
                                            float(viento_frio),
                                            float(velocidad_viento),
                                            dir_viento,
                                            float(dir_id),
                                            float(racha),
                                            float(lluvia_rel),
                                            float(lluvia_total))
                try:
                    cursor.execute(insert_values)
                    
                except sql.zxJDBC.Error, t:
                    onNonExistentTable(t)
                    print 'cerrando archivo...'
                    f.close()
                    print 'archivo cerrado'
                    print 'cerrando conexion...'
                    conn.close()
                    print 'conexion cerrada'
                    sys.exit(0)    
    #Commit Debe hacerse Fuera del For Each
    conn.commit()    
    print 'cerrando archivo...'
    f.close()
    print 'archivo cerrado'
    print 'cerrando conexion...'
    conn.close()
    print 'conexion cerrada'
    
  

def actualizar_24h_db(archivo):
    """
    This method Updates the Database From a Previously Selected File which Contains 24h Time Format
    """
    try:
        conn = zxJDBC.connect("jdbc:mysql://localhost/realinfo_test",  # @UndefinedVariable
              "root", "admin", 
              "org.gjt.mm.mysql.Driver")
    
    except sql.zxJDBC.Error, e:
        print e
        onComsFailure(e)
        sys.exit(0)
        
        
    cursor = conn.cursor()
    use_db = 'USE REALINFO_TEST;'
    cursor.execute(use_db)
        
    with open(archivo, 'r') as f:
        read_data = csv.reader(f, delimiter=';') 
                
        print 'archivo abierto'
        #especificamos que la primera linea no es necesario leerla
        
        #con un for Circulamos por cada una de las lineas del archivo
        print "Observando y Agregando el Contenido..."
        header = next(read_data)
        print header
        for row in read_data:
            
            #almacenamos cada dato en una variable en cada iteracion
            try:
                id_registro, fecha, presion_rel, temp_int, humedad_int,\
                temp_ext, humedad_ext, punto_cond, viento_frio, velocidad_viento,\
                dir_viento, racha, lluvia_rel, lluvia_total = row
            except ValueError, t:
                onDataMismatch(t)
                print 'cerrando archivo...'
                f.close()
                print 'archivo cerrado'
                print 'cerrando conexion...'
                conn.close()
                print 'conexion cerrada'
                sys.exit(0)


            try:
                if len(fecha) > 16:
                    TimeMismatchException()
            except TypeError, q:
                onDateMismatch24h(q)
                print 'cerrando archivo...'
                f.close()
                print 'archivo cerrado'
                print 'cerrando conexion...'
                conn.close()
                print 'conexion cerrada'
                sys.exit(0)
                
            fecha2 = fecha.split()
            hora = fecha2.pop(1)
            hora = ampmformat(hora)
            fechaF1 = fecha2.pop(0)
            fechaF2 = fechaF1.split('.')
            fechaF3 = ''
            fechaF3 += '%s-%s-%s' % (fechaF2.pop(2), fechaF2.pop(0), fechaF1.split('.').pop(1))


            query = "SELECT DIR_VIENTO FROM REGISTROS WHERE FECHA=\'%s\' AND HORA=\'%s\'" % (fechaF3, hora)
            cursor.execute(query)
            resultado = cursor.fetchall()    
            
            try:
                if len(resultado) <= 0:
                    pass
                else:
                    ExistsInDB()
            except TypeError, i:
                onExistsInDB(i)
                print 'cerrando archivo...'
                f.close()
                print 'archivo cerrado'
                print 'cerrando conexion...'
                conn.close()
                print 'conexion cerrada'
                sys.exit(0)
            
            if dir_viento == 'N':
                dir_id = 1
            else:
                dir_id = dirId(dir_viento)
            '''
             Bug Aqui, Cuando dir_viento = 'N' no asigna el valor correcto
            '''   
            insert_values = """INSERT INTO REGISTROS(FECHA, HORA, PRESION_RELATIVA_inHg, TEMPERATURA_INTERIOR_F, HUMEDAD_INTERIOR, TEMPERATURA_EXTERIOR_F, HUMEDAD_EXTERIOR, PUNTO_CONDENSACION, VIENTO_FRIO, VELOCIDAD_VIENTO, DIR_VIENTO,DIR_ID, RACHA, LLUVIA_RELATIVA, LLUVIA_TOTAL)
                           VALUES(\'%s\', \'%s\', %f, %f, %f, %f, %f, %f, %f, %f, \'%s\',%f, %f, %f, %f);""" % (
                                            fechaF3,
                                            hora,
                                            float(presion_rel),
                                            float(temp_int),
                                            float(humedad_int),
                                            float(temp_ext),
                                            float(humedad_ext),
                                            float(punto_cond),
                                            float(viento_frio),
                                            float(velocidad_viento),
                                            dir_viento,
                                            float(dir_id),
                                            float(racha),
                                            float(lluvia_rel),
                                            float(lluvia_total))
    #Ejecutamos el Query
            #print insert_values
            try:
                cursor.execute(insert_values)
            except sql.zxJDBC.Error, t:
                onNonExistentTable(t)
                
                sys.exit(0)
    #print 'cosa'
    #Guardamos los cambios en la base de datos       
    conn.commit()
            
    print 'cerrando archivo...'
    f.close()
    print 'archivo cerrado'
    print 'cerrando conexion...'
    conn.close()
    print 'conexion cerrada'
