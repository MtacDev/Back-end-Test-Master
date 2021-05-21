from menu.models import User, Menu, Menu_Selected
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import uuid

class CreateUser:
    """ 
    This class save the user info into the database
    """
    def __init__(self,name,username,
                                password,
                                nationality,
                                access):
        self.name = name
        self.username = username
        self.password = password
        self.nationality = nationality
        self.access = access
        self.resultCreatedUser = self.save_user()

    def save_user(self):
        encrypted_pass = make_password(self.password)
        try:
            saveUser = User(name = self.name,
                                    username = self.username,
                                    password = encrypted_pass,
                                    nationality = self.nationality,
                                    access = self.access)
            saveUser.save()
            return True
        except Exception:
            return False

class menuSelected():
    """
    This class save the menu selected by the user 
    """
    def __init__(self,optionSelected, customMenu, username, fecha):
        self.optionselected = optionSelected
        self.customMenu = customMenu
        self.fecha = fecha
        self.username = username
        self.resultMenuSelected = self.saveMenuSelected()

    def saveMenuSelected(self):
        try:
            now = timezone.localtime().strftime("%Y-%m-%d")
            userId = User.objects.filter(username = self.username).values()
            menu = Menu.objects.filter(fecha_menu = self.fecha).values() 
                            
            saveMenuSelc = Menu_Selected(user = User.objects.get(id_user = userId[0]['id_user']),
                                            menu = Menu.objects.get(id_menu = menu[0]['id_menu']),
                                            option_selected = self.optionselected,
                                            customization = self.customMenu,
                                            fecha_menu_selec = now)

            saveMenuSelc.save()
            return True
        except Exception:
            return False        

class checkCredentials:
    """ 
    This class check the username and password of the user to allow or 
    denies the Log In 
    """
    def __init__(self,username, password):
        self.username = username
        self.password = password
        self.levelOfAccess = 0
    
    def getUserdata(self):      
        userObj = User.objects.filter(username = self.username).values()
        if userObj:
            return userObj
        else:
            return False

    def checkCredentials(self):
        encrypted_pass = self.getUserdata()
        if encrypted_pass != False:
            resultLog = check_password(self.password ,encrypted_pass[0]['password'])
            self.levelOfAccess = encrypted_pass[0]['access']
            return resultLog
        else:
            return False

class dailyMenu:
    """ 
    This class save the daily menus created
    """
    def __init__(self, fechamenu,descMenu):
        self.fechamenu = fechamenu
        self.descMenu = descMenu
        self.resultSaveMenu = self.saveDayliMenu()

    def saveDayliMenu(self):
        try:
            saveMenu = Menu(id_menu = uuid.uuid1(),
                                fecha_menu = self.fechamenu,                
                                desc_menu = self.descMenu)
            saveMenu.save()
            return True
        except Exception:
            return False

class updateMenu:
    """
    This class update the changes in the menus options. 
    """
    def __init__(self, fechaMenu,editedMenu):
        self.fechaMenu = fechaMenu
        self.editedMenu = editedMenu
        self.resultUdate = self.updateDayliMenu()
    
    def updateDayliMenu(self):
        try:
            Menu.objects.filter(fecha_menu = self.fechaMenu).update(
                desc_menu = self.editedMenu
            )
            return True
        except Exception:
            return False