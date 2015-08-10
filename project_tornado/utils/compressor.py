# -*- coding:utf-8 -*-

# @version: 1.0
# @author: Zhipeng Zhang
# @date: '2015/04/07'
import logging
import os
import zlib
import subprocess

from project_tornado.utils.enum import Enum


class ENUM_COMPRESS(Enum):
    zip = "zip"
    tar = "tar"
    gz = "gz"
    zlib = "zlib"


class ENUM_SOURCE_TYPE(Enum):
    text = "text"
    file = "file"


class Compressor(object):
    def __init__(self):
        self._decompress_start = "un"

    def compress(self, content, is_file=False, compress_type=ENUM_COMPRESS.zlib,
                 source_type=ENUM_SOURCE_TYPE.text, save_dir="."):
        if source_type == ENUM_SOURCE_TYPE.text:
            if is_file:
                with file(content)as f:
                    text = f.read()
            else:
                text = content

            compress_method = getattr(self, compress_type + "_" + source_type)
            try:
                content_compressed = compress_method(text)
                return content_compressed
            except TypeError:
                logging.error("压缩错误，没有找到对应压缩方式:%s" % compress_type)
                return -1
        elif source_type == ENUM_SOURCE_TYPE.file:
            pass
        else:
            logging.error("source_type must is 'text' or 'file'.")
            return False

    def un_compress(self, content, is_file=False, compress_type=ENUM_COMPRESS.zlib,
                    source_type=ENUM_SOURCE_TYPE.text, save_dir=".", delete_source=False):
        compress_method_name = self._decompress_start + compress_type + "_" + source_type
        compress_method = getattr(self, self._decompress_start + compress_type + "_" + source_type)
        if not compress_method:
            logging.error("解压失败，没有找到对应压缩方式:%s" % compress_method_name)
            return -1
        if source_type == ENUM_SOURCE_TYPE.text:
            if is_file:
                with file(content)as f:
                    text = f.read()
            else:
                text = content
            try:
                content_compressed = compress_method(text)
                return content_compressed
            except Exception, e:
                logging.error("解压失败，compress_method_name:%s, Error:%s" % (compress_method_name, e))
                return -1
        elif source_type == ENUM_SOURCE_TYPE.file:
            try:
                content_compressed = compress_method(content, save_dir, delete_source)
                return content_compressed
            except Exception, e:
                logging.error("解压失败，compress_method_name:%s, Error:%s" % (compress_method_name, e))
                return -1

        else:
            logging.error("source_type must is 'text' or 'file'.")
            return False

    def zip_text(self, content):
        return content

    def unzip_text(self, content):
        return content

    def zip_file(self):
        pass

    def unzip_file(self, file_path=None, save_dir=".", delete_source=False):
        if not file_path or not os.path.isfile(file_path):
            logging.error("解压文件异常，file_path:%s 不存在或为空" % file_path)
            return False
        kwargs = {"file_path": file_path, "save_dir": save_dir}
        if delete_source:
            shell = "unzip -o %(file_path)s -d %(save_dir)s && rm %(file_path)s " % kwargs
        else:
            shell = "unzip -o %(file_path)s -d %(save_dir)s " % kwargs
        try:

            subprocess.Popen(shell, shell=True)
            return True
        except Exception, e:
            logging.error("解压文件异常， Error:%s" % e)
            return False

    def zlib_text(self, content):
        return zlib.compress(content)

    def unzlib_text(self, content):
        return zlib.decompress(content)

    def tar_text(self, content):
        return content

    def untar_text(self, content):
        return content

    def gz_text(self, content):
        return content

    def ungz_text(self, content):
        return content


if __name__ == "__main__":
    sostr = "Hello,测试压缩..."
    compress = Compressor()
    enstr = compress.compress(sostr)
    print sostr, "\n==>\n", enstr
    print "--------------------------------------"
    destr = compress.un_compress(enstr)
    print enstr, "\n==>\n", destr
