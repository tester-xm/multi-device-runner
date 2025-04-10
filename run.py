# -*- encoding=utf-8 -*-
import os
import traceback
import subprocess
import webbrowser
import time
import json
import shutil
from airtest.core.android.adb import ADB
from jinja2 import Environment, FileSystemLoader
import re
import pandas as pd


def run(devices, air, run_all=False):
    try:
        results = load_json_data(air, run_all)
        tasks = run_on_multi_device(devices, air, results, run_all)
        for task in tasks:
            status = task['process'].wait()
            results['tests'][task['dev']] = run_one_report(task['air'], task['dev'])
            results['tests'][task['dev']]['status'] = status
            json.dump(results, open('data.json', "w"), indent=4)
        run_summary(results)

        time.sleep(3)

        replace_in_folder(air, 'Airtest Report', 'QQ13 Report')

        parent_folder = os.path.dirname(os.path.abspath(air))
        replace_in_parent_html(parent_folder, 'Airtest 多设备并行测试结果汇总', 'QQ13 多设备并行测试结果汇总')

    #     commands = [
    #     'airtest report start_run_stop.air --log_root start_run_stop.air/log/13afea4f0606 --outfile start_run_stop.air/log/13afea4f0606/log.html --lang zh',
    #     'airtest report start_run_stop.air --log_root start_run_stop.air/log/17027deb0906 --outfile start_run_stop.air/log/17027deb0906/log.html --lang zh'
    # ]
        commands = cmds
        execute_airtest_reports(commands)

    except Exception as e:
        traceback.print_exc()



def execute_airtest_reports(commands):
    for command in commands:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            print(f"命令 {command} 执行成功，输出如下：")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"命令 {command} 执行失败，错误信息如下：")
            print(e.stderr)

def replace_in_folder(air, old_text, new_text):
    for root, dirs, files in os.walk(air):
        for file in files:
            if file == 'log.html':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    new_content = content.replace(old_text, new_text)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Content in {file_path} has been replaced.")
                except Exception as e:
                    print(f"An error occurred while processing {file_path}: {e}")


def replace_in_parent_html(air, old_text, new_text):
    html_files = []
    for file in os.listdir(air):
        if file.endswith('.html'):
            html_files.append(os.path.join(air, file))
    for html_file in html_files[:2]:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = content.replace(old_text, new_text)
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Content in {html_file} has been replaced.")
        except Exception as e:
            print(f"An error occurred while processing {html_file}: {e}")

def run_on_multi_device(devices, air, results, run_all):
    tasks = []
    for dev in devices:
        if (not run_all and results['tests'].get(dev) and
           results['tests'].get(dev).get('status') == 0):
            print("Skip device %s" % dev)
            continue
        log_dir = get_log_dir(dev, air)
        cmd = [
            "airtest",
            "run",
            air,
            "--device",
            "Android:///" + dev,
            "--log",
            log_dir
        ]
        print("cmd "*5,cmd)
        try:
            tasks.append({
                'process': subprocess.Popen(cmd, cwd=os.getcwd()),
                'dev': dev,
                'air': air
            })
        except Exception as e:
            traceback.print_exc()
    return tasks


cmds = []
def run_one_report(air, dev):
    try:
        log_dir = get_log_dir(dev, air)
        print("log_dir "*5,log_dir)
        log = os.path.join(log_dir, 'log.txt')
        print("log "*5,log)

        if os.path.isfile(log):
            cmd = [
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--outfile",
                os.path.join(log_dir, 'log.html'),
                "--lang",
                "zh"
            ]
            ret = subprocess.call(cmd, shell=True, cwd=os.getcwd())
            print("Report build Success.", cmd)
            print("cmd."*5, ' '.join(cmd))
            cmds.append(' '.join(cmd))
            return {
                    'status': ret,
                    'path': os.path.join(log_dir, 'log.html')
                    }
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc()
    return {'status': -1, 'device': dev, 'path': ''}


def run_summary(data):
    try:
        summary = {
            'time': "%.3f" % (time.time() - data['start']),
            'success': [item['status'] for item in data['tests'].values()].count(0),
            'count': len(data['tests'])
        }
        summary.update(data)
        summary['start'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(data['start']))
        env = Environment(loader=FileSystemLoader(os.getcwd()),
                          trim_blocks=True)
        html = env.get_template('report_tpl.html').render(data=summary)
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(html)
        webbrowser.open('report.html')
    except Exception as e:
        traceback.print_exc()


def load_json_data(air, run_all):
    json_file = os.path.join(os.getcwd(), 'data.json')
    if (not run_all) and os.path.isfile(json_file):
        data = json.load(open(json_file))
        data['start'] = time.time()
        return data
    else:
        clear_log_dir(air)
        return {
            'start': time.time(),
            'script': air,
            'tests': {}
        }


def clear_log_dir(air):
    log = os.path.join(os.getcwd(), air, 'log')
    if os.path.exists(log):
        shutil.rmtree(log)


def get_log_dir(device, air):
    log_dir = os.path.join(air, 'log', device.replace(".", "_").replace(':', '_'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir


def generate_adb_commands(device_ids):
    if not device_ids:
        return ""
    commands = []
    for device_id in device_ids:
        # 异步清空设备的日志缓冲区
        subprocess.Popen(f"adb -s {device_id} logcat -c", shell=True)
        time.sleep(3)
        command = f"adb -s {device_id} logcat *:E > {device_id}.log"
        commands.append(command)
    return " & ".join(commands)


def clean_log_files(device_ids, log_root_dir="logcat"):
    # 清理当前目录下的日志文件和 Excel 文件
    current_dir = os.getcwd()
    for device_id in device_ids:
        log_file_path = os.path.join(current_dir, f"{device_id}.log")
        excel_file_path = os.path.join(current_dir, f"{device_id}.xlsx")
        if os.path.exists(log_file_path):
            try:
                os.remove(log_file_path)
                print(f"已删除当前目录下日志文件: {log_file_path}")
            except Exception as e:
                print(f"删除当前目录下文件 {log_file_path} 时出错: {e}")
        if os.path.exists(excel_file_path):
            try:
                os.remove(excel_file_path)
                print(f"已删除当前目录下 Excel 文件: {excel_file_path}")
            except Exception as e:
                print(f"删除当前目录下 Excel 文件 {excel_file_path} 时出错: {e}")

    # 清理指定目录下的日志文件
    log_base_dir = os.path.join(log_root_dir, "log")
    for device_id in device_ids:
        device_log_dir = os.path.join(log_base_dir, device_id)
        if os.path.exists(device_log_dir):
            for root, dirs, files in os.walk(device_log_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        print(f"已删除日志文件: {file_path}")
                    except Exception as e:
                        print(f"删除文件 {file_path} 时出错: {e}")


# def parse_log_file(log_file_path):
#     dates = []
#     contents = []
#     date_pattern = re.compile(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
#     with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
#         for line in file:
#             match = date_pattern.search(line)
#             if match:
#                 date = match.group(1)
#                 content = line.replace(date, '').strip()
#                 dates.append(date)
#                 contents.append(content)
#     return dates, contents

def parse_log_file(log_file_path):
    date_content_dict = {}
    date_pattern = re.compile(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = date_pattern.search(line)
            if match:
                date = match.group(1)
                content = line.replace(date, '').strip()
                if date in date_content_dict:
                    date_content_dict[date].append(content)
                else:
                    date_content_dict[date] = [content]

    dates = []
    contents = []
    for date, content_list in date_content_dict.items():
        combined_content = '\n'.join(content_list)
        dates.append(date)
        contents.append(combined_content)

    return dates, contents


def generate_excel(device_id, log_file_path):
    dates, contents = parse_log_file(log_file_path)
    df = pd.DataFrame({
        '日期': dates,
        '内容': contents
    })
    excel_file_path = f"{device_id}.xlsx"
    df.to_excel(excel_file_path, index=False)
    print(f"已生成 Excel 文件: {excel_file_path}")


def run_and_pause_after_5s(device_ids, log_root_dir="logcat"):
    air = 'start_run_stop.air'
    clean_log_files(device_ids, air)
    command = generate_adb_commands(device_ids)
    if not command:
        return
    try:
        process = subprocess.Popen(command, shell=True)
        devices = [tmp[0] for tmp in ADB().devices()]
        # air = 'start_run_stop.air'
    
        # Continue tests saved in data.json
        # Skip scripts that run succeed
        # 基于data.json的进度，跳过已运行成功的脚本
        # run(devices, air)

        # Resun all script
        # 重新运行所有脚本
        run(devices, air, run_all=True)

        time.sleep(5)
        process.terminate()
        print("命令已在运行 5 秒后结束。")
        log_base_dir = os.path.join(log_root_dir, "log")
        if not os.path.exists(log_base_dir):
            os.makedirs(log_base_dir)

        for device_id in device_ids:
            device_log_dir = os.path.join(log_base_dir, device_id)
            print("device_log_dir"*5,device_log_dir)
            replace_in_folder(device_log_dir, 'Airtest Report', 'QQ13 Report')
            if not os.path.exists(device_log_dir):
                os.makedirs(device_log_dir)
            log_file_path = f"{device_id}.log"
            destination_path = os.path.join(device_log_dir, f"{device_id}.log")
            if os.path.exists(log_file_path):
                shutil.copy2(log_file_path, destination_path)
                print(f"日志文件 {log_file_path} 已复制到 {destination_path}")
                generate_excel(device_id, log_file_path)
    except Exception as e:
        print(f"执行命令时出现错误: {e}")
        
if __name__ == '__main__':
    print("generate"*5)
    devices_ids = [tmp[0] for tmp in ADB().devices()]
    command = run_and_pause_after_5s(devices_ids,log_root_dir='start_run_stop.air')

    # devices = [tmp[0] for tmp in ADB().devices()]
    # air = 'start_run_stop.air'
    
    # # Continue tests saved in data.json
    # # Skip scripts that run succeed
    # # 基于data.json的进度，跳过已运行成功的脚本
    # # run(devices, air)

    # # Resun all script
    # # 重新运行所有脚本
    # run(devices, air, run_all=True)