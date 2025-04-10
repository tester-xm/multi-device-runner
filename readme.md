项目概述
本项目是一个基于 Airtest 框架的多设备自动化测试项目，主要用于在多个 Android 设备上并行执行自动化测试脚本，并生成详细的测试报告。同时，还支持采集设备日志并解析成 Excel 文件。
项目结构
plaintext
multi-device-runner/
├── .DS_Store
├── run.py              # 主运行脚本
├── requirements.txt    # 项目依赖文件
├── 17027deb0906.xlsx   # 设备 17027deb0906 的日志解析 Excel 文件
├── report_tpl.html     # 测试报告模板文件
├── 17027deb0906.log    # 设备 17027deb0906 的日志文件
├── README.md           # 项目说明文档
├── 13afea4f0606.xlsx   # 设备 13afea4f0606 的日志解析 Excel 文件
├── data.json           # 测试结果数据文件
├── report.html         # 汇总测试报告文件
├── 13afea4f0606.log    # 设备 13afea4f0606 的日志文件
├── .git/               # Git 版本控制目录
└── start_run_stop.air/ # 测试脚本目录
依赖安装
在项目根目录下，运行以下命令安装所需的依赖包：
bash
pip install -r requirements.txt
requirements.txt 文件中包含了项目所需的各种 Python 库，如 Airtest、pytest、pandas 等。
运行说明
1. 设备连接
将待测试的 Android 设备通过 USB 连接到电脑，并开启设备的 USB 调试模式。
2. 运行测试
在项目根目录下，运行以下命令启动测试：
bash
python run.py
此命令会自动检测已连接的设备，然后在这些设备上并行执行 start_run_stop.air 脚本。如果需要重新运行所有脚本（不跳过之前已成功运行的脚本），可使用以下命令：
bash
python run.py --run_all
3. 测试报告
单设备报告：每个设备的测试日志会被保存到 start_run_stop.air/log/<device_id> 目录下，其中 <device_id> 是设备的唯一标识符。运行结束后，会自动为每个设备生成 HTML 格式的测试报告，存放在相应的日志目录下。
汇总报告：所有设备的测试结果会被汇总到 report.html 文件中，运行结束后会自动在浏览器中打开该文件，展示测试的总体情况。
4. 日志处理
日志采集：脚本会使用 adb logcat 命令采集每个设备的日志，并保存为 <device_id>.log 文件。
日志解析：运行结束后，会对日志文件进行解析，提取其中的日期和内容，并生成相应的 Excel 文件 <device_id>.xlsx。
日志清理：在每次运行测试前，会自动清理之前的日志文件和 Excel 文件，确保测试环境的干净。
注意事项
请确保设备已正确连接，并且 adb 命令可以正常使用。
若在运行过程中出现问题，请检查日志文件以获取详细的错误信息。
若需要修改测试用例，请编辑 start_run_stop.air 目录下的脚本文件。

使用这个的前提是，1-n部小米手机，需要手动连接手机-信任电脑-打开USB调试-允许USB调试-允许安装软件-传输文件模式-不要设置密码和手势密码｜且易安装小米计算器app。

python run.py