from pyspark.sql import functions
from pyspark.sql.functions import split, lit

class CallDetailRecord(object):
    """Domain class for device type Telco. This class will hold information of how to transform into structured dataframe
        and which all pipeline it should go through in mediation and rating process.
    """
    #Sample raw cdr 
    #TESTCUST12,20181101 154530,20181101 164530,49.252121 | -122.893949,49.252814 | -122.896873,2365482589,2365694587,0,1
    #This method will transform raw cdr coming into mediation layer to structured dataframe
    def map(self, raw_cdr):
        cdr_df = raw_cdr.select(raw_cdr['value'].cast('string'))
        events = functions.split(cdr_df['value'], ',')
        cdr_df = cdr_df.withColumn('customerId', events.getItem(0)) \
                       .withColumn('dateTimeConnect', events.getItem(1)) \
                       .withColumn('dateTimeDisconnect',events.getItem(2)) \
                       .withColumn('origNodeId',events.getItem(3)) \
                       .withColumn('destNodeId',events.getItem(4)) \
                       .withColumn('callingPartyNumber',events.getItem(5)) \
                       .withColumn('originalCalledPartyNumber',events.getItem(6)) \
                       .withColumn('callStatus',events.getItem(7)) \
                       .withColumn('eventType',events.getItem(8))

        return cdr_df

    # Method involves in deciding pipeline cdr`s should go through in mediation layer
    # Input: Mapped dataframe
    # Output: Normalized dataframe after going through mediation pipeline
    def invoke_mediation(self, mapped_df):
        pass

    # Method involves in deciding pipeline cdr`s should go through in rating layer
    # Input: Normalized dataframe coming from mediation pipeline
    # Output: Dataframes after rating applied based on offers
    def invoke_rating(self, med_df):
        pass


