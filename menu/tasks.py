from celery import shared_task
from dotenv import load_dotenv, find_dotenv
from django.utils import timezone
from menu.models import User, Menu, Menu_Selected
from django.utils import timezone
import os
import aiohttp
import asyncio

load_dotenv(find_dotenv())

@shared_task
def create_task():
    linkUUID = getMenuUUID()
    resultCall = asyncio.run(slackApiCall(linkUUID))
    return resultCall

def getMenuUUID():
   """
   Obtains the menu uuid from the db and creates the link for
   the user to access to the daily menu. 
   """
   now = timezone.localtime().strftime("%Y-%m-%d")
   menuUUID = Menu.objects.filter(fecha_menu = now).values()
   linkUUID = 'http://127.0.0.1:1337/menu/' + menuUUID[0]['id_menu'] + '/'
   return linkUUID  

async def get_response(session, url):
    """
    Performs an async request with a given url
    """
    headers = {'Authorization': 'Bearer ' + os.environ.get('SLACK_API_TOKEN')}
    async with session.get(url, headers = headers) as resp:
        response = await resp.json()
        return response

async def slackApiCall(linkUUID):
    """
    Create an url with the parameter necessaries to create a reminder in slack,
    then that url is passed to get_response function.
    """
    try:
        dataCall = []
        tasks = []
        async with aiohttp.ClientSession() as session:
            
            urls =[
                'https://slack.com/api/reminders.add?text='+ linkUUID +'&'+
                                    'time=in%205%20minutes&pretty=1'           
                ]    
         
            for url in urls:
                tasks.append(asyncio.ensure_future(get_response(session, url)))

            result_response = await asyncio.gather(*tasks)
            for response in result_response:
                dataCall.append(response)
            
            return dataCall
    except Exception:
        return False