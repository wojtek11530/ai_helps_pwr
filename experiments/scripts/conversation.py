"""Script for ."""
import json
from datetime import datetime
import os
from pathlib import Path

import configparser
import click
import yaml

from ai_helps_pwr.utils.common import (
    load_model_from_config,
    load_json
)


@click.command()
@click.option(
    "--config_path",
    help="Path to config.",
    type=click.Path(exists=True, path_type=Path),
    default=Path("config/config.local")
)
@click.option(
    "--output_dir",
    help="Directory to save data.",
    type=click.Path(path_type=Path),
    default=Path("output")
)
@click.option(
    "--hparams_path",
    help="Path to selected model hparams",
    type=click.Path(exists=True, path_type=Path),
    default=Path("experiments/config/models.yaml")
)
@click.option(
    "--model",
    help="Name of selected model",
    type=str,
    default="qpt_conversation"
)
@click.option(
    "--output_dir",
    help="Directory to save data.",
    type=click.Path(path_type=Path),
    default=Path("output")
)
def main(
    config_path: Path,
    hparams_path: Path,
    model: str,
    output_dir: Path
):
    """Use GPT to answer a question."""
    config = configparser.RawConfigParser()
    config.read(config_path)

    gpt_config = dict(config.items('gpt'))

    with open(hparams_path, "r") as fin:
        hparams = yaml.safe_load(fin)[model]

    model = load_model_from_config(cfg=hparams["model"])

    prompt = load_json(hparams["prompt"]["message_path"])

    out = model(prompt, gpt_config['apikey'])

    time_now = datetime.now().strftime("%m_%d_%Y__%H_%M_%S")
    output_file = Path(os.path.join(
        output_dir, Path(model.name),
        Path(f"{time_now}.json")
    ))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w") as f_out:
        json.dump(obj=out, fp=f_out, indent=4, ensure_ascii=True)


if __name__ == "__main__":
    main()
