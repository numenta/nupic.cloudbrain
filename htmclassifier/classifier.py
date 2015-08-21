# TODO: see metric_store.py
# 1. subscribe to rabbitMQ 
# 2. load trained model
# 3. run data through trained model

#!/usr/bin/env python
from cloudbrain.listeners.pika_subscriber import PikaSubscriber 
from abc import ABCMeta, abstractmethod

class Classifier(object):
  __metaclass__ = ABCMeta
  
  def __init__(self, device_name, device_id, host):
    self.device_name = device_name
    self.device_id = device_id
    self.host = host
    self.subscriber = PikaSubscriber(self.device_name, self.device_id, self.host)
    self.model = None
   
  @abstractmethod 
  def initialize(self):  
    """
    
    :return:
    """
    
  
    
  @abstractmethod
  def classify(self):
    """
    
    :return:
    """
    
  @abstractmethod
  def train(self):
    """
    
    :return:
    """
    
  @abstractmethod
  def load_model(self):
    """
    
    :return:
    """
    
    
  @abstractmethod
  def save_model(self):
    """
    
    :return:
    """
    
    
