from math import pow


class FitnessXY:
    # This fitness object is only applicable if the dataset is shape [x, y]
    # where x is input and y is the target output

    def __init__(self, dataframe):
        # TODO:make if to test if cols x and y exist in the df
        self.df = dataframe

    # MSE = Σ(y_i – t_i)^2 / n
    def mse(self, chr):
        if chr.tree is None:
            return 0

        s = 0
        for _, row in self.df.iterrows():
            s += pow((chr.compute(row["x"]) - row["y"]), 2)

        val_mse = s / len(self.df)
        normalize = 1 / (1 + val_mse)

        return normalize

    # E =
    def avrg_err(self, chr):
        if chr.tree is None:
            return 0

        s = 0
        for _, row in self.df.iterrows():
            s += abs(chr.compute(row["x"]) - row["y"])

        ave = s / len(self.df)
        normalize = 1 / (1 + ave)
        return normalize
