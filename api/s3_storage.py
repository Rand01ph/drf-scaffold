#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Rand01ph on 2019/4/30

import os
import posixpath
from tempfile import SpooledTemporaryFile
import logging
import yaml

from boto.s3.connection import S3Connection, Location
from boto.exception import S3CreateError, S3ResponseError

from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "config.yaml"), 'r') as conf_file:
    cfg = yaml.load(conf_file)

object_based_storage = cfg['OBJECT_BASED_STORAGE']

ACCESS_KEY = object_based_storage['ACCESS_KEY']
SECRET_KEY = object_based_storage['SECRET_KEY']
S3_HOST = object_based_storage['S3_HOST']
S3_BUCKET = object_based_storage['S3_BUCKET']
S3_CALLING_FORMAT = object_based_storage['S3_CALLING_FORMAT']
S3_LOCATION = object_based_storage['S3_LOCATION']

logger = logging.getLogger(__name__)


@deconstructible
class S3Storage(Storage):
    """
    try to implementation a attachment storage over S3
    """

    def __init__(self, s3_bucket_name=None, s3_access_key=None, s3_secret_key=None,
                 s3_host=None, s3_calling_format=None, is_secure=False, location=None):

        self.s3_access_key = s3_access_key or ACCESS_KEY
        self.s3_secret_key = s3_secret_key or SECRET_KEY
        self.s3_host = s3_host or S3_HOST
        self.s3_bucket_name = s3_bucket_name or S3_BUCKET
        self.is_secure = is_secure
        self.s3_calling_format = s3_calling_format or S3_CALLING_FORMAT
        self.location = location or S3_LOCATION
        # connect to S3
        connection_kwargs = {
            "calling_format": self.s3_calling_format
        }
        connection_kwargs["aws_access_key_id"] = self.s3_access_key
        connection_kwargs["aws_secret_access_key"] = self.s3_secret_key
        connection_kwargs["host"] = self.s3_host
        connection_kwargs["is_secure"] = self.is_secure
        self.s3_connection = S3Connection(**connection_kwargs)
        try:
            self.bucket = self.s3_connection.create_bucket(self.s3_bucket_name,
                                                           location=getattr(Location, self.location))
        except (S3CreateError, S3ResponseError):
            self.bucket = self.s3_connection.get_bucket(self.s3_bucket_name, validate=False)
        # ok
        super(S3Storage, self).__init__()

    def _temporary_file(self):
        """
        Creates a temporary file.
        We need a lot of these, so they are tweaked for efficiency.
        """
        return SpooledTemporaryFile(max_size=1024 * 1024 * 20)  # 20 MB.

    def get_valid_name(self, name):
        return posixpath.normpath(name.replace(os.sep, "/"))

    def _generate_url(self, name):
        """
        Generates a URL to the given file.
        Authenticated storage will return a signed URL. Non-authenticated
        storage will return an unsigned URL, which aids in browser caching.
        """
        return self.s3_connection.generate_url(expires_in=3600,
                                               method="GET",
                                               bucket=self.s3_bucket_name,
                                               key=name,
                                               query_auth=True,
                                               force_http=True)

    def _get_key(self, name, validate=False):
        return self.bucket.get_key(name, validate=validate)

    def _open(self, name, mode="rb"):
        if (mode != "rb"):
            raise ValueError("S3 files can only be opened in read-only mode")
        # Load the key into a temporary file. It would be nice to stream the
        # content, but S3 doesn't support seeking, which is sometimes needed.
        key = self._get_key(name)
        content = self._temporary_file()
        try:
            key.get_contents_to_file(content)
        except S3ResponseError:
            raise IOError("File {name} does not exist".format(name=name, ))
        content.seek(0)
        # All done!
        return File(content, name)

    def _save(self, name, content):
        # Save the file.
        if self.exists(name):
            raise IOError('File already exists and can\'t be replaced')
        else:
            try:
                self._get_key(name).set_contents_from_file(content,
                                                           replace=False)
            except Exception as e:
                raise IOError('Error during uploading file')
        # self._get_key(name).set_canned_acl('public-read')
        # Return the name that was saved.
        return name

    def delete(self, name):
        """
        Deletes the specified file from the storage system.
        """
        self._get_key(name).delete()

    def exists(self, name):
        """
        Returns True if a file referenced by the given name already exists in the
        storage system, or False if the name is available for a new file.
        """
        # We also need to check for directory existence, so we'll list matching
        # keys and return success if any match.
        return self.bucket.new_key(name).exists()

    def listdir(self, path):
        """
        Lists the contents of the specified path, returning a 2-tuple of lists;
        the first item being directories, the second item being files.
        """
        # Normalize directory names.
        if path and not path.endswith("/"):
            path += "/"
        # Look through the paths, parsing out directories and paths.
        files = set()
        dirs = set()
        for key in self.bucket.list(prefix=path, delimiter="/"):
            key_path = key.name[len(path):]
            if key_path.endswith("/"):
                dirs.add(key_path[:-1])
            else:
                files.add(key_path)
        # All done!
        return list(dirs), list(files)

    def size(self, name):
        """
        Returns the total size, in bytes, of the file specified by name.
        """
        return self._get_key(name, validate=True).size

    def url(self, name):
        """
        Returns an absolute URL where the file's contents can be accessed
        directly by a Web browser.
        """
        return self._generate_url(name)
