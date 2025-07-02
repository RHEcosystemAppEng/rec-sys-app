import pandas as pd
from pathlib import Path
from datetime import datetime
from feast import FeatureStore


class DatasetProvider:
    def item_df(self):
        return None

    def user_df(self):
        return None

    def interaction_df(self):
        return None


class LocalDatasetProvider(DatasetProvider):
    def __init__(self, store=None):
        self._item_df_path = Path("./feature_repo/data/item_df_output.parquet")
        self._user_df_path = Path("./feature_repo/data/user_df_output.parquet")
        self._interaction_df_path = Path("./feature_repo/data/interaction_df_output.parquet")

        if self._item_df_path.exists() & self._user_df_path.exists() & self._interaction_df_path.exists():
            self._item_df = pd.read_parquet(self._item_df_path)
            self._user_df = pd.read_parquet(self._user_df_path)
            self._interaction_df = pd.read_parquet(self._interaction_df_path)
            return

        # Use Feast item, user and interaction services to create the dataframes
        assert store is not None
        self._load_from_store(store)

    def _load_from_store(self, store: FeatureStore):
        # load feature services
        item_service = store.get_feature_service("item_service")
        user_service = store.get_feature_service("user_service")
        interaction_service = store.get_feature_service("interaction_service")
        print('service loaded')

        interactions_ids = pd.read_parquet('./feature_repo/data/recommendation_interactions.parquet')
        user_ids = interactions_ids['user_id'].unique().tolist()
        item_ids = interactions_ids['item_id'].unique().tolist()
        # select which items to use for the training
        item_entity_df = pd.DataFrame.from_dict(
            {
                'item_id': item_ids,
                'event_timestamp': [datetime(2025, 1, 1)] * len(item_ids)
            }
        )
        # select which users to use for the training
        user_entity_df = pd.DataFrame.from_dict(
            {
                'user_id': user_ids,
                'event_timestamp': [datetime(2025, 1, 1)] * len(user_ids)
            }
        )
        # Select which item-user interactions to use for the training
        item_user_interactions_df = interactions_ids[['item_id', 'user_id']].copy()
        item_user_interactions_df['event_timestamp'] = datetime(2025, 1, 1)
        # retrieve datasets for training
        self._item_df = store.get_historical_features(entity_df=item_entity_df, features=item_service).to_df()
        self._user_df = store.get_historical_features(entity_df=user_entity_df, features=user_service).to_df()
        self._interaction_df = store.get_historical_features(entity_df=item_user_interactions_df,
                                                             features=interaction_service).to_df()
        self._item_df.to_parquet(self._item_df_path)
        self._user_df.to_parquet(self._user_df_path)
        self._interaction_df.to_parquet(self._interaction_df_path)

    def item_df(self):
        return self._item_df

    def user_df(self):
        return self._user_df

    def interaction_df(self):
        return self._interaction_df



