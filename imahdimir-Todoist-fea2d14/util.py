"""

    """

import asyncio
import pytz
import datetime

import pandas as pd
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync

from models import Todoist
from models import TodoistProject
from models import TodoistSection
from models import TodoistTask

to = Todoist()
tp = TodoistProject()

class Params :
    routine_proj_id = '2312505898'
    tz = pytz.timezone('Asia/Tehran')
    routine_reset_time = datetime.time(3 , 35 , 0 , tzinfo = tz)

pa = Params()

def ret_not_special_items_of_a_class(cls) :
    return {x : y for x , y in cls.__dict__.items() if not x.startswith('__')}

tpd = ret_not_special_items_of_a_class(TodoistProject)
tsd = ret_not_special_items_of_a_class(TodoistSection)
ttd = ret_not_special_items_of_a_class(TodoistTask)

def get_daily_routine_project_id() :
    df = get_all_todoist_projects()
    msk = df[tp.name].eq('routine')
    ind = df[msk].index[0]
    return df.at[ind , tp.id]

def get_all_sections() :
    secs = asyncio.run(get_sections_async())
    df = pd.DataFrame()
    for col in tsd :
        df[col] = [getattr(x , col) for x in secs]
    return df

def del_sections(id_list) :
    api = TodoistAPI(to.tok)
    for idi in id_list :
        api.delete_section(idi)

def get_all_todoist_projects() :
    apia = TodoistAPIAsync(to.tok)
    secs = asyncio.run(apia.get_projects())
    df = pd.DataFrame()
    for col in tpd :
        df[col] = [getattr(x , col) for x in secs]
    return df

async def get_sections_async() :
    api = TodoistAPIAsync(to.tok)
    try :
        scs = await api.get_sections()
        return scs
    except Exception as error :
        print(error)

async def get_all_tasks_async() :
    api = TodoistAPIAsync(to.tok)
    tsks = await api.get_tasks()
    return tsks

def get_all_tasks() :
    tsks = asyncio.run(get_all_tasks_async())
    df = pd.DataFrame()
    for col in ttd :
        df[col] = [getattr(x , col) for x in tsks]
    return df
