[]: # 1. 安装依赖
pip install -r requirements.txt
[]: # 2. 运行
python run.py

airtest run start_run_stop.air --device Android:///13afea4f0606 --log start_run_stop.air/log/13afea4f0606
airtest report start_run_stop.air --log_root start_run_stop.air/log/13afea4f0606 --outfile start_run_stop.air/log/13afea4f0606/log.html --lang zh

airtest run start_run_stop.air --device Android:///17027deb0906 --log start_run_stop.air/log/17027deb0906
airtest report start_run_stop.air --log_root start_run_stop.air/log/17027deb0906 --outfile start_run_stop.air/log/17027deb0906/log.html --lang zh