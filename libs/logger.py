import os
import sys
from logging import getLogger, FileHandler, StreamHandler, Formatter, shutdown

def writelog(logname, systemname, msg, logfilename='log'):
    logpath = 'log'
    logfullpath = logpath + '\\' + logfilename +'.log'
    if os.path.exists(logpath) == False:
        print("mkdir", logpath)
        os.makedirs(logpath)

    # ログの出力名を設定
    logger = getLogger(systemname)
    msg = str(sys.argv[0]) + " - " + systemname + " - " + msg
    if logname == 'notest': #設定値の記録
        level = 0
    elif logname == 'debug': #動作確認の記録
        level = 10
    elif logname == 'info': #正常動作の記録
        level = 20
    elif logname == 'warning': #ログの記録
        level = 30
    elif logname == 'error': #エラーの記録
        level = 40
    
    # ログレベルの設定
    logger.setLevel(level)
    # ログのファイル出力先を設定
    fh = FileHandler(logfullpath)
    logger.addHandler(fh)
    # ログのコンソール出力の設定
    sh = StreamHandler()
    logger.addHandler(sh)
    # ログの出力形式の設定
    #formatter = Formatter('%(asctime)s:%(lineno)d:%(levelname)s:%(message)s')
    formatter = Formatter('%(asctime)s - %(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.log(level, msg)
    for h in logger.handlers:
        logger.removeHandler(h)
    shutdown()
    return