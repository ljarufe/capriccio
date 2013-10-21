'''
Created on 27/04/2010

@author: mauricio
'''
import xmlrpclib
import base64

class conecta():
    xml = ''
    
    def __init__(self):
        self.xml = xmlrpclib
        #return self.xml
         
    def coneccion(self):
        server = self.xml.ServerProxy('https://api.webfaction.com/')
        session_id, account = server.login("aqpnet","04718802")
        return session_id,server
    
    def obtener_mailboxes(self,server,session):
        a = session
        b = server
        c = b.list_mailboxes(a)
        options = ''
        for i in c:
            options += "<option value='%s'>%s</option>" % (i["mailbox"],i["mailbox"])
        
        return options
    
    def crear_mailbox_email_address(self,mailbox,server,session):
        a = session
        b = server
        b.create_mailbox(a,mailbox)
        b.create_email(a,mailbox + "@capriccioperu.com",mailbox)
        return "Creacion correcta cambie su contrasena"
    
    def cambiar_contrasena_mailbox(self,mailbox,server,session,password):
        a = session
        b = server
        b.change_mailbox_password(a,mailbox,base64.decodestring(password))
        return "Cambio exitoso"
    
    def eliminar_mailbox_email_address(self,mailbox,server,session):
        a = session
        b = server
        b.delete_email(a,mailbox+"@capriccioperu.com")
        b.delete_mailbox(a,mailbox)
        return "Cuenta Eliminada"
        

        
