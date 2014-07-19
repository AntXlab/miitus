from __future__ import absolute_import
from celery import shared_task
from ..utils import return_exception
from ..core import Core
from ..exceptions import WorkerIdInitFailed
from ..models import Worker
from datetime import datetime
from miitus import defs
import time, uuid


c = Core()
seqs = [0] * defs.SEQ_MAX
wid = 0

def get_wid():
    global wid, seqs, wid

    if not wid:
        salt = c.random()
        while True:
            id = c.random(scale=(1 << 16) - 1)
            # check if this id is already used.
            exist = Worker.objects(id=id).first()
            if exist:
                continue

            # create a record
            Worker.create(id=id, salt=salt)

            # sleep a while
            time.sleep(1)

            # make sure we are the owner of that record
            back_check = Worker.objects(id=id).first()
            if back_check.salt == salt:
                wid = id
                break

    return wid
 

@shared_task
def gen_dist_uuid(resource):
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
    global seqs

    if resource >= defs.SEQ_MAX:
        raise ValueError('receive resource-id: ' + str(resource) +\
                ', when max resource-id is:' + str(defs.SEQ_MAX))

    wid_local = get_wid()
    if not wid_local:
        raise WorkerIdInitFailed()

    while True:
        # see if we need to reset
        t = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
        if seqs[defs.SEQ_TIMESTAMP] != t:
            seqs = [0] * defs.SEQ_MAX
            seqs[defs.SEQ_TIMESTAMP] = t

        seqs[resource] = seq = seqs[resource] + 1
        if seq > defs.MAX_SEQ_NUM:
            time.sleep(1)
            continue

        # compose uuid
        id = wid_local | (seq << 80) | (t << 96)
        break 

    return uuid.UUID(int=id)

