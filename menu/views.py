"""
System with 3 level of access: NORMAL, EXECUTIVE and ADMIN.
To be able to access the acconts its need the username and password:
    - User = Carlos, username = carlos, password = 123456, Level of access = ADMIN
    - User = Julia, username = julia, password = 123456, Level of access = EXECUTIVE
    - User = Maria, username = maria, password = 123456, Level of access = NORMAL
Incompleted requirements:     
    - testing
"""

from django.shortcuts import redirect, render
from menu.models import User, Menu, Menu_Selected
from .forms import FormCreateUser, FormCreateMenu, FormLogin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .savedata_class import CreateUser, menuSelected, checkCredentials, dailyMenu, updateMenu
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import create_task
import os

def login(request):
    os.environ['ENVUSERNAME'] = ''
    os.environ['ACCESSLEVEL'] = ''
    formLogin = obtainLoginData(request)

    try:
        #The username is save in a env variable 
        # to validate if a user do a logged correctly
        os.environ['ENVUSERNAME'] = formLogin.username
        if formLogin.levelOfAccess == '1':
            return redirect('/home')
        elif formLogin.levelOfAccess == '2':
            #The level of access is save in a env variable to validate if 
            # a user can enter to certain urls like modifymenu and menurequests. 
            os.environ['ACCESSLEVEL'] = formLogin.levelOfAccess
            return redirect('/createmenu')
        elif formLogin.levelOfAccess == '3':
            return redirect('/adminform')
        
    except Exception:
        context = {
            'formLogin': formLogin,
        } 
        return render(request, "template/login.html",context = context)

def home(request): 
    objMenus = menuForTheDay()
    obtainMenuSelected(request)

    try:
        username = os.environ['ENVUSERNAME']
        if username:
            
            context = {
                'username': username,
                'menus':objMenus[0][0],
                'fomartFecha': objMenus[0][1]
            }
            return render(request, "template/home.html", context = context)
        else:
            return redirect('../')   
    except Exception:
        return redirect('../')  

def adminform(request):
    formUser = obtainUserData(request)

    try:
        username = os.environ['ENVUSERNAME']
        if username:

            context = {
                'formUser': formUser,
                'username': username
            }
            return render(request, "template/adminform.html", context = context)
        else:
            return redirect('../')   
    except Exception:
        return redirect('../') 

def createMenu(request):
    formMenu = obtainMenuData(request)

    try:
        username = os.environ['ENVUSERNAME']
        if username:
            
            context = {
                'formMenu': formMenu,
                'username': username
            }
            return render(request, "template/createmenu.html", context = context)
        else:
            return redirect('../')   
    except Exception:
        return redirect('../') 

def menuoftheday(request):
    return render(request, "template/menuoftheday.html")

def menurequests(request):
    now = timezone.localtime().strftime("%Y-%m-%d")
    try:
        access = os.environ['ACCESSLEVEL']
        if access == "2":
            menusSelected = Menu_Selected.objects.filter(fecha_menu_selec = now).values()
            nameUser= User.objects.filter(id_user=menusSelected[0]['user_id']).values()
            context = {
                'menusSelected': menusSelected,
                'nameUser':nameUser[0]['name'],
                'fecha':now
            }
            return render(request, "template/menurequests.html", context = context)
        else:
            return redirect('../')      
    except Exception:
        return redirect('../')               

def modifyMenu(request):
    now = timezone.localtime().strftime("%Y-%m-%d")
    obtainModifiedMenu(request)
    try:
        access = os.environ['ACCESSLEVEL']
        if access == "2":
            editMenu = Menu.objects.filter(fecha_menu = now).values()
            
            context = {
                'editMenu': editMenu,
                'Date':now
            }
            return render(request, "template/modifymenu.html", context = context)
        else:
            return redirect('../')      
    except Exception:
        return redirect('../')  

def obtainLoginData(request):
    """
    This function obtain the data from the login form fields, and pass 
    the credentials of log in to the class checkCredentials.   
    """
    if request.method == 'POST':
      
        formLogin = FormLogin(request.POST)

        if formLogin.is_valid():

            username = formLogin.cleaned_data.get('username')
            password = formLogin.cleaned_data.get('password')
            if not isinstance(username, str):
                raise ValueError('The username has to be an string')
            if not isinstance(password, str):
                raise ValueError('The password has to be an string')

            check = checkCredentials(username, password)
            logIn = check.checkCredentials()
            
            if logIn !=False:
                return check
            else:
                formLogin = FormLogin()
                message = 'Username or password are incorrect'
                messages.error(request, message)       
        else:
           formLogin = FormLogin.errors
             
    else:
       formLogin = FormLogin()

    return formLogin 

def obtainUserData(request):
    """
    This function obtains the values from the
    admin view fields to create a new user, using the class CreateUser.
    """

    if request.method == 'POST':
        
        formUser = FormCreateUser(request.POST)
        if formUser.is_valid():
            name = formUser.cleaned_data.get('name')
            user_name = formUser.cleaned_data.get('user_name')
            password = formUser.cleaned_data.get('password')
            nationality = formUser.cleaned_data.get('nationality')
            user_access = formUser.cleaned_data.get('user_access')
            
            if not isinstance(name, str):
                raise ValueError('The name has to be an string')
            if not isinstance(user_name, str):
                raise ValueError('The user_name has to be an string')
            if not isinstance(password, str):
                raise ValueError('The pasword has to be an string')
            if not isinstance(nationality, str):
                raise ValueError('The nationality has to be an string')
            if not isinstance(user_access, str):
                raise ValueError('The user_access has to be an string')
         
            newUser = CreateUser(name,user_name,
                                        password,
                                        nationality,
                                        user_access)

            formUser = FormCreateUser()
            if newUser.resultCreatedUser == False:
                message = 'The user was not created'
                messages.error(request, message)
            else:
                message = "New user was created"
                messages.success(request, message)     
        else:
            formUser = FormCreateUser.errors
                    
    else:
        formUser = FormCreateUser()

    return formUser

def obtainMenuData(request):
    """
    This function obtain the data from the create menu view form fields
    to create the menu of the day instantiating the class dailyMenu.  
    """
    if request.method == 'POST':
        
        formMenu = FormCreateMenu(request.POST)
        if formMenu.is_valid():
            fechaMenu = formMenu.cleaned_data.get('fecha_menu')
            descMenu = formMenu.cleaned_data.get('name_menu')

            if not isinstance(descMenu, str):
                raise ValueError('The descMenu has to be an string')
            
            dMenu = dailyMenu(fechaMenu, descMenu)
            formMenu = FormCreateMenu()
            if dMenu == False:

                message = 'The menu was not Created'
                messages.error(request, message)
            else:
                message = "Today's menu added"
                messages.success(request, message)  
        else:
            formMenu = FormCreateMenu.errors
             
    else:
        formMenu = FormCreateMenu()

    return formMenu

    
def obtainMenuSelected(request):
    """
    This function obtain the data from the option menu and custom menu fields
    and passes the data to the class menuSelected.  
    """
    if request.method == 'POST':

        userOptionSelected = str(request.POST['optionSelected'])
        customMenu = request.POST['customizatedMenu']  
        username = request.POST['username']
        date = request.POST['dateoftheMenu']
        
        if not isinstance(userOptionSelected, str):
            raise ValueError('The userOptionSelected has to be an string')
        if not isinstance(customMenu, str):
            raise ValueError('The customMenu has to be an string')
        if not isinstance(username, str):
            raise ValueError('The username has to be an string')
       

        optionSaved = menuSelected(userOptionSelected,
                                        customMenu,
                                        username,
                                        date)
             
        if optionSaved.resultMenuSelected == False:
            message = 'The option selected was not saved'
            messages.error(request, message) 
        else:
            message = "The option selected was saved"
            messages.success(request, message) 

def obtainModifiedMenu(request):
    """
    Capture data from the view modifymenu fields
    and passes to the class updateMenu.
    """ 
    if request.method == 'POST':    
        dateMenu = request.POST['datemenu']
        editedMenu = request.POST['editDescMenu']
        if not isinstance(dateMenu, str):
            raise ValueError('The dateMenu has to be an string')
        if not isinstance(editedMenu, str):
            raise ValueError('The editedMenu has to be an string')

        resultUpdate = updateMenu(dateMenu,editedMenu)

        if resultUpdate.resultUdate == False:
                message = "The menu couldn't be modified"
                messages.error(request, message)
        else:
            message = "Today's menu has been edited"
            messages.success(request, message) 


def menuForTheDay():
    """
    This function validates the current time to allow the user to 
    pick an option menu between 8 am and 11 am. 
    Also makes a consult to the database for obtain the 
    menus of the day.    
    """
    objMenu = []
    menus = ''
    now = timezone.localtime()
    currentTime = now.strftime("%H:%M:%S")
    if currentTime > '08:00:00' and currentTime < '21:00:00':    
        menus = Menu.objects.filter(fecha_menu = now.strftime("%Y-%m-%d")).values()
        
        if menus:
            objMenu.append([menus,now.strftime("%Y-%m-%d")])
           
        else:    
            yesterday = now - timedelta(1) 
            menus = Menu.objects.filter(fecha_menu = yesterday.strftime("%Y-%m-%d")).values()
            objMenu.append([menus, yesterday.strftime("%Y-%m-%d")])
    else:
        objMenu.append(['',''])    
    return objMenu  


@csrf_exempt
def run_task(request):
    """
    It's receive the post from the view createmenu to 
    trigger the tasks in tasks.py
    """   
    if request.POST:
        task = create_task()
        return JsonResponse({"task": task}, status=202)


def getUUID(request,uuid):
    """
    It's receive the uuid from a link posted in reminders 
    in slack then uses the uuid to identify the menu of the day
    """
    menu = Menu.objects.filter(id_menu=uuid).values()
    context = {
            'menu': menu,
        }
    return render(request, "template/menuoftheday.html", context = context)