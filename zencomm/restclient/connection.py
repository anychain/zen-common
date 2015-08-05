import time
import socket
import random
import threading
import httplib
import traceback
import json
from zencomm.log import logger
from duplicity.path import Path


class ConnectionQueue(object):
    ''' http connection queue '''

    def __init__(self, timeout=60):
        self.queue = []
        self.timeout = timeout

    def size(self):
        ''' return the size of connection queue '''
        return len(self.queue)

    def get_conn(self):
        '''
        @return: a valid connection or None
        '''
        for _ in range(len(self.queue)):
            (conn, _) = self.queue.pop(0)
            if self._is_conn_ready(conn):
                return conn
            else:
                self.put_conn(conn)
        return None

    def put_conn(self, conn):
        ''' insert a valid conn into queue
        '''
        self.queue.append((conn, time.time()))

    def clear(self):
        ''' clear expired connections
        '''
        while len(self.queue) > 0 and self._is_conn_expired(self.queue[0]):
            self.queue.pop(0)

    def _is_conn_expired(self, conn_info):
        ''' check whether connection expired
        '''
        (_, time_stamp) = conn_info
        return (time.time() - time_stamp) > self.timeout

    def _is_conn_ready(self, conn):
        """
        sometimes the response may not be remove after read at
        lasttime's connection
        """
        response = getattr(conn, '_HTTPConnection__response', None)
        return (response is None) or response.isclosed()


class ConnectionPool(object):
    ''' http connection pool for multiple hosts
        it is thread-safe
    '''

    CLEAR_INTERVAL = 5.0

    def __init__(self, timeout=60):
        self.timeout = timeout
        self.last_clear_time = time.time()
        self.lock = threading.Lock()
        self.pool = {}

    def size(self):
        ''' return the size of connection pool '''
        with self.lock:
            size = 0
            for k in self.pool:
                size += self.pool[k].size()
        return size

    def put_conn(self, host, is_secure, conn):
        ''' put connection into host's connection pool
        '''
        with self.lock:
            key = (host, is_secure)
            if key not in self.pool:
                self.pool[key] = ConnectionQueue(self.timeout)

            self.pool[key].put_conn(conn)

    def get_conn(self, host, is_secure):
        ''' get connection from host's connection pool
            @return: a valid connection or None
        '''
        self._clear()
        with self.lock:
            key = (host, is_secure)
            if key not in self.pool:
                return None
            return self.pool[key].get_conn()

    def _clear(self):
        ''' clear expired connections of all hosts
        '''
        with self.lock:
            curr_time = time.time()
            if (self.last_clear_time + self.CLEAR_INTERVAL) > curr_time:
                return
            key_to_delete = []
            for key in self.pool:
                self.pool[key].clear()
                if self.pool[key].size() == 0:
                    key_to_delete.append(key)
            for key in key_to_delete:
                del self.pool[key]
            self.last_clear_time = curr_time


class HTTPRequest(object):

    def __init__(self, method, protocol, header, host, port, path,
                 params, body={}):
        """Represents an HTTP request.
        @param method - The HTTP method name, 'GET', 'POST', 'PUT' etc.
        @param protocol - 'http' or 'https'
        @param header - http request header
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param path - URL path that is being accessed.
        @param auth_path - The part of the URL path used when creating the
                         authentication string.
        @param params - HTTP url query parameters, {'name':'value'}.
        @param body - Body of the HTTP request. If not present, will be None or
                     empty string ('').
        """
        self.method = method
        self.protocol = protocol
        self.headers = header
        self.host = host
        self.port = port
        self.path = path
        self.auth_path = path
        self.params = params
        self.body = body

    def __str__(self):
        return (('method:(%s) protocol:(%s) header(%s) host(%s) '
                 'port(%s) path(%s) params(%s) body(%s)')
                % (self.method, self.protocol, self.headers,
                   self.host, str(self.port),
                   self.path, self.params, self.body))

    def authorize(self, connection, **kwargs):
        ''' add authorize information to request '''
        connection._auth_handler.add_auth(self, **kwargs)


class RestClient(object):
    ''' This connection will be used to connect to rest service
    '''

    def __init__(self, host, port, protocol, pool=None, msg_time_out=10,
                 http_socket_timeout=10):
        '''
        @param pool - the connection pool
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - protocol to access to web server, "http" or "https"
        @param msg_time_out - the time_out of message
        @param retry_time - the retry_time when message send fail
        '''
        self.host = host
        self.port = port
        self.protocol = protocol
        self.secure = True if self.protocol.lower() == "https" else False
        self._conn = pool if pool else ConnectionPool()
        self.msg_time_out = msg_time_out
        self.http_socket_timeout = http_socket_timeout
        pass

    def _get_conn(self):
        ''' get connection from pool '''
        conn = self._conn.get_conn(self.host, self.secure)
        if conn is None:
            conn = self._new_conn()
        return conn

    def _set_conn(self, conn):
        ''' set valid connection into pool '''
        self._conn.put_conn(self.host, self.secure, conn)

    def _new_conn(self):
        ''' create a new connection '''
        if self.secure:
            return httplib.HTTPSConnection(self.host, self.port,
                                           timeout=self.http_socket_timeout)
        else:
            return httplib.HTTPConnection(self.host, self.port,
                                          timeout=self.http_socket_timeout)

    def send_request(self, path, params, method='GET', retry_time=3):
        '''
            @param parms: dict user request
            @return: response from user, json
        '''
        if path[-1] != '/':
            path = path + '/'
        conn = self._get_conn()
        retry_cnt = 0
        while retry_cnt < retry_time:
            # Use binary exponential backoff to desynchronize client requests
            next_sleep = random.random() * (2 ** retry_cnt) * 0.1
            try:
                if isinstance(params, dict):
                    params = json.dumps(params)
                # request.authorize(self)
                conn.request(method, path, params,
                             {"Content-Type": "application/json"})

                response = conn.getresponse()

                if response.status in [200, 201, 204]:
                    self._set_conn(conn)
                    return response.read()
                else:
                    # if retcode and retbody in reply,
                    # the connection is successful
                    rest_reply = response.read()
                    if rest_reply.find('retbody') != -1:
                        return rest_reply
                    # log error and retry
                    logger.error("Request failed with status: %d, error: %s "
                                 % (response.status, rest_reply))
                    conn = self._get_conn()
            except Exception, e:
                # only retry for timeout error
                # print traceback.format_exc()
                if isinstance(e, socket.timeout):
                    logger.error("timeout for request")
                    logger.exception(e)
                    return None
                logger.error("restclient request failed with exception %s" % e)
                logger.exception(e)
                conn = self._get_conn()
            retry_cnt += 1
            # do not sleep for the first 2 retries
            if retry_cnt <= 2:
                continue
            time.sleep(next_sleep)
            logger.warn("retry request for [%d] time after sleep [%.2f] secs"
                        % (retry_cnt, next_sleep))

        logger.error("send request failed after retry for [%d] times"
                     % (retry_cnt))
        return None
