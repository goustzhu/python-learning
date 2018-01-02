#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# @Time    : 2018/1/2 17:57
# @Author  : goustzhu <goustzhu@gmail.com>
# @File    : hbase_connection.py
# @Github  : https://github.com/goustzhu
# @Software: PyCharm
from __future__ import division, print_function
import sys, os, time, datetime, warnings, logging
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.packages.hbase import THBaseService
from thrift.packages.hbase.ttypes import *

warnings.filterwarnings("ignore")
logger = logging.getLogger(__name__)

class NoConnectionsAvailable(RuntimeError):
    pass

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class ConnectionPool(object):

    DEFAULT_NETWORK_TIMEOUT = 0
    DEFAULT_POOL_SIZE = 100

    def __init__(self, host, port, iface_cls=THBaseService.Client, size=DEFAULT_POOL_SIZE, async=False, network_timeout=DEFAULT_NETWORK_TIMEOUT):
        self.host = host
        self.port = port
        self.iface_cls = iface_cls

        self.network_timeout = network_timeout
        self.size = size

        self._closed = False
        self._async = async
        if self._async:
            import gevent.queue
            try:
                from gevent import lock as glock
            except ImportError:
                # gevent < 1.0
                from gevent import coros as glock
            self._semaphore = glock.BoundedSemaphore(size)
            self._connection_queue = gevent.queue.LifoQueue(size)
            self._QueueEmpty = gevent.queue.Empty

        else:
            import threading
            import Queue
            self._semaphore = threading.BoundedSemaphore(size)
            self._connection_queue = Queue.LifoQueue(size)
            self._QueueEmpty = Queue.Empty

    def close(self):
        self._closed = True
        while not self._connection_queue.empty():
            try:
                conn = self._connection_queue.get(block=False)
                try:
                    self._close_thrift_connection(conn)
                except:
                    pass
            except self._QueueEmpty:
                pass

    def _create_thrift_connection(self):
        # socket = TSocket.TSocket(self.host, self.port)
        # if self.network_timeout > 0:
        #     socket.setTimeout(self.network_timeout)
        # transport = TTransport.TBufferedTransport(socket)
        # protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
        # connection = self.iface_cls(protocol)
        # transport.open()
        connection = Connection(self.host, self.port)
        connection.open()
        return connection

    def _close_thrift_connection(self, conn):
        try:
            # conn._iprot.trans.close()
            conn.close()
        except:
            logger.warn('warn: failed to close iprot trans on {%s}' % conn)
            pass
        try:
            # conn._oprot.trans.close()
            conn.close()
        except:
            logger.warn('warn: failed to close oprot trans on {%s}' % conn)
            pass

    def get_connection(self):
        """ get a connection from the pool. This blocks until one is available.
        """
        self._semaphore.acquire()
        if self._closed:
            raise RuntimeError('connection pool closed')
        try:
            return self._connection_queue.get(block=False)
        except self._QueueEmpty:
            try:
                return self._create_thrift_connection()
            except:
                self._semaphore.release()
                raise

    def return_connection(self, conn):
        """ return a thrift connection to the pool.
        """
        if self._closed:
            self._close_thrift_connection(conn)
            return
        self._connection_queue.put(conn)
        self._semaphore.release()

    def release_conn(self, conn):
        """ call when the connect is no usable anymore
        """
        try:
            self._close_thrift_connection(conn)
        except:
            pass
        if not self._closed:
            self._semaphore.release()

class Connection(object):

    def __init__(self, host, port, timeout=None, autoconnect=True):
        logger.info("build connection host=%s, port=%s" % (host, port))
        self.host = host
        self.port = port
        self.timeout = timeout
        self.transport = None
        self.client = None
        self.refresh_thrift_client()
        if autoconnect:
            self.open()

    def refresh_thrift_client(self):
        logger.info("refresh connection host=%s, port=%s" % (self.host, self.port))
        socket = TSocket.TSocket(self.host, self.port)

        if self.timeout:
            socket.setTimeout(self.timeout * 1000)

        transport = TTransport.TBufferedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = THBaseService.Client(protocol)
        self.transport = transport
        self.client = client

    def open(self):
        if self.transport.isOpen():
            return
        self.transport.open()

    def close(self):
        if not self.transport.isOpen():
            return
        self.transport.close()

    def get(self, table, rowkey):
        entity = None
        query = TGet(row=rowkey)
        result = self.client.get(table, query)
        if result:
            entity = FeatureEntity(rowkey)
            for columnValue in result.columnValues:
                dictV = columnValue.__dict__
                entity.put(str(str(dictV['family']) + ":" + str(dictV['qualifier'])), dictV['value'])
        return entity

    def getByFix(self, table, scan):
        entity = None
        result = self.client.getScannerResults(table, scan, 1)
        if result:
            for record in result:
                rowkey = record.row
                entity = FeatureEntity(rowkey)
                for columnValue in record.columnValues:
                    dictV = columnValue.__dict__
                    entity.put(str(str(dictV['family']) + ":" + str(dictV['qualifier'])), dictV['value'])
                break
        return entity

    def scan(self, table, scan, page=1, pagesize=20):
        result = []
        scannerid = self.client.openScanner(table, scan)
        flag = True
        index = 1
        while flag:
            result = self.client.getScannerRows(scannerid, pagesize)
            if not result:
                break
            if index==page:
                break
        if result:
            for record in result:
                rowkey = record.row
                entity = FeatureEntity(rowkey)
                for columnValue in record.columnValues:
                    dictV = columnValue.__dict__
                    entity.put(str(str(dictV['family']) + ":" + str(dictV['qualifier'])), dictV['value'])
                result.append(entity)
        return result

    def scanNumber(self, table, scan, pagesize=5000):
        results = 0
        scannerid = self.client.openScanner(table, scan)
        # print("scannerid=%s" % (scannerid))
        flag = True
        while flag:
            result = self.client.getScannerRows(scannerid, pagesize)
            # print("\tresult=%s" % (result))
            if result:
                results += len(result)
            else:
                flag = False
        return results

class FeatureEntity(object):
    def __init__(self, rowkey):
        self.rowkey = rowkey
        self.map_features = {}

    def put(self, key, value):
        self.map_features[key] = value

    def putCF(self, family, quor, value):
        key = "%s:%s" % (family, quor)
        self.put(key, value)

    def get(self, key):
        return self.map_features.get(key, "")

    def getCF(self, family, quor):
        key = "%s:%s" % (family, quor)
        return self.get(key)

    def getByFamliy(self, family):
        map_vs = {}
        for keys in self.map_features:
            if keys.startswith(family):
                map_vs[keys] = self.map_features.get(keys)
        return map_vs

    def getByFamilys(self, familys):
        map_vs = {}
        for keys in self.map_features:
            kf = keys[:keys.find(":")]
            if kf in familys:
                map_vs[keys] = self.map_features.get(keys)
        return map_vs

    def __str__(self):
        map_vs = ""
        for key in self.map_features:
            map_vs += ", "+key+"="+self.map_features.get(key)
        return "rowkey=%s%s" % (self.rowkey, map_vs)

