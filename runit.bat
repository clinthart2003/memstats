ECHO ON

cd C:\Pycharm\TQ_Setup

python ./plot_csv_create.py %*

python ./plot_csv_create_jvm.py %*

python ./plot_csvload_js.py %*

python ./plot_system_mem_js.py %*

python ./plot_topstats_js.py %*

python ./plot_combo_tqc_cpu.py %*

python ./plot_combo_graph.py %*

python ./plot_diskio_js.py %*

python ./plot_java_usage_js.py %*

python ./create_list.py %*

ROBOCOPY "C:\Pycharm\TQ_Setup\results\memory" "C:\inetpub\wwwroot" /mir