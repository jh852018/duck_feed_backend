ENV = 'prod'

SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI'
SQLALCHEMY_DATABASE_URI_DEV = 'postgresql://postgres:toor@localhost/duck_feed'
SQLALCHEMY_DATABASE_URI_PROD = 'postgres://fcvsmlzuwlmubg:196a52b2d0b1510bb66d321f812e1fab6c337e61fc38be0c4d4b441f76bd795c@ec2-54-144-196-35.compute-1.amazonaws.com:5432/d6kgqfsk0i1tls'
SQLALCHEMY_TRACK_MODIFICATIONS = 'SQLALCHEMY_TRACK_MODIFICATIONS'

TABLENAME = 'duckfeedentry'

DF_TIME_J = 'dfTime'
DF_FOOD_J = 'dfFood'
DF_FOOD_LOCATION_J =  'dfLocation'
DF_FOOD_COUNT_J = 'dfCount'
DF_FOOD_TYPE_J = 'dfFoodType'
DF_FOOD_QTY_J = 'dfFoodQty'

DF_TIME_T = 'df_time'
DF_FOOD_T = 'df_food'
DF_FOOD_LOCATION_T = 'df_location'
DF_FOOD_COUNT_T = 'df_count'
DF_FOOD_TYPE_T = 'df_food_type'
DF_FOOD_QTY_T = 'df_food_qty'

ERROR = 'error'
MESSAGE = 'message'
DESCRIPTION = 'description'