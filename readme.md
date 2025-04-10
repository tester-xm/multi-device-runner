功能描述
multi-device-runner 是一个用于多设备并行测试的工具，它可以同时在多个 Android 设备上运行 Airtest 脚本，并生成详细的测试报告。主要功能包括：
多设备并行测试：支持同时在多个 Android 设备上运行 Airtest 脚本，提高测试效率。
日志记录与管理：记录每个设备的测试日志，并提供日志清理和复制功能。
测试报告生成：为每个设备生成 HTML 格式的测试报告，并汇总测试结果。
日志解析与 Excel 生成：解析设备日志文件，并将日志内容整理成 Excel 文件。
安装依赖
在运行 multi-device-runner 之前，需要安装所需的 Python 依赖包。可以通过以下命令安装：
bash
pip install -r requirements.txt
requirements.txt 文件中包含了所有必要的依赖项，具体如下：
airtest: Airtest 测试框架，用于编写和执行自动化测试脚本。
pandas: 用于数据处理和分析的 Python 库。
openpyxl: 用于操作 Excel 文件的 Python 库。
pywin32: 用于在 Windows 平台上操作文件和文件夹的 Python 库。
部署软件
步骤 1：连接 Android 设备
确保所有需要进行测试的 Android 设备已通过 USB 连接到计算机，并且已经开启了 USB 调试模式。
步骤 2：准备 Airtest 脚本
将需要运行的 Airtest 脚本放在 multi-device-runner 目录下，例如 start_run_stop.air。
步骤 3：运行测试
在终端中进入 multi-device-runner 目录，然后运行以下命令：
bash
python run.py
如果需要重新运行所有脚本，可以使用以下命令：
bash
python run.py --run_all
步骤 4：查看测试报告
测试完成后，会在每个设备的日志目录下生成 HTML 格式的测试报告，同时会在项目根目录下生成一个汇总报告 report.html。可以使用浏览器打开这些报告文件，查看详细的测试结果。
注意事项
请确保计算机上已经安装了 ADB 工具，并且 ADB 环境变量已经正确配置。
在运行测试之前，建议清理设备的日志缓冲区，以避免旧日志对测试结果产生干扰。可以使用 clean_log_files 函数来清理日志文件。