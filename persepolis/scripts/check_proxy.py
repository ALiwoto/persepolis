import urllib
import requests
import os
from persepolis.scripts import logger
import platform
import subprocess

# finding platform
os_type = platform.system()
platform = 'platform : ' + os_type
logger.sendToLog(platform, "INFO")

# get proxy function
def getProxy():
    socks_proxy = False

    # finding desktop environment
    desktop = os.environ.get('XDG_CURRENT_DESKTOP')
    proxy = {}
    if os_type == 'Linux' or os_type == 'FreeBSD' or os_type == 'OpenBSD':
        if desktop == None:
            desktop_env_type = 'Desktop Environment not detected!'
        else:
            desktop_env_type = 'Desktop environment: ' + str(desktop)

        logger.sendToLog(desktop_env_type, "INFO")
        print(desktop_env_type)

    # check if it is KDE
    if desktop == 'KDE' :
        # creat empty list for proxies
        proxysource = {}

        # user home directory path
        home_address = os.path.expanduser("~")

        # read kde plasma proxy config file
        try:
            plasma_proxy_config_file_path = os.path.join(home_address, '.config', 'kioslaverc')
            with open(plasma_proxy_config_file_path) as proxyfile:
                for line in proxyfile:
                    name, var = line.partition("=")[::2]
                    proxysource[name.strip()] = str(var)
        except:
            logger.sendToLog('no proxy file detected', 'INFO')

        # check proxy enabled as manually
        if proxysource['ProxyType'].split('\n')[0] == '1' :
            # get ftp proxy
            try:
                proxy['ftp_proxy_port'] = proxysource['ftpProxy'].split(' ')[1].replace("/", "").replace("\n", "")
                proxy['ftp_proxy_ip'] = proxysource['ftpProxy'].split(' ')[0].split('//')[1]
            except:
                logger.sendToLog('no manuall ftp proxy detected', 'INFO')

            # get http proxy
            try:
                proxy['http_proxy_port'] = proxysource['httpProxy'].split(' ')[1].replace("/", "").replace("\n", "")
                proxy['http_proxy_ip'] = proxysource['httpProxy'].split(' ')[0].split('//')[1]
            except:
                logger.sendToLog('no manuall http proxy detected', 'INFO')

            # get https proxy
            try:
                proxy['https_proxy_port'] = proxysource['httpsProxy'].split(' ')[1].replace("/", "").replace("\n", "")
                proxy['https_proxy_ip'] = proxysource['httpsProxy'].split(' ')[0].split('//')[1]
            except:
                logger.sendToLog('no manuall https proxy detected', 'INFO')

            # get socks proxy
            try:
                socks_proxy = proxysource['socksProxy'].split(' ')[0].split('//')[1]

            except:
                socks_proxy = False

        # proxy disabled
        else:
            logger.sendToLog('no manuall proxy detected', 'INFO')


    # if it is windows,mac and other linux desktop
    else:
        # get proxies
        proxysource = urllib.request.getproxies()
        # get http proxy
        try:
            proxy['http_proxy_ip'] = proxysource['http'].split(':')[1].replace('//','')
            proxy['http_proxy_port'] = proxysource['http'].split(':')[2].replace("/", "").replace("\n", "")
        except:
            logger.sendToLog('no http proxy detected', 'INFO')

        # get https proxy
        try:
            proxy['https_proxy_ip'] = proxysource['https'].split(':')[1].replace('//','')
            proxy['https_proxy_port'] = proxysource['https'].split(':')[2].replace("/", "").replace("\n", "")
        except:
            logger.sendToLog('no https proxy detected', 'INFO')

        # get ftp proxy
        try:
            proxy['ftp_proxy_ip'] = proxysource['ftp'].split(':')[1].replace('//','')
            proxy['ftp_proxy_port'] = proxysource['ftp'].split(':')[2].replace("/", "").replace("\n", "")
        except:
            logger.sendToLog('no ftp proxy detected', 'INFO')

        # get socks proxy
        try:
            # if it is gnome or unity
            if desktop == 'GNOME' or desktop == 'Unity:Unity7' :
                socks_proxy = proxysource['all'].split(':')[1].replace('//','')
            # if it is Mac OS
            elif os_type == 'Darwin' :

                validKeys = ['SOCKSEnable']

                # get proxies list using scutil command and parse it in tmp list
                mac_tmp_proxies_list = {}
                proxyList = subprocess.run(['scutil', '--proxy'], stdout=subprocess.PIPE)
                for line in proxyList.stdout.decode('utf-8').split('\n'):
                    words = line.split()
                    if len(words) == 3 and words[0] in validKeys:
                        mac_tmp_proxies_list[words[0]] = words[2]

                if mac_tmp_proxies_list['SOCKSEnable'] is '1' :
                    socks_proxy = True
                else:
                    socks_proxy = False
            # others except KDE,Mac OS,gnome,unity7
            else:
                socks_proxy = proxysource['socks'].split(':')[1].replace('//','')
        except:
            socks_proxy = False

    # check if just socks proxy exists
    key_is_available = False
    key_list = ['http_proxy_ip', 'https_proxy_ip', 'ftp_proxy_ip']
    for key in key_list:
        if key in proxy.keys():
            key_is_available = True


    if not key_is_available and socks_proxy :
        # all print just for debugung
        socks_message = "persepolis and aria2 don't support socks\n\
        you must convert socks proxy to http proxy.\n\
        Please read this for more help:\n\
            https://github.com/persepolisdm/persepolis/wiki/Privoxy"
        print(socks_message)
        logger.sendToLog(socks_message, 'ERROR')

    # return results
    proxy_log_message = 'proxy: ' + str(proxy)
    logger.sendToLog(proxy_log_message, 'INFO')
    return proxy
