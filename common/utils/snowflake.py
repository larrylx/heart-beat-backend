# Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
# https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

# Modify from https://www.pythonf.cn/read/86025 and https://www.yuque.com/kaixiang-jinoo/gtspek/mft5gx

import time
# import logging

# 64-bit ID division
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# Maximum value calculation
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# Shift offset calculation
WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# Sequence Mask
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# Twitter timestamp
TWEPOCH = 1288834974657


# logger = logging.getLogger('flask.app')


class IdWorker(object):
    """
    Generate distributed ID
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        Initialization
        :param datacenter_id:
        :param worker_id:
        :param sequence:
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id out of range')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id out of range')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        # Time stamp of last id generation
        self.last_timestamp = -1

    def _gen_timestamp(self):
        """
        Generate int timestamp
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def get_id(self):
        """
        Produce ID
        :return: id
        """
        timestamp = self._gen_timestamp()

        # Clock Back
        # Approach 1: Wait until last time stamp
        # while timestamp < self.last_timestamp:
        #     logging.error('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
        #     print('Clock Back')
        #     timestamp = self._gen_timestamp()

        # Approach 2: Use last time stamp
        timestamp = max(timestamp, self.last_timestamp)

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << DATACENTER_ID_SHIFT) | \
                 (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        Wait until next ms
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

# Test
# if __name__ == '__main__':
#     worker = IdWorker(1, 2, 0)
#     print(worker.get_id())
