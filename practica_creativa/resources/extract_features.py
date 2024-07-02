import sys, os, re
import iso8601
import datetime


# Pass date and base path to main() from airflow
def main(base_path):
  APP_NAME = "fetch_prediction_requests.py"
  
  # If there is no SparkSession, create the environment
  try:
    sc and spark
  except NameError as e:
    import findspark
    findspark.init()
    import pyspark
    import pyspark.sql
    
    sc = pyspark.SparkContext()
    spark = pyspark.sql.SparkSession(sc).builder.appName(APP_NAME).getOrCreate()
    
  # Load the on-time parquet file
  on_time_dataframe = spark.read.parquet('{}/data/on_time_performance.parquet'.format(base_path))
  on_time_dataframe.registerTempTable("on_time_performance")
  
  # Select a few features of interest
  simple_on_time_features = spark.sql("""
  SELECT
    FlightNum,
    FlightDate,
    DayOfWeek,
    DayofMonth AS DayOfMonth,
    CONCAT(Month, '-',  DayofMonth) AS DayOfYear,
    Carrier,
    Origin,
    Dest,
    Distance,
    DepDelay,
    ArrDelay,
    CRSDepTime,
    CRSArrTime
  FROM on_time_performance
  """)
  simple_on_time_features.show()
  
  # Sample 10% to make executable inside the notebook
  simple_on_time_features = simple_on_time_features.sample(False, 0.1, seed=27)

  # Filter nulls, they can't help us
  filled_on_time_features = simple_on_time_features.filter(
    simple_on_time_features.ArrDelay.isNotNull()
    &
    simple_on_time_features.DepDelay.isNotNull()
  )
  
  # We need to turn timestamps into timestamps, and not strings or numbers
  def convert_hours(hours_minutes):
    hours = hours_minutes[:-2]
    minutes = hours_minutes[-2:]
    
    if hours == '24':
      hours = '23'
      minutes = '59'
    
    time_string = "{}:{}:00Z".format(hours, minutes)
    return time_string
  
  def compose_datetime(iso_date, time_string):
    return "{} {}".format(iso_date, time_string)
  
  def create_iso_string(iso_date, hours_minutes):
    time_string = convert_hours(hours_minutes)
    full_datetime = compose_datetime(iso_date, time_string)
    return full_datetime
  
  def create_datetime(iso_string):
    return iso8601.parse_date(iso_string)
  
  def convert_datetime(iso_date, hours_minutes):
    iso_string = create_iso_string(iso_date, hours_minutes)
    dt = create_datetime(iso_string)
    return dt
  
  def day_of_year(iso_date_string):
    dt = iso8601.parse_date(iso_date_string)
    doy = dt.timetuple().tm_yday
    return doy
  
  def alter_feature_datetimes(row):
    
    flight_date = iso8601.parse_date(row['FlightDate'])
    scheduled_dep_time = convert_datetime(row['FlightDate'], row['CRSDepTime'])
    scheduled_arr_time = convert_datetime(row['FlightDate'], row['CRSArrTime'])
    
    # Handle overnight flights
    if scheduled_arr_time < scheduled_dep_time:
      scheduled_arr_time += datetime.timedelta(days=1)
    
    doy = day_of_year(row['FlightDate'])
    
    return {
      'FlightNum': row['FlightNum'],
      'FlightDate': flight_date,
      'DayOfWeek': int(row['DayOfWeek']),
      'DayOfMonth': int(row['DayOfMonth']),
      'DayOfYear': doy,
      'Carrier': row['Carrier'],
      'Origin': row['Origin'],
      'Dest': row['Dest'],
      'Distance': row['Distance'],
      'DepDelay': row['DepDelay'],
      'ArrDelay': row['ArrDelay'],
      'CRSDepTime': scheduled_dep_time,
      'CRSArrTime': scheduled_arr_time,
    }
  
  timestamp_features = filled_on_time_features.rdd.map(alter_feature_datetimes)
  timestamp_df = timestamp_features.toDF()
  
  # Explicitly sort the data and keep it sorted throughout. Leave nothing to chance.
  sorted_features = timestamp_df.sort(
    timestamp_df.DayOfYear,
    timestamp_df.Carrier,
    timestamp_df.Origin,
    timestamp_df.Dest,
    timestamp_df.FlightNum,
    timestamp_df.CRSDepTime,
    timestamp_df.CRSArrTime,
  )
  
  # Store as a single json file and bzip2 it
  os.system("sudo rm -rf {}/data/simple_flight_delay_features.json".format(base_path))
  sorted_features.repartition(1).write.mode("overwrite").json("{}/data/simple_flight_delay_features.json".format(base_path))
  os.system("cp {}/data/simple_flight_delay_features.json/part* {}/data/simple_flight_delay_features.jsonl".format(base_path, base_path))
  os.system("bzip2 --best {}/data/simple_flight_delay_features.jsonl".format(base_path))
  os.system("bzcat {}/data/simple_flight_delay_features.jsonl.bz2 >> {}/data/simple_flight_delay_features.jsonl".format(base_path, base_path))


if __name__ == "__main__":
  main(sys.argv[1])
