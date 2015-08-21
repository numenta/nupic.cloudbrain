_DEVICE_ID = "my_device"
_DEVICE_NAME = "muse"
_HOST = "localhost"
_BUFFER_SIZE = 100
_TRAINING_SET_SIZE = 6440
_NUM_RECORDS = 12728

_NUMBER_OF_LABELS = 3 # meditate, concentrate, normal
_CLASSIFICATION_FEATURES = ['metric']

_VERBOSITY = 0

_SCALAR_ENCODER_PARAMS = {
    "name": "metric",
    "fieldname": "metric",
    "type": "ScalarEncoder",
    "n": 256,
    "w": 21,
    "minval": None, # needs to be initialized after file introspection
    "maxval": None  # needs to be initialized after file introspection
}

_CATEGORY_ENCODER_PARAMS = {
    "name": 'label',
    "w": 21,
    "categoryList": range(_NUMBER_OF_LABELS)
}


_TRAINING_SET_FILE = 'training_data.csv'

import os
import csv
import copy

from classifier import Classifier
from nupic.data.file_record_stream import FileRecordStream
from htm.classification_network import createNetwork
from pika_record_stream import PikaRecordStream

class HTMSequenceClassifier(Classifier):
  
  def __init__(self, device_name, device_id, host, training_set_file):
    
    super(HTMSequenceClassifier, self).__init__(device_name, device_id, host)
    self.network = None
    self.csv_reader = None
    self.training_set_file = training_set_file
    self.liveDataSource = None
    

  
  def initialize(self):
    
    self.csv_reader = csv.reader(open(self.training_set_file, 'rb'))
    headers = self.csv_reader.next() # header
    self.csv_reader.next() # these are the NuPIC data types
    self.csv_reader.next() # these are NuPIC flags
    
    encoders = {}
    for metric in headers[:-1]: # last metric is the label, so we don't care about the min/max
      minval, maxval = self._find_min_max(self.training_set_file, metric)
      encoders[metric] = self._setup_scalar_encoder(minval, maxval)


    # Create network with a training data source. 
    # Test data will be streamed separately later during the 'classify' phase.
    #   - Input data comes from a CSV file (scalar values, labels). The
    #   - RecordSensor region allows us to specify a file record stream as the
    #     input source via the dataSource attribute.
    fileDataSource = FileRecordStream(streamID=self.training_set_file)
    
    self.liveDataSource = PikaRecordStream()
   
    #TODO: pass live source  too
    self.network = createNetwork((fileDataSource, "py.RecordSensor", "py.SequenceClassifierRegion", encoders))

    # Need to init the network before it can run.
    self.network.initialize()
    print '-> HTM network initialized ...'
  

  
  def train(self):
    """
    
    :return:
    """
    sensorRegion = self.network.regions["sensor"]
    spatialPoolerRegion = self.network.regions["SP"]
    temporalMemoryRegion = self.network.regions["TM"]
    classifierRegion = self.network.regions["classifier"]
    
    print '-> Training Spatial Pooler ...'
    for i in xrange(_TRAINING_SET_SIZE):
      # Run the network for a single iteration
      self.network.run(1)
  
      # SP has been trained. Now start training the TM too.
      if i == _TRAINING_SET_SIZE * 1/3:
        print '-> Training Temporal Memory ...'
        temporalMemoryRegion.setParameter("learningMode", True)
  
      # Start training the classifier as well.
      elif i == _TRAINING_SET_SIZE * 2/3:
        print '-> Training CLA Classifier ...'
        classifierRegion.setParameter("learningMode", True)
        self._run_classifier(sensorRegion, temporalMemoryRegion, classifierRegion, i)
        
  
    # stop the training
    spatialPoolerRegion.setParameter("learningMode", False)
    temporalMemoryRegion.setParameter("learningMode", False)
    classifierRegion.setParameter("learningMode", False)
    print '-> Training completed :-)'
  
     
  def classify(self):
    """
    
    :return:
    """
    

    self.subscriber.connect()
    self.subscriber.consume_messages(self.liveDataSource.consume_message)
    while 1:
      self.network.run(1)

    
    sensorRegion = self.network.regions["sensor"]
    temporalMemoryRegion = self.network.regions["TM"]
    classifierRegion = self.network.regions["classifier"]
    
    print "== Stating to predict Tom's state of mind: 0 is normal, 1 is meditation =="
    
    for i in xrange(_NUM_RECORDS - _TRAINING_SET_SIZE):
    
      clResults = self._run_classifier(sensorRegion, temporalMemoryRegion, classifierRegion, _TRAINING_SET_SIZE + i)

      inferredValue = clResults["actualValues"][clResults[int(classifierRegion.getParameter("steps"))].argmax()]
      
      print "predicted state: %s"  %inferredValue  

  def _run_classifier(self, sensorRegion, temporalMemoryRegion, classifierRegion, recordNum):
    actualValue = sensorRegion.getOutputData("categoryOut")[0]
    bucketIdx = actualValue

    classificationIn = {"bucketIdx": int(bucketIdx),
                        "actValue": int(actualValue)}

    # List the indices of active cells (non-zero pattern)
    activeCells = temporalMemoryRegion.getOutputData("bottomUpOut")
    patternNZ = activeCells.nonzero()[0]

    # Call classifier
    clResults = classifierRegion.getSelf().customCompute(
        recordNum=recordNum, patternNZ=patternNZ, classification=classificationIn)
    
    return clResults


  def load_model(self):
    """
    
    :return:
    """
    
  def save_model(self):
    """
    
    :return:
    """
    
  def _setup_scalar_encoder(self, minval, maxval):
    
    scalar_encoder_params = copy.deepcopy(_SCALAR_ENCODER_PARAMS)
    # Set min and max for scalar encoder params.
    scalar_encoder_params["minval"] = minval
    scalar_encoder_params["maxval"] = maxval 
    
    return scalar_encoder_params
  
  def _find_min_max(self, file_name, metric_name):
  
    # get the scalar values
    values = []
    with open(file_name, 'rU') as inputFile:
      csvReader = csv.reader(inputFile)
      headers = csvReader.next()
      
      # skip the rest of the header rows
      csvReader.next()
      csvReader.next()
      
      if metric_name not in headers:
        raise IncorrectHeadersException("metric name '%s' is not in headers '%s'" %(metric_name,headers))
    
      for line in csvReader:
        values.append(float(line[headers.index(metric_name)]))
        
  
    return min(values), max(values)
      

class IncorrectHeadersException(Exception):
  pass

if __name__ == "__main__":
  
  classifier = HTMSequenceClassifier(_DEVICE_NAME, _DEVICE_ID, _HOST, _TRAINING_SET_FILE)
  classifier.initialize()
  classifier.train()
  classifier.classify()
  
