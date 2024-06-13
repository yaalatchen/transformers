import os
import random
import numpy as np
import pandas as pd
import torch

import sys
sys.path.insert(1, r'C:\Users\yczohar\projects\IBM_tsfm')
sys.path.insert(1, r'C:\Users\yczohar\projects\transformers\src')

from transformers import (
    EarlyStoppingCallback,
    PatchTSMixerConfig,
    PatchTSMixerForPrediction,
    Trainer,
    TrainingArguments,
)

from tsfm_public.toolkit.util import select_by_index
from tsfm_public.toolkit.dataset import ForecastDFDataset
from tsfm_public.toolkit.time_series_preprocessor import TimeSeriesPreprocessor

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

if __name__ =='__main__':

    # Set seed for reproducibility
    SEED = 42
    torch.manual_seed(SEED)
    random.seed(SEED)
    np.random.seed(SEED)

    num_workers = 8  # Reduce this if you have low number of CPU cores
    batch_size = 32  # Reduce if not enough GPU memory available
    patch_length = 8
    context_length = 512
    forecast_horizon = 96
    num_workers = 16  # Reduce this if you have low number of CPU cores
    batch_size = 64  # Adjust according to GPU memory

    print(f"Loading target dataset")
    dataset_path = r"C:\Users\yczohar\Desktop\demand_data\full_demand_weather_data_noNAN.csv"
    id_columns = []
    forecast_columns = ["year","month","day","hour","minute","second","temperature","dew_point","wind_direction","wind_speed",
                        "wind_gust_speed","pressure","sky_coverage","day_of_week","new_years_eve","new_years_day","easter_day_1","easter_day_2",
                        "may_day","victory_day","ascention_day","mothers_day","whit_sunday","whit_monday","fathers_day","bastille_day","assumption_day",
                        "all_saints_day","armistice_day","christmas_eve","christmas_day","demand"]
    train_start_index = None  # None indicates beginning of dataset
    train_end_index = 12 * 30 * 24 * 4
    timestamp_column = "date"

    # we shift the start of the validation/test period back by context length so that
    # the first validation/test timestamp is immediately following the training data
    valid_start_index = 12 * 30 * 24 * 4 - context_length
    valid_end_index = 12 * 30 * 24 * 4 + 4 * 30 * 24 * 4

    test_start_index = 12 * 30 * 24 * 4 + 4 * 30 * 24 * 4 - context_length
    test_end_index = 12 * 30 * 24 * 4 + 8 * 30 * 24 * 4

    # Download ECL data from https://github.com/zhouhaoyi/Informer2020
    # dataset_path = r"C:\Users\yczohar\Downloads\ECL.csv"
    id_columns = []

    data = pd.read_csv(
        dataset_path,
        parse_dates = [timestamp_column]
    )

    train_data = select_by_index(
        data,
        id_columns=id_columns,
        start_index=train_start_index,
        end_index=train_end_index,
    )
    valid_data = select_by_index(
        data,
        id_columns=id_columns,
        start_index=valid_start_index,
        end_index=valid_end_index,
    )
    test_data = select_by_index(
        data,
        id_columns=id_columns,
        start_index=test_start_index,
        end_index=test_end_index,
    )

    tsp = TimeSeriesPreprocessor(
        timestamp_column=timestamp_column,
        id_columns=id_columns,
        target_columns=forecast_columns,
        scaling=True,
    )

    # print(train_data["date"].iloc[0].timestamp())


    def timestamp(t):
        return t.timestamp()


    print(train_data["date"].iloc[0].timestamp())
    train_data['date'] = train_data['date'].apply(timestamp)


    tsp.train(train_data)

    train_dataset = ForecastDFDataset(
        tsp.preprocess(train_data),
        id_columns=id_columns,
        target_columns=forecast_columns,
        context_length=context_length,
        prediction_length=forecast_horizon,
    )
    valid_dataset = ForecastDFDataset(
        tsp.preprocess(valid_data),
        id_columns=id_columns,
        target_columns=forecast_columns,
        context_length=context_length,
        prediction_length=forecast_horizon,
    )
    test_dataset = ForecastDFDataset(
        tsp.preprocess(test_data),
        id_columns=id_columns,
        target_columns=forecast_columns,
        context_length=context_length,
        prediction_length=forecast_horizon,
    )

    config = PatchTSMixerConfig(
        context_length=context_length,
        prediction_length=forecast_horizon,
        patch_length=patch_length,
        num_input_channels=len(forecast_columns),
        patch_stride=patch_length,
        d_model=48,
        num_layers=3,
        expansion_factor=3,
        dropout=0.5,
        head_dropout=0.7,
        mode="common_channel",  # change it `mix_channel` if we need to explicitly model channel correlations
        scaling="std",
        prediction_channel_indices = [len(forecast_columns)-1]
    )
    model = PatchTSMixerForPrediction(config=config)

    train_args = TrainingArguments(
        output_dir="./checkpoint/patchtsmixer/direct/train/output/",
        overwrite_output_dir=True,
        learning_rate=0.0001,
        num_train_epochs=20,
        do_eval=True,
        evaluation_strategy="epoch",
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        dataloader_num_workers=num_workers,
        report_to="tensorboard",
        save_strategy="epoch",
        logging_strategy="epoch",
        save_total_limit=3,
        logging_dir="./checkpoint/patchtsmixer/direct/train/logs/",  # Make sure to specify a logging directory
        load_best_model_at_end=True,  # Load the best model when training ends
        metric_for_best_model="eval_loss",  # Metric to monitor for early stopping
        greater_is_better=False,  # For loss
        label_names=["future_values"],
    )

    # Create a new early stopping callback with faster convergence properties
    early_stopping_callback = EarlyStoppingCallback(
        early_stopping_patience=5,  # Number of epochs with no improvement after which to stop
        early_stopping_threshold=0.001,  # Minimum improvement required to consider as improvement
    )

    trainer = Trainer(
        model=model,
        args=train_args,
        train_dataset=train_dataset,
        eval_dataset=valid_dataset,
        callbacks=[early_stopping_callback],
    )

    print("\n\nDoing forecasting training on Etth1/train")
    trainer.train()
    res = trainer.evaluate(test_dataset)
    print(res)