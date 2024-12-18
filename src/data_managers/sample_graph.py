import polars as pl
import torch
import torch_geometric as pyg

from src.base_classes.omic_data_loader import OmicDataLoader, OmicDataManager
from src.gnn_utils.graph_building import (
    cosine_similarity_matrix,
    dense_to_coo,
    keep_n_neighbours,
    threshold_matrix,
)


class SampleGraphDataManager(OmicDataManager):
    """
    Graph data manager for creating graphs based on sample similarity
    """

    def __init__(
        self, omic_data_loaders: dict[str, OmicDataLoader], params, n_splits: int = 5
    ):
        super().__init__(omic_data_loaders, n_splits)
        self.params = params
        # save num_classes and input dims
        data, _, _, _ = self.get_split(0)
        self.n_classes = data.y.unique().shape[0]
        self.feature_names = None

    def get_split(self, fold_idx: int):
        """
        Given a fold_idx returns train_x, test_x, train_y, test_y where
        train_x and test_x are concats of all the omics
        """

        omic_data = self.load_split(fold_idx)
        data = pyg.data.HeteroData()
        self.feature_names = {}

        for omic in omic_data:
            # train test df for current omic
            train_df = omic_data[omic]["train_df"]
            test_df = omic_data[omic]["test_df"]
            sample_column = omic_data[omic]["sample_column"]
            class_column = omic_data[omic]["class_column"]

            self.load_classes(train_df, test_df, sample_column, class_column)

            train_df = train_df.drop(class_column, sample_column)
            test_df = test_df.drop(class_column, sample_column)
            # save feature names for the current fold
            assert train_df.columns == test_df.columns
            self.feature_names[omic] = train_df.columns

            x_train = train_df.to_torch(dtype=pl.Float32)
            x_test = test_df.to_torch(dtype=pl.Float32)

            # we can probably just stack train and test vertically right?
            X = torch.cat([x_train, x_test], dim=0)

            A_cos_sim = cosine_similarity_matrix(X)

            if self.params["graph_style"] == "threshold":
                A = threshold_matrix(
                    A_cos_sim,
                    self_connections=self.params["self_connections"],
                    target_avg_degree=self.params["avg_degree"],
                )
            elif self.params["graph_style"] == "knn":
                A = keep_n_neighbours(
                    A_cos_sim,
                    self_connections=self.params["self_connections"],
                    n=self.params["knn"],
                )
            else:
                raise ValueError("Invalid graph style")

            data[omic].x = X
            data[omic].edge_index = dense_to_coo(A)

        train_y = torch.tensor(self.train_y)
        test_y = torch.tensor(self.test_y)

        # vcat y
        data.y = torch.cat([train_y, test_y], dim=0)

        # create train / test masks
        data.train_mask = torch.cat(
            [torch.ones_like(train_y), torch.zeros_like(test_y)], dim=0
        )
        data.test_mask = torch.cat(
            [torch.zeros_like(train_y), torch.ones_like(test_y)], dim=0
        )
        # make them bool
        data.train_mask = data.train_mask.bool()
        data.test_mask = data.test_mask.bool()
        data.val_mask = data.test_mask  # !! CHANGE LATER

        # prepare for next fold
        self.reset_attributes()

        return data, data, None, None
