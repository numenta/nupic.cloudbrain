# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""
Pika (python rabbitMQ client) based implementation of a record stream
"""

from cloudbrain.listeners.pika_subscriber import PikaSubscriber

from nupic.data.record_stream import RecordStreamIface

_DEVICE_ID = "my_device"
_DEVICE_NAME = "muse"
_HOST = "localhost"


class PikaRecordStream(RecordStreamIface):
  """ 
  Pika based RecordStream implementation
  """
 
  def __init__(self):
    
    super(PikaRecordStream, self).__init__()
    
    # keep track of how many records have been streamed
    self._recordCount = 0
    self.subscriber = PikaSubscriber(_DEVICE_NAME, _DEVICE_ID, _HOST)
    self.subscriber.connect()

    
    
  def getNextRecord(self, useCache=True):
    """ 
    Returns next available data record 
   
    """
    record = self.subscriber.get_one_message()
    return record
  
  
  def close(self):
    raise NotImplementedError("not implemented")

  def rewind(self):
    raise NotImplementedError("You can't rewind when subscribing to a message queue")


  def getRecordsRange(self, **kwargs):
    raise NotImplementedError("not implemented")


  def getLastRecords(self, numRecords):
    raise NotImplementedError("not implemented")


  def removeOldData(self):
    raise NotImplementedError("not implemented")

  def appendRecord(self, record, inputBookmark=None):
    raise NotImplementedError("not implemented")

  def appendRecords(self, records, inputRef=None, progressCB=None):
    raise NotImplementedError("not implemented")


  def getBookmark(self):
    raise NotImplementedError("not implemented")


  def recordsExistAfter(self, bookmark):
   return True # we are continually listening for messages

  def seekFromEnd(self, numRecords):
    raise NotImplementedError("not implemented")

  def getStats(self):
    raise NotImplementedError("not implemented")

  def clearStats(self):
   raise NotImplementedError("not implemented")

  def getError(self):
    raise NotImplementedError("not implemented")

  def setError(self, error):
   raise NotImplementedError("not implemented")

  def isCompleted(self):
    raise NotImplementedError("not implemented")
  

  def setCompleted(self, completed=True):
    raise NotImplementedError("not implemented")
  
  
  def getFieldNames(self):
    raise NotImplementedError("not implemented")
  
  def getFields(self):
    raise NotImplementedError("not implemented")

  def getNextRecordIdx(self):
    """
    Returns the index of the record that will be read next from getNextRecord()
    """
    return self._recordCount


  def setTimeout(self, timeout):
    raise NotImplementedError("not implemented")


  def flush(self):
    raise NotImplementedError("not implemented")



