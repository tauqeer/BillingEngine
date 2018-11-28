from org.sfu.billing.utils.configurations import SparkConfig
from org.sfu.billing.utils import configurations
from org.sfu.billing import *
from org.sfu.billing.devices.cdr import CallDetailRecord

from pyspark.sql import functions
from pyspark.sql.functions import split



class Controller:
    """
    Controller class is used to control lifecycle of entire application. It invokes all modules in logical sequence.
    Execution pipeline is Mediation module, Rating Module and Persistent module        
    """

    spark_config = SparkConfig()

    #This method will start streaming of events based on registered topic in kafka
    def stream_rawCdr(self):
        events = self.spark_config.get_events()
        return events

    # This method will determine device type and return its object
    # Default or implemented case as of now is of call detail record
    # There can be other iot devices as well which can be rated
    def device_type(self,events):
        return CallDetailRecord()
    
    # Main method which includes logic of Lifecycle of application
    # 1.Starts Streaming process
    # 2.Detect type of device
    # 3.Map raw events into structured dataframe
    # 4.Invoke Mediation process
    # 5.Invoke Rating process
    # 6.Check data in hdfs 
    # 7.Persist data on configured database
    def process(self):
        events = self.stream_rawCdr()
        cdr = self.device_type(events)
        mapped_df = cdr.map(events)


        stream = mapped_df.writeStream.foreachBatch(configurations.save_batch).start()
        self.spark_config.stopStreaming(stream)
        pass
        
        
def main():
    controller = Controller()
    controller.process()

if __name__ == "__main__":
    main()
