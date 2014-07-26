from __future__ import absolute_import
from celery.contrib.methods import task
from celery.signals import worker_shutdown
from ..core import Runtime
from ..utils import Config, Singleton
from ..exc import WorkerIdInitFailed
from ..models.cql import Worker
from datetime import datetime
from miitus import const
import time, uuid


rt = Runtime()
conf = Config()


class GenDistUUID(Singleton):
    """
    Shortern solution for generating distributed UUID.
    Replace with ZooKeeper is not worked.
    """

    def __init__(self):
        self.seqs = [0] *const.SEQ_MAX
        self.__wid = 0

        worker_shutdown.connect(self.release_wid)

    def __get_wid(self):
        """
        get worker id
        """
        global conf

        if not self.__wid:
            salt = rt.random()
            while True:
                id = rt.random(scale=(1 << 16) - 1)
                # check if this id is already used.
                exist = Worker.objects(id=id).first()
                if exist:
                    continue

                # create a record
                Worker.create(id=id, salt=salt)

                # sleep a while
                time.sleep(conf.WORKER_GET_ID_INTERVAL)

                # make sure we are the owner of that record
                back_check = Worker.objects(id=id).first()
                if back_check.salt == salt:
                    self.__wid = id
                    break

        return self.__wid

    def __reset_seqs(self, t):
        """
        check to see if we need to reset sequence array
        """
        if self.seqs[const.SEQ_TIMESTAMP] != t:
            self.seqs = [0] * const.SEQ_MAX
            self.seqs[const.SEQ_TIMESTAMP] = t

    def release_wid(self, **kwargs):
        """
        release worker id
        """
        if self.__wid == 0:
           return 

        Worker.objects(id=self.__wid).delete()

    @task(name='GenDistUUID.gen_dist_uuid')
    def gen_dist_uuid(self, resource):
        """
        generate universal unique uuid. refer to link below for more details

            http://srinathsview.blogspot.tw/2012/04/generating-distributed-sequence-number.html

        ret: 128bit uuid
        format: |-- timestamp --|-- sequence number --|-- worker id--|
            timestamp: 32bit
            seq: 80bit
            worker: 16bit

        ret: 128 bit id
        """
        if resource >= const.SEQ_MAX:
            raise ValueError('receive resource-id: ' + str(resource) +\
                ', when max resource-id is:' + str(const.SEQ_MAX))

        wid_local = self.__get_wid()
        if not wid_local:
            raise WorkerIdInitFailed()

        while True:
            # see if we need to reset
            t = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
            self.__reset_seqs(t)

            self.seqs[resource] = seq = self.seqs[resource] + 1
            if seq > const.MAX_SEQ_NUM:
                time.sleep(1)
                continue

            # compose uuid
            id = wid_local | (seq << 80) | (t << 96)
            break 

        return uuid.UUID(int=id)

