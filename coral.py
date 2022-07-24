import pathlib
import os
import datetime
import re
import platform
import numpy as np
import graphlib

def onefile_serch(filename, search_target, sep ='|'):
    with open(filename, 'rt', encoding="utf-8") as f:
        text = f.readlines()

    count = []
    for i in range(len(text)):
        line = text[i]
        if (search_target in line):
            count.append(i)

    coral_tag = []
    if len(count)>0:
        # coralタグ抽出
        s = text[count[0]]
        r = ((s[s.find(search_target + sep) + len(search_target + sep):]).replace('\n', '')).split('|')
        print(r)

        # 親文字列操作
        r[0] = r[0].replace(' ', '')
        r[0] = r[0].replace('　', '')
        if len(r[0])>0:
            coral_tag.append(re.split('[,]', r[0]))
        else:
            coral_tag.append(False)

        # メモ文字列操作
        kaigyo_num = 16
        memo = ''
        for i in np.arange(len(r[1])//kaigyo_num+1):
            memo = memo + r[1][kaigyo_num*i:kaigyo_num*(i+1)] + '<br/>'
        coral_tag.append(memo)

        # color文字列操作
        if r[2]=='r' or r[2]=='red':
            coral_tag.append('#fa2100')
        elif r[2]=='g' or r[2]=='green':
            coral_tag.append('#0dfa00')
        elif r[2]=='b' or r[2]=='blue':
            coral_tag.append('#0015fa')
        elif r[2]=='y' or r[2]=='yellow':
            coral_tag.append('#fae100')
        elif r[2]=='m' or r[2]=='magenta':
            coral_tag.append('#fa00ee')
        elif r[2]=='c' or r[2]=='cyan':
            coral_tag.append('#00f2fa')
        elif r[2]=='k' or r[2]=='black':
            coral_tag.append('#242424')
        else:
            coral_tag.append('#ecffed')

    else:
        coral_tag = False

    return coral_tag

def creation_date(path_to_file):
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime

def graph_max_path_count(graph):
    max_node_path_count = 0
    for i in np.arange(len(graph)):
        max_node_path_count = max_node_path_count + 1
        ts = graphlib.TopologicalSorter(graph)
        ts.prepare()
        ready_nodes = ts.get_ready()
        del_key_list = []
        for gn in graph.keys():
            hit_node = set(ready_nodes) & set(graph[gn])
            if len(hit_node)>0:
                stay_node = graph[gn]^hit_node
                if len(stay_node)>0:
                    graph[gn] = graph[gn]^hit_node
                else:
                    del_key_list.append(gn)
        for dkl in del_key_list:
            del graph[dkl]
        if len(graph)==0:
            break

    return  max_node_path_count


def coral_make(target_dir='./', target_ext='.py', search_target='coral', sep='|'):

    file_list = [str(p.resolve()) for p in pathlib.Path(target_dir).glob('**/*'+target_ext)]

    # main node
    mermaid_main_node = ''
    dt_list = []
    dt_graph_dict = {}
    for file_path in file_list:
        coral_tag = onefile_serch(file_path, search_target = '!'+search_target, sep = sep)
        if coral_tag:
            # ファイル作成日時
            dt = str(datetime.datetime.fromtimestamp(creation_date(pathlib.Path(file_path))))[0:10]
            dt = dt.replace('-','_')
            dt_list.append(dt)
            # ファイル名のみ抽出
            file_name = os.path.basename(file_path)

            mermaid_main_node = mermaid_main_node+'subgraph '+dt+'\n'
            mermaid_main_node = mermaid_main_node+file_name+'["'+file_name+'<br/>'+coral_tag[1]+'"]'+'\n'
            mermaid_main_node = mermaid_main_node+'style '+file_name+' fill:'+coral_tag[2]+',stroke:#000000'+'\n'
            mermaid_main_node = mermaid_main_node+'end\n'
            if coral_tag[0]:
                if dt in dt_graph_dict.keys():
                    dt_graph_dict[dt][file_name] = set(coral_tag[0])
                else:
                    dt_graph_dict[dt] = {file_name:set(coral_tag[0])}
                for c0 in coral_tag[0]:
                    mermaid_main_node = mermaid_main_node+c0+'-->'+file_name+'\n'

            mermaid_main_node = mermaid_main_node+'\n'

    # 日時のテキスト作成
    mermaid_date = ''
    dt_list = list(set(dt_list))
    dt_list.sort()
    for i in np.arange(len(dt_list)):
        mermaid_date = mermaid_date+'subgraph '+dt_list[i]+'\n'
        mermaid_date = mermaid_date+dt_list[i]+'_[" "]\n'
        mermaid_date = mermaid_date+'style '+dt_list[i]+' fill:#e8e8e8,stroke:#e8e8e8'+'\n'+'style '+dt_list[i]+'_ fill:#e8e8e8,stroke:#e8e8e8'+'\n'+'end\n\n'
    for i in np.arange(len(dt_list)-1):
        pc = graph_max_path_count(dt_graph_dict[dt_list[i]])
        mermaid_date = mermaid_date+dt_list[i]+'_-'+'-'*pc+'-'+dt_list[i+1]+'_\n'+'linkStyle '+str(i)+' stroke-width:0px\n'

    # merge
    mermaid_txt = '```mermaid\ngraph BT\n'+mermaid_date+'\n\n\n'+mermaid_main_node+'```'

    path_w = 'coral.md'
    with open(path_w, mode='w', encoding='utf-8') as f:
        f.write(mermaid_txt)

    print(dt_graph_dict)
    pass

coral_make()

