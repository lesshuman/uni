csv-файл для тарификации формируется следующим образом:
nfdump -r nfcapd.202002251200 -o csv > dump.csv
Тарификация трафика:
python3 lab2.py
Просмотр статистики (генерация графика зависимости объема трафика от времени):
python3 plot.py
Скрипты также приведены в ipynb-формате и могут быть запущены в jupyter notebook, в т.ч. онлайн. Достаточно запустить демо-версию JupyterLab по ссылке (https://hub.gke.mybinder.org/user/jupyterlab-jupyterlab-demo-1hctmj6t/lab), загрузить .ipynb и .csv файлы, и запустить выполнение скрипта.
Построенный график сохранен в файле stats.pdf

