import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
import pickle, datetime, holidays, warnings
from main.models import ZoneDetail

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()


class Command(BaseCommand):

    def predict(self, predict_start_date, predict_end_date):

        predict_start_date = datetime.datetime.strptime(predict_start_date,"%Y-%m-%d")
        predict_end_date = datetime.datetime.strptime(predict_end_date,"%Y-%m-%d")
        run_date = timezone.now()
        
        def get_ymd(date_str):
            y, m, d = date_str.strftime("%Y"),date_str.strftime("%m"),date_str.strftime("%d")
            return int(y), int(m), int(d)
        
        help = 'Predict busyness'
        try:
            zone = ZoneDetail.objects.filter(Q(prediction_last_update__isnull=True) | 
                                             Q(prediction_last_update__date__lte=datetime.date(get_ymd(run_date)[0],
                                                                                                 get_ymd(run_date)[1],
                                                                                                 get_ymd(run_date)[2]))
                                             ).filter(datetime__gte=datetime.date(get_ymd(predict_start_date)[0],
                                                                                  get_ymd(predict_start_date)[1],
                                                                                  get_ymd(predict_start_date)[2])
                                                    ).filter(datetime__lte=datetime.date(get_ymd(predict_end_date)[0],
                                                                                  get_ymd(predict_end_date)[1],
                                                                                  get_ymd(predict_end_date)[2])
                                                    )
            
            
            # Convert the data into pandas dataframe and process before feeding into model
            df = pd.DataFrame.from_records(zone.values())

            # Create a dictionary of US holidays for 2022 and 2023
            us_holidays = dict(holidays.US(years=[2022, 2023]))

            # Assuming df is your DataFrame and 'datetime' is your date column
            # First, ensure that your 'datetime' column is indeed a datetime object
            df['datetime'] = pd.to_datetime(df['datetime'])

            # Change holiday column
            # otherwise, it will be "No"
            df['holiday'] = df['datetime'].dt.date.apply(lambda x: us_holidays.get(x, "No"))
            
            # Rename column to match with training data
            df.columns = df.columns.str.replace('taxi_zone_id', 'taxi_zone')
            df.columns = df.columns.str.replace('impression_predict','passenger_count')
            
            # Change datatype
            df['taxi_zone'] = df['taxi_zone'].astype('category')
            df['month'] = df['month'].astype('category')
            df['week'] = df['week'].astype('category')
            df['hour'] = df['hour'].astype('category')
            df['holiday'] = df['holiday'].astype('category')
            df['borough'] = df['borough'].astype('category')
            df['passenger_count'] = df['passenger_count'].fillna(-1).astype(int)

            # print(df.dtypes)
    
            # print existing categories:
            taxi_zone_cate = []
            for i in range(1,264):
                if i not in (103,104):
                    taxi_zone_cate.append(i)

            df['taxi_zone'] = df['taxi_zone'].cat.set_categories(taxi_zone_cate)
            df['week'] = df["week"].cat.set_categories(['0','1','2','3','4','5','6'])
            df['hour'] = df["hour"].cat.set_categories(['0','1','2','3','4','5','6','7','8','9','10','11','12',
                                                    '13','14','15','16','17','18','19','20','21','22','23'])
            
            # print(df[df['hour'].isnull()])

            df['borough'] = df['borough'].cat.set_categories(['Bronx', 'Brooklyn', 'EWR', 'Manhattan', 'Queens', 
                                                            'Staten Island'])
            df['month'] = df['month'].cat.set_categories(['1','2','3','4','5','6','7','8','9','10','11','12'])

            df['holiday'] = df['holiday'].cat.set_categories(['Christmas Day','Christmas Day (Observed)',
                                                            'Columbus Day','Independence Day','Labor Day',
                                                            'Martin Luther King Jr. Day', 'Memorial Day',
                                                            "New Year's Day", "New Year's Day (Observed)","No",
                                                            "Thanksgiving","Veterans Day","Washington's Birthday"
                                                            ])
                                                                
            # Keep the primary key and needed info to match and concat the results later
            df_pk = df[['zone_time_id','taxi_zone','impression_history','datetime','prediction_last_update','holiday']]
                        
            df = df.drop(labels=['zone_time_id','impression_history','datetime','place_last_update','prediction_last_update'], axis=1)

            # set up dummies features
            df_dummy = pd.get_dummies(df)
            
            # split data set into the features and target feature
            target_features=df_dummy[['passenger_count']]
            features = df_dummy.drop(labels=["passenger_count"], axis=1)

            # print(features.dtypes)
            
            # load the trained model
            loaded_model = pickle.load(open('../website/main/final_XGboost_model.pkl', 'rb'))
            
            # feed the model
            predictions = loaded_model.predict(features)
            predictions[predictions < 0] = 0
            predictions = predictions.astype(int)

            # convert prediction to a dataframe
            predictions_df = pd.DataFrame(predictions, columns=['predicted_passenger_count'])

            # concatenate the target_feature, features and primary key dataframes
            result = pd.concat([df_pk, predictions_df, target_features, features], axis=1)

            # Step 1: Convert DataFrame to a list of dictionaries
            update_data = df.to_dict(orient="records")

            # Step 2: Fetch existing objects based on zone_time_id
            existing_objects = zone.in_bulk(field_name="zone_time_id")

            # Step 3: Update fields of existing objects and add new objects to update_data
            updated_objects = []
            for data in update_data:
                zone_time_id = data["zone_time_id"]
                if zone_time_id in existing_objects:
                    # Update fields of existing object
                    obj = existing_objects[zone_time_id]
                    obj.impression_predict = data["impression_predict"]
                    obj.holiday = data["holiday"]
                    obj.prediction_last_update = timezone.now()
                    updated_objects.append(obj)
                else:
                    # Add new object with prediction_last_update as timezone.now()
                    data["prediction_last_update"] = timezone.now()
                    updated_objects.append(ZoneDetail(**data))

            # Step 4: Use bulk_update() to perform the bulk update
            with transaction.atomic():
                zone.bulk_update(updated_objects, fields=["impression_predict", "holiday", "prediction_last_update"])


            # print(result[['holiday']])
            
            # write prediction result in database
            # for index, row in result.iterrows():
            #     # try: 
            #     zone.filter(zone_time_id=row['zone_time_id']).bulk_update(impression_predict=int(row['predicted_passenger_count']),
            #                                                             prediction_last_update = timezone.now(),
            #                                                             holiday = row['holiday']
            #                                                             )
            #     print('Record no.',row['zone_time_id'],'Zone no.',row['taxi_zone'],'Time',row['datetime'],'updated prediction:',
            #           row['predicted_passenger_count'])
            #     # except Exception as e:
            #     #     print(e)                    

            # return zone
        
        except Exception as e:
            print(e)
        

    def add_arguments(self , parser):
        today = timezone.now()
        default_start = today.strftime('%Y-%m-%d')
        parser.add_argument('start' , nargs='?', type=str, default=default_start,
        help='Prediction is run to predict data from today by default.'
        )

        latest_data = ZoneDetail.objects.filter(prediction_last_update__isnull=False).latest("datetime")
        default_end = latest_data.datetime.strftime('%Y-%m-%d')
        parser.add_argument('end', nargs='?', type=str, default=default_end,
        help='Prediction is run to predict data to the latest day we have business data by default.'
        )
    
    def handle(self, *args, **kwargs):
        start_date = kwargs['start']
        end_date = kwargs['end']
        self.predict(start_date,end_date)