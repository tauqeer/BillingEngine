from org.sfu.billing.mediation.mediationcdr import MediationCdr
from pyspark.sql import functions
from pyspark.sql.functions import split, to_timestamp, trim

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

        cdr_df = cdr_df.withColumn('customerId', trim(events.getItem(0))) \
                       .withColumn('dateTimeConnect', to_timestamp(trim(events.getItem(1)),format='yyyyMMdd HHmmss')) \
                       .withColumn('dateTimeDisconnect',to_timestamp(trim(events.getItem(2)),format='yyyyMMdd HHmmss')) \
                       .withColumn('origNodeId',trim(events.getItem(3))) \
                       .withColumn('destNodeId',trim(events.getItem(4))) \
                       .withColumn('callingPartyNumber',trim(events.getItem(5))) \
                       .withColumn('originalCalledPartyNumber',trim(events.getItem(6))) \
                       .withColumn('callStatus',trim(events.getItem(7)).cast('int')) \
                       .withColumn('eventType',trim(events.getItem(8)))

        cdr_df = cdr_df.drop(cdr_df['value'])
           
        return cdr_df

    # Method involves in deciding pipeline cdr`s should go through in mediation layer
    # Input: Mapped dataframe
    # Output: Normalized dataframe after going through mediation pipeline
    def invoke_mediation(self, mapped_df):
        mediationCdr = MediationCdr()
        normalized_frame = mediationCdr.execute(mapped_df)
        return normalized_frame

    # Method involves in deciding pipeline cdr`s should go through in rating layer
    # Input: Normalized dataframe coming from mediation pipeline
    # Output: Dataframes after rating applied based on offers
    def invoke_rating(self, med_df):
        pass


