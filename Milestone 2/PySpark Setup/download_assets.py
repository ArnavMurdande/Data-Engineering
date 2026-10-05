import os
import urllib.request
import ssl

ssl_context = ssl._create_unverified_context()

base_dir = os.path.dirname(os.path.abspath(__file__))
hadoop_bin = os.path.join(base_dir, "hadoop", "bin")
jars_dir = os.path.join(base_dir, "jars")

os.makedirs(hadoop_bin, exist_ok=True)
os.makedirs(jars_dir, exist_ok=True)

downloads = [
    # Winutils
    ("https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.6/bin/winutils.exe",
     os.path.join(hadoop_bin, "winutils.exe")),
    ("https://github.com/cdarlint/winutils/raw/master/hadoop-3.3.6/bin/hadoop.dll",
     os.path.join(hadoop_bin, "hadoop.dll")),
    # MySQL Connector/J JDBC Driver JAR
    ("https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.4.0/mysql-connector-j-8.4.0.jar",
     os.path.join(jars_dir, "mysql-connector-j-8.4.0.jar"))
]

for url, target in downloads:
    if os.path.exists(target) and os.path.getsize(target) > 1000:
        print(f"Already exists: {target} ({os.path.getsize(target)} bytes)")
        continue
    print(f"Downloading {url} -> {target}...")
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, target)
    print(f"Downloaded successfully: {target} ({os.path.getsize(target)} bytes)")

print("All dependencies downloaded!")
