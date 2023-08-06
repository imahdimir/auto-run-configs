"""

    """

import datetime as dt
from pathlib import Path

from models import ColName
from models import Todoist
from models import TodoistSection
from models import TodoistTask
from util import del_sections
from util import get_all_sections
from util import get_all_tasks
from util import Params

to = Todoist()
tt = TodoistTask()
ts = TodoistSection()
pa = Params()
c = ColName()

def split_max_time_of_section_from_its_name(df) :
    df[c.secmt] = df[ts.name].str.split('-')
    df[c.secmt] = df[c.secmt].apply(lambda x : x[1] if len(x) > 1 else None)
    df[c.secmt] = df[c.secmt].str.strip()
    return df

def find_next_reset_datetime() :
    dtn = dt.datetime.now(pa.tz)

    # routine reset date time
    if dtn.time() > pa.routine_reset_time :
        rrdate = dtn.date() + dt.timedelta(days = 1)
        rrdt = dt.datetime.combine(rrdate , pa.routine_reset_time)
    else :
        rrdt = dt.datetime.combine(dtn.date() , pa.routine_reset_time)

    print('next reset datetime: ' , rrdt)

    return rrdt

def format_max_time(df) :
    df[c.secmt] = df[c.secmt].str.upper()
    df[c.secmt] = df[c.secmt].str.replace('\s' , '' , regex = True)
    df[c.secmt] = df[c.secmt].str.replace(r'(AM|PM)' , r' \1' , regex = True)
    return df

def find_max_time(df) :
    pat = '([1-9]|10|11|12) (AM|PM)'

    msk = df[c.secmt].str.fullmatch(pat)
    msk = msk.fillna(False)

    fu = lambda x : dt.datetime.strptime(x , '%I %p').time()
    df.loc[msk , c.secmt] = df.loc[msk , c.secmt].apply(fu)

    pat = '([1-9]|10|11|12):\d\d (AM|PM)'

    msk = df[c.secmt].str.fullmatch(pat)
    msk = msk.fillna(False)

    fu = lambda x : dt.datetime.strptime(x , '%I:%M %p').time()
    df.loc[msk , c.secmt] = df.loc[msk , c.secmt].apply(fu)

    return df

def find_max_datetime(secmt , rrdt) :
    if secmt is None :
        return None

    elif rrdt.time() > secmt :
        secmt = dt.datetime.combine(rrdt.date() , secmt)

    else :
        scdt = rrdt.date() + dt.timedelta(days = -1)
        secmt = dt.datetime.combine(scdt , secmt)

    return secmt

def add_datetime_to_sections(df , rrdt) :
    df = format_max_time(df)
    df = find_max_time(df)

    df[c.secmt] = df[c.secmt].apply(lambda x : find_max_datetime(x , rrdt))

    fu = lambda x : x + dt.timedelta(minutes = 5) if x is not None else None
    df[c.secmt] = df[c.secmt].apply(fu)

    return df

def make_rm_section_based_on_time(df) :
    # mark passed sections true also those without max time (None)
    df['now'] = dt.datetime.now(pa.tz)
    df['now'] = df['now'].dt.tz_localize(None)
    df['now'] = df['now'].astype('datetime64[ns]')

    df[c.rm_sec] = df[c.secmt].lt(df['now'])

    msk = df[c.secmt].isnull()
    df.loc[msk , c.rm_sec] = True

    df = df.drop(columns = ['now'])

    return df

def adjust_rm_section_based_on_having_no_tasks(df) :
    dft = get_all_tasks()

    # mark sections with no tasks as true
    msk = ~ df[ts.id].isin(dft[tt.section_id])

    df[c.rm_sec] &= msk

    return df

def adj_rm_sec_based_on_not_pinned_sections(df) :
    msk = ~ df[ts.name].str.contains('📌')
    df[c.rm_sec] &= msk
    return df

def main() :
    pass

    ##
    # get all availabe sections in the routine project
    dfs = get_all_sections()

    ##
    # keep only routine project sections
    msk = dfs[ts.project_id].eq(pa.routine_proj_id)
    dfs = dfs[msk]

    ##
    # split max time of section from its name if exists
    dfs = split_max_time_of_section_from_its_name(dfs)

    ##
    # find next reset datetime
    rrdt = find_next_reset_datetime()

    ##
    # add date to max time of sections
    df = add_datetime_to_sections(dfs , rrdt)

    ##
    # find sections that their max time has passed, or have no max time
    df = make_rm_section_based_on_time(df)

    ##
    # find empty sections
    df = adjust_rm_section_based_on_having_no_tasks(df)

    ##
    # keep only not pinned sections
    df = adj_rm_sec_based_on_not_pinned_sections(df)

    ##
    # delete filtered sections
    del_sections(df.loc[df[c.rm_sec] , ts.id])

##


if __name__ == '__main__' :
    main()
    print(f'{Path(__file__).name} Done!')

##

if False :
    pass

    ##

    ##

    ##

    ##
