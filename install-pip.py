#!/usr/bin/python
import tempfile
import urllib
import shutil
import os
import subprocess
import tarfile
import zipfile
import fnmatch

setuptools_url="https://pypi.python.org/packages/84/24/610d8bb87219ed6d0928018b7b35ac6f6f6ef27a71ed6a2d0cfb68200f65/setuptools-24.0.3.tar.gz"
setuptools_version="setuptools-24.0.3"
pip_url="https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz"
pip_version="pip-8.1.2"
python27_url='https://codeload.github.com/dr1s/python-2.7/zip/master'

hdd='/DataVolume'
python_dir=os.path.join(hdd,'python')

def download_file(url, folder, file_name=None):
    if not file_name:
        file_name = url.split('/')[-1]
    urllib.urlretrieve (url, os.path.join(folder,file_name))

def extract_archives(folder):
    tar_files = fnmatch.filter(os.listdir(folder), '*.tar.gz')
    for file in tar_files:
        x = tarfile.open(os.path.join(folder,file))
        x.extractall(path=folder)
        x.close()
    zip_files = fnmatch.filter(os.listdir(folder), '*.zip')
    for file in zip_files:
        z = zipfile.ZipFile(os.path.join(folder,file))
        z.extractall(path=folder)
        z.close


def main():
    tmpdir = None
    try:
        tmpdir = tempfile.mkdtemp()
        print('Downloadinging files')
        download_file(setuptools_url, tmpdir)
        download_file(pip_url, tmpdir)
        download_file(python27_url, tmpdir, 'python27.zip')

        extract_archives(tmpdir)

        if not os.path.exists(python_dir):
            os.makedirs(python_dir)

        setuptools_dir = os.path.join(tmpdir, setuptools_version)
        setuptools_setup = os.path.join(setuptools_dir, 'setup.py')
        pip_dir = os.path.join(tmpdir, pip_version)
        pip_setup = os.path.join(pip_dir, 'setup.py')
        python27_dir = os.path.join(tmpdir,'python-2.7-master')

        args = ['python', setuptools_setup, 'install']

        print('Installing setuptools')
        devnull = open(os.devnull, 'w')
        subprocess.call(args, stdout=devnull, stderr=subprocess.STDOUT)

        print('Installing pip')
        args[1] = pip_setup
        os.chdir(pip_dir)
        subprocess.call(args, stdout=devnull, stderr=subprocess.STDOUT)

        print('Installing xml-Module from python-2.7')
        site_packages='/usr/lib/python2.7/site-packages/xml'
        if not os.path.exists(site_packages):
            python27_xml = os.path.join(python27_dir,os.path.join('Lib','xml'))
            shutil.copytree(python27_xml, site_packages)

    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)



if __name__ == "__main__":
    main()
