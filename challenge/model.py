import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.utils.class_weight import compute_class_weight


from typing import Tuple, Union, List

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        self.FEATURES_COLS = [
        "OPERA_Latin American Wings", 
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air"
    ]

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    #) -> Union(Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame):
    ) -> pd.DataFrame:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        data = self.generate_features(data)
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES'),            
        ], axis = 1)
        # In case that the data hasn't all the columns
        # we need to add the missing ones
        for col in self.FEATURES_COLS:
            if col not in features.columns:
                features[col] = 0
        selected_features = features[self.FEATURES_COLS]
        if target_column is not None:
            target = data[[target_column]]
            return selected_features, target
        return selected_features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        
        self._model = LogisticRegression(class_weight='balanced', max_iter=1000)
        self._model.fit(features, target)

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        if self._model:
            prediction = self._model.predict(features).tolist()
            return prediction
        return [0] * len(features)
    
    def generate_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate features from raw data.

        Args:
            data (pd.DataFrame): raw data.

        Returns:
            pd.DataFrame: features.
        """
        if 'Fecha-I' not in data or 'Fecha-O' not in data:
            return data
        # 2.a. Period of Day
        data['period_day'] = data['Fecha-I'].apply(self.get_period_day)
        # 2.b. High Season
        data['high_season'] = data['Fecha-I'].apply(self.is_high_season)
        # 2.c. Difference in Minutes
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)
        
        # 2.d. Delay
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        return data
    
    def get_period_day(self, date):
        date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
        morning_min = datetime.strptime("05:00", '%H:%M').time()
        morning_max = datetime.strptime("11:59", '%H:%M').time()
        afternoon_min = datetime.strptime("12:00", '%H:%M').time()
        afternoon_max = datetime.strptime("18:59", '%H:%M').time()
        evening_min = datetime.strptime("19:00", '%H:%M').time()
        evening_max = datetime.strptime("23:59", '%H:%M').time()
        night_min = datetime.strptime("00:00", '%H:%M').time()
        night_max = datetime.strptime("4:59", '%H:%M').time()
        
        if(date_time > morning_min and date_time < morning_max):
            return 'mañana'
        elif(date_time > afternoon_min and date_time < afternoon_max):
            return 'tarde'
        elif(
            (date_time > evening_min and date_time < evening_max) or
            (date_time > night_min and date_time < night_max)
        ):
            return 'noche'
        
    def is_high_season(self, date):
        fecha_año = int(date.split('-')[0])
        fecha = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year = fecha_año)
        range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year = fecha_año)
        range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year = fecha_año)
        range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year = fecha_año)
        range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year = fecha_año)
        range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year = fecha_año)
        range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year = fecha_año)
        range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year = fecha_año)
        
        if ((fecha >= range1_min and fecha <= range1_max) or 
            (fecha >= range2_min and fecha <= range2_max) or 
            (fecha >= range3_min and fecha <= range3_max) or
            (fecha >= range4_min and fecha <= range4_max)):
            return 1
        else:
            return 0
        
    def get_min_diff(self, data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff