import csv
import os
import random

def get_row_count(filename):
    row_count = 0
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if len(row) > 0:
                row_count += 1
    return row_count

def get_datas(flg=0):
    datas = []
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if flg == 0:
                datas.append(row['name'])
            else:
                datas.append(row['id'])
    return datas

def get_name_list(id_list):
    name_list = []
    id_set = set(id_list)
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] in id_set:
                name_list.append(row['name'])
    return name_list

def get_name_by_id(user_id):
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == str(user_id):
                return row['name']
    return None

def get_id_by_name(target_name):
    with open('data.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name'] == target_name:
                return row['id']
    return None

def get_name_and_job_lists():
    id_list = []
    job_list = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id_list.append(row['id'])
            job_list.append(row['job'])
    name_list = get_name_list(id_list)
    return name_list, job_list

def get_to_id(user_id):
    with open('interview.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['from'] == str(user_id):
                return row['to']
    return None

def get_vote_max_ids():
    max_vote = 0
    max_ids = []
    with open('vote.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            vote_count = int(row['ted'])
            if vote_count > max_vote:
                max_vote = vote_count
    with open('vote.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row['ted']) == max_vote:
                max_ids.append(row['id'])
    return max_ids

def get_alives_ids():
    alives_ids = []
    with open('status.csv', 'r') as status_file:
        status_reader = csv.DictReader(status_file)
        for row in status_reader:
            if row['vital'] == '0':
                alives_ids.append(row['id'])
    return alives_ids

def get_alivewolfs_ids():
    wolf_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['job'] == '人狼' and row['vital'] == '0':
                wolf_ids.append(row['id'])
    return wolf_ids

def get_exeid_by_sham():
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['sham'] == '1':
            return row['id']    

def mk_vote_dsc():
    rows = []
    dsc_lines = []
    with open('vote.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        name = row['name']
        vote_count = row['ted']
        vote_list = row['list']
        vote_ids = vote_list.strip(";").split(";")
        vote_names = get_name_list(vote_ids)
        votes = ", ".join(vote_names)
        if vote_count == "0":
            dsc_lines.append(f"{name} {vote_count}票")
        else:
            dsc_lines.append(f"{name} {vote_count}票 <- [{votes}]")
    return "\n".join(dsc_lines)

def update_check_count(payload): # DMへの反応をCHECKする
    user_id = payload.user_id
    check_count = 0
    rows = []
    with open('check.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['id'] == str(user_id):
            if row['check'] == '1':
                return -1
            else:
                row['check'] = '1'
        if row['check'] == '1':
            check_count += 1
    with open('check.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return check_count

def update_check_count_wolf():
    wolf_ids = []
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['job'] == '人狼' and row['vital'] == '0':
                wolf_ids.append(row['id'])
    rows = []
    with open('check.csv', 'r', newline='') as check_file:
        check_reader = csv.DictReader(check_file)
        rows = list(check_reader)
        for row in rows:
            if row['id'] in wolf_ids:
                row['check'] = '1'
    with open('check.csv', 'w', newline='') as check_file:
        fieldnames = check_reader.fieldnames
        writer = csv.DictWriter(check_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    check_count = sum(1 for row in rows if row['check'] == '1')
    return check_count

def update_check_count_other():
    others_ids = []
    ftnd_zero_ids = []
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['vital'] == '0':
            if row['job'] in ('狂人', '市民', '霊媒師'):
                others_ids.append(row['id'])
            if row['ftnd'] == '0':
                ftnd_zero_ids.append(row['id'])
    if len(ftnd_zero_ids) == 0:
        with open('status.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['job'] == '占い師' and row['vital'] == '0':
                    others_ids.append(row['id'])
    rows = []
    with open('check.csv', 'r', newline='') as check_file:
        check_reader = csv.DictReader(check_file)
        rows = list(check_reader)
    for row in rows:
        if row['id'] in others_ids:
            row['check'] = '1'
    with open('check.csv', 'w', newline='') as check_file:
        fieldnames = check_reader.fieldnames
        writer = csv.DictWriter(check_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    check_count = sum(1 for row in rows if row['check'] == '1')
    return check_count

def update_from(user_id):
    with open('interview.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id,])

def update_status(user_id, flg=0):
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    if flg == 1:
        for row in rows:
            if row['id'] == str(user_id):
                row['kil'] = '1'
    elif flg == 2:
        for row in rows:
            if row['id'] == str(user_id):
                row['ftnd'] = '2'
    elif flg == 3:
        for row in rows:
            if row['id'] == str(user_id):
                row['grd'] = '1'
    elif flg == 4:
        for row in rows:
            if row['id'] == str(user_id):
                row['grd'] = '2'
    elif flg == 5:
        for row in rows:
            if row['id'] == str(user_id):
                row['vital'] = '1'
                row['sham'] = '1'
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def update_interview(user_id, to_id):
    rows = []
    with open('interview.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['from'] == user_id:
            row['to'] = to_id
    with open('interview.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def update_vote_list(id_number, user_id):
    rows = []
    with open('vote.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['id'] == str(id_number):
            vote_count = int(row['ted'])
            vote_count += 1
            row['ted'] = str(vote_count)
            row['list'] += ';' + str(user_id)
    with open('vote.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def reset_check_column():
    rows = []
    with open('check.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        row['check'] = '0'
    with open('check.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def set_vote_data(flg=1):
    if flg == 1:
        alives_ids = get_alives_ids()
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames + ['ted', 'list']
            with open('vote_tmp.csv', 'w', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in reader:
                    if row["id"] not in alives_ids:
                        continue
                    row['ted'] = '0'
                    row['list'] = ''
                    writer.writerow(row)
        os.replace("vote_tmp.csv", "vote.csv")
    elif flg == 2:
        executed_ids = get_vote_max_ids()
        if len(executed_ids) > 1:
            with open('data.csv', 'r') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames + ['ted', 'list']
                with open('vote_tmp.csv', 'w', newline='') as outfile:
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in reader:
                        if row["id"] not in executed_ids:
                            continue
                        row['ted'] = '0'
                        row['list'] = ''
                        writer.writerow(row)
            os.replace("vote_tmp.csv", "vote.csv")

def reset_flg_status():
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['grd'] == '1':
            row['grd'] = '0'
        if row['vital'] == '0':
            row['kil'] = '0'
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def reset_fortune():
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['ftnd'] == '2':
            row['ftnd'] = '1'
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def reset_conse_grd_flg():
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for row in rows:
        if row['grd'] == '2':
            row['grd'] = '1'
            break
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def reset_temp():
    with open("interview_temp.csv", "w", newline="") as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["from", "to"])
    os.remove("interview.csv")
    os.replace("interview_temp.csv", "interview.csv")

def select_ids_other_alives(user_id):
    selected_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['vital'] == '0' and row['id'] != str(user_id):
                selected_ids.append(row['id'])
    return selected_ids

def select_grd_ids(user_id):
    selected_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['vital'] == '0' and row['id'] != str(user_id) and row['grd'] == '0':
                selected_ids.append(row['id'])
    return selected_ids

def random_select_to(user_id):
    selected_ids = select_ids_other_alives(user_id)
    if selected_ids is None:
        print("interview to error")
        return
    selected_id = random.choice(selected_ids)
    rows = []
    with open('interview.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            if row['from'] == str(user_id):
                row['to'] = selected_id
    with open('interview.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def check_game_status():
    job_wolf_count = 0
    job_villager_count = 0
    alive_wolf_count = 0
    with open('status.csv', 'r') as status_file:
        status_reader = csv.DictReader(status_file)
        for row in status_reader:
            if row['job'] == '人狼' and row['vital'] == '0':
                alive_wolf_count += 1
                job_wolf_count += 1
            elif row['job'] == '狂人' and row['vital'] == '0':
                job_wolf_count += 1
            elif row['vital'] == '0':
                job_villager_count += 1
    if alive_wolf_count == 0:
        return 2
    elif job_wolf_count >= job_villager_count:
        return 1
    else:
        return 0

def count_alives():
    count = 0
    with open('status.csv', 'r') as status_file:
        status_reader = csv.DictReader(status_file)        
        for row in status_reader:
            if row['vital'] == '0':
                count += 1
    return count

def check_status(flg=0):
    checked = 0
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    if flg == 1:
        for row in rows:
            if row['vital'] == '0' and row['kil'] == '1':
                checked = 1
                break
    elif flg == 2:
        for row in rows:
            if row['vital'] == '0' and row['ftnd'] == '2':
                checked = 1
                break
    elif flg == 3:
        for row in rows:
            if row['vital'] == '0' and (row['grd'] == '1' or row['grd'] == '2'):
                checked = 1
                break
    return checked

def shuffle_discussion_order():
    discussion_ids = []
    with open('status.csv', 'r') as status_file:
        status_reader = csv.DictReader(status_file)
        for row in status_reader:
            if row['vital'] == '0':
                discussion_ids.append(row['id'])
    random.shuffle(discussion_ids)
    return discussion_ids

def ini_settings():
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = ['id', 'job', 'col','vital','ftnd', 'sham', 'kil', 'grd']
        with open('status_tmp.csv', 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                job_value = ''
                col_value = ''
                vital_value = '0'
                ftnd_value = '0'
                sham_value = '0'
                kil_value = '0'
                grd_value = '0'
                writer.writerow({'id': row['id'], 'job': job_value, 'col': col_value, 'vital': vital_value, 'ftnd': ftnd_value ,'sham': sham_value, 'kil': kil_value, 'grd': grd_value})
    os.replace("status_tmp.csv", "status.csv")
    with open('data.csv', 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['ted', 'list']
        with open('vote_tmp.csv', 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                row['ted'] = '0'
                row['list'] = ''
                writer.writerow(row)
    os.replace("vote_tmp.csv", "vote.csv")
    with open('data.csv', 'r') as file: # dm flg check
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['check']
        with open('check_tmp.csv', 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                row['check'] = '0'
                writer.writerow(row)
    os.replace("check_tmp.csv", "check.csv")
    with open("interview_temp.csv", "w", newline="") as temp_file:
        writer = csv.writer(temp_file)
        writer.writerow(["from", "to"])
    os.replace("interview_temp.csv", "interview.csv")

def select_random_white():
    rand_white_ids = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['col'] == '0' and row['ftnd'] == '0':
                rand_white_ids.append(row['id'])
    rand_white_id = random.choice(rand_white_ids)
    rand_white_name = get_name_by_id(rand_white_id)
    rows = []
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['id'] == rand_white_id:
                row['ftnd'] = '1'
            rows.append(row)
    with open('status.csv', 'w', newline='') as file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return rand_white_name

def assign_roles():
    name_count = get_row_count('data.csv')
    if 9 <= name_count <= 11:
        roles = ['人狼', '人狼', '狂人', '騎士', '占い師', '霊媒師']
    elif 12 <= name_count <= 14:
        roles = ['人狼', '人狼', '人狼', '狂人', '騎士', '占い師', '霊媒師']
    elif name_count == 15:
        roles = ['人狼', '人狼', '人狼', '狂人', '狂人', '騎士', '占い師', '霊媒師']
    elif name_count == 8:
        roles = ['市民', '狂人', '騎士', '占い師', '霊媒師']
        random.shuffle(roles)
        roles.pop()
        roles += ['人狼']*2
    elif name_count == 7:
        roles = ['市民', '騎士', '占い師', '霊媒師']
        random.shuffle(roles)
        roles.pop()
        roles += ['人狼']*2
    elif 4 <= name_count <= 6:
        roles = ['市民', '狂人', '騎士', '占い師']
        random.shuffle(roles)
        roles.pop()
        roles += ['人狼']*2
    else:
        print("assign error")
        return
    num_citizens = name_count - len(roles)
    roles += ['市民'] * num_citizens
    random.shuffle(roles)
    with open('status.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    for i, row in enumerate(rows):
        role_index = i % len(roles)
        role = roles[role_index]
        row['job'] = role
        if role == "人狼":
            row['col'] = "1"
        else:
            row['col'] = "0"
            if role == "占い師":
                row['ftnd'] = '1'
    with open('status.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def mk_info(num):
    if 9 <= num <= 11:
        txt = "□ 配役\n人狼2 狂人1 占い師1 霊媒師1 騎士1 " + f"\n市民{num-6}"
    elif 12 <= num <= 14:
        txt = "□ 配役\n人狼3 狂人1 占い師1 霊媒師1 騎士1 " + f"\n市民{num-7}"
    elif num == 15:
        txt = "□ 配役\n人狼3 狂人2 占い師1 霊媒師1 騎士1 \n市民7"
    elif num == 8:
        txt = "□ 配役\n人狼2 狂人1* 占い師1* 霊媒師1* 騎士1* \n市民2~3 ※*欠けあり"
    elif num == 7:
        txt = "□ 配役\n人狼2 占い師1* 霊媒師1* 騎士1* \n市民2~3 ※*欠けあり"
    elif 4 <= num <= 6:
        txt = "□ 配役\n人狼1 狂人1* 占い師1* 騎士1* "+ f"\n市民{num-4}~{num-3} ※*欠けあり"
    else:
        txt = "□ 配役\n（4~15人まで設定可）"
    return txt
