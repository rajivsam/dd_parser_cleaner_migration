from pathlib import Path
import pandas as pd
import yaml


class PathCoordinator:
    def __init__(self, config):
        self.config = config
        self.working_dir = Path(config["working_dir"])
        self.raw_dir = self.working_dir / config.get("raw_data_dir", "data")
        self.output_dir = self.working_dir / config.get("featurization_output_dir", "data")

    @property
    def orders_path(self):
        return self.raw_dir / self.config["orders_file"]

    @property
    def order_items_path(self):
        return self.raw_dir / self.config["order_items_file"]

    @property
    def customers_path(self):
        return self.raw_dir / self.config["customers_file"]

    @property
    def featurized_path(self):
        return self.output_dir / self.config["featurized_data_file"]

    @property
    def sp_subset_path(self):
        return self.output_dir / self.config["sp_subset_file"]

    @property
    def sp_weekly_revenue_path(self):
        return self.output_dir / self.config["sp_weekly_revenue_file"]

    @property
    def sp_freq_prod_path(self):
        return self.output_dir / self.config["sp_freq_prod_file"]

    @property
    def sp_freq_prod_parquet(self):
        return self.output_dir / self.config["sp_freq_prod_parquet"]


class SimpleContext:
    def __init__(self, config, coordinator):
        self.config = config
        self.coord = coordinator
        self.df = None


def load_config(config_path: Path):
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_raw_data(context, stage_cfg=None):
    df_orders = pd.read_csv(context.coord.orders_path, parse_dates=["order_purchase_timestamp"])
    df_order_items = pd.read_csv(context.coord.order_items_path)
    df_customers = pd.read_csv(context.coord.customers_path)
    context.df = (
        pd.merge(df_orders, df_order_items, on="order_id", how="inner")
          .loc[:, ["order_id", "customer_id", "order_purchase_timestamp", "order_item_id", "product_id", "price"]]
          .merge(df_customers[["customer_id", "customer_zip_code_prefix", "customer_city", "customer_state"]], on="customer_id", how="left")
          .sort_values(["order_id", "order_item_id"])
          .reset_index(drop=True)
    )
    return context.df


def build_order_level_dataset(context, stage_cfg=None):
    df = context.df.copy() if context.df is not None else load_raw_data(context)
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    context.df = df
    context.df.to_csv(context.coord.featurized_path, index=False)
    return context.df


def derive_sp_2017_subset(context, stage_cfg=None):
    df = context.df.copy()
    df["year"] = df["order_purchase_timestamp"].dt.year
    df["month"] = df["order_purchase_timestamp"].dt.month
    df["woy"] = df["order_purchase_timestamp"].dt.isocalendar().week
    df_sp = df[(df["customer_state"] == "SP") & (df["year"] == 2017)].reset_index(drop=True)
    df_sp.to_csv(context.coord.sp_subset_path, index=False)
    context.df = df_sp
    return df_sp


def build_sp_weekly_product_matrix(context, stage_cfg=None):
    df = context.df.copy()
    df_weekly_revenue = df.groupby(["year", "woy"], observed=True)["price"].sum().reset_index()
    df_weekly_revenue.columns = ["year", "woy", "weekly_revenue"]
    df_weekly_revenue.to_csv(context.coord.sp_weekly_revenue_path, index=False)
    df_freq_prod = df.pivot_table(
        index="woy",
        columns="product_id",
        values="price",
        aggfunc="sum",
        fill_value=0
    ).reset_index()
    df_freq_prod.to_csv(context.coord.sp_freq_prod_path, index=False)
    df_freq_prod.to_parquet(context.coord.sp_freq_prod_parquet, index=False)
    return df_freq_prod


def run_pipeline(config_path: Path):
    config = load_config(config_path)
    coord = PathCoordinator(config)
    context = SimpleContext(config, coord)
    for stage_cfg in config.get("pipeline", []):
        method = globals()[stage_cfg["method"]]
        print(f"Running stage: {stage_cfg['name']}")
        method(context, stage_cfg)
    return context


if __name__ == "__main__":
    config_path = Path(__file__).resolve().parent.parent / "featurizer_config.yaml"
    run_pipeline(config_path)
