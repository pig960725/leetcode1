import time
import logging

class InvalidSystemClock(Exception):
    pass


# 64位ID的划分
WORKER_ID_BITS = 5  # 机器id
DATACENTER_ID_BITS = 5  # 数据标识id
SEQUENCE_BITS = 12  # 12位序列号

# 最大值计算
MAX_WORKED_ID = -1 ^ (-1 << WORKER_ID_BITS)
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# 移位偏移计算
WORK_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS
# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)
# Twitter 元年时间戳
TWEPOCH = 1288834974657



class idworker():

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        :param datacenter_id:  数据中心(机器区域)id
        :param worker_id:  设备id
        :param sequence: 真实序号
        """
        if worker_id > MAX_WORKED_ID or worker_id < 0 :
            raise ValueError('worker_ID 值越界')
        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0 :
            raise ValueError('datacenter_id 值越界')
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1 # 上次计算的时间戳

    def _gen_timestamp(self):
        return int(time.time()*1000)

    def get_id(self):
        timestamp = self._gen_timestamp()

        if timestamp < self.last_timestamp:
            logging.error('clock is moving backwards. Rejecting request until {}'.format(self.last_timestamp))
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

        self.last_timestamp = timestamp
        new_id = ((timestamp-TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) |\
                 (self.worker_id << WORK_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_stamp):
        timestamp = self._gen_timestamp()
        while timestamp <= last_stamp:
            timestamp = self._gen_timestamp()
        return timestamp



