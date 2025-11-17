import pandas as pd

class DataValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def check_non_null(self):
        null_counts = self.df.isnull().sum()
        failed = null_counts[null_counts > 0]
        return failed.to_dict()

    def check_duplicates(self):
        duplicate_rows = self.df[self.df.duplicated()]
        return duplicate_rows.shape[0]

    def check_positive_values(self, numeric_cols):
        negative_counts = {}
        for col in numeric_cols:
            count = (self.df[col] < 0).sum()
            if count > 0:
                negative_counts[col] = int(count)
        return negative_counts

    def run_all_validations(self, numeric_cols):
        results = {
            "null_values": self.check_non_null(),
            "duplicates": self.check_duplicates(),
            "negative_values": self.check_positive_values(numeric_cols)
        }
        return results
