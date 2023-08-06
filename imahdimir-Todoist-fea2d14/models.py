"""

    """

from mtok import get_token as get_tok

class ColName :
    url = 'url'
    jsn = 'json'
    th = 'T-[h]'
    tm = 'T-[m]'
    indnt = 'INDENT'
    srt = 'sort'
    sec = 'section'
    secn = 'secn'
    secmt = 'sec_max_time'
    pri = 'PRIORITY'
    tty = 'T Type'
    cnt = 'CONTENT'
    ty = "TYPE"
    sec_id = 'sec_id'
    par_id = 'par_id'
    labels = 'labels'
    excl = 'Exclude'
    rm_sec = 'remove_section'

class TodoistTask :
    assignee_id = 'assignee_id'
    assigner_id = 'assigner_id'
    comment_count = 'comment_count'
    is_completed = 'is_completed'
    content = 'content'
    created_at = 'created_at'
    creator_id = 'creator_id'
    description = 'description'
    due = 'due'
    id = 'id'
    labels = 'labels'
    order = 'order'
    parent_id = 'parent_id'
    priority = 'priority'
    project_id = 'project_id'
    section_id = 'section_id'
    url = 'url'

class TodoistSection :
    id = 'id'
    name = 'name'
    order = 'order'
    project_id = 'project_id'

class TodoistProject :
    color = 'color'
    comment_count = 'comment_count'
    id = 'id'
    is_favorite = 'is_favorite'
    is_inbox_project = 'is_inbox_project'
    is_shared = 'is_shared'
    is_team_inbox = 'is_team_inbox'
    name = 'name'
    order = 'order'
    parent_id = 'parent_id'
    url = 'url'
    view_style = 'view_style'

class Types :
    tsk = 'task'
    sec = 'section'

class Notion :
    tok = get_tok('Notion')
    db_id = get_tok('Notion_Day_Routine_db_id')
    db_url = f'https://api.notion.com/v1/databases/{db_id}/query'
    pg_url = 'https://api.notion.com/v1/pages/'
    hdrs = {
            'Authorization'  : f'Bearer {tok}' ,
            'Notion-Version' : '2022-06-28' ,
            }

class Todoist :
    tok = get_tok('Todoist')
    hdrs = {
            'Authorization' : f'Bearer {tok}'
            }
