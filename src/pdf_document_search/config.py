"""Strict local configuration without directory creation or network access."""

import ipaddress
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    data_dir: Path = Path("data")
    host: str = "127.0.0.1"
    port: int = 8765
    ocr_enabled: bool = False
    semantic_enabled: bool = False


def load_config(path: str | Path | None = None) -> Config:
    if path is None:
        return Config()
    source = Path(path).resolve()
    with source.open("rb") as stream:
        values = tomllib.load(stream)
    unknown = values.keys() - Config.__dataclass_fields__.keys()
    if unknown:
        raise ValueError(f"Неизвестные параметры: {', '.join(sorted(unknown))}")
    host = values.get("host", "127.0.0.1")
    if not isinstance(host, str):
        raise ValueError("Адрес должен быть строкой")
    try:
        is_loopback = ipaddress.ip_address(host).is_loopback
    except ValueError:
        is_loopback = False
    if not is_loopback:
        raise ValueError("Разрешён только локальный IP-адрес")
    port = values.get("port", 8765)
    if type(port) is not int or not 1 <= port <= 65535:
        raise ValueError("Порт должен быть целым числом от 1 до 65535")
    for key in ("ocr_enabled", "semantic_enabled"):
        if key in values and type(values[key]) is not bool:
            raise ValueError(f"{key}: требуется логическое значение")
    data_dir = values.get("data_dir", "data")
    if not isinstance(data_dir, str) or not data_dir.strip():
        raise ValueError("Каталог данных должен быть непустой строкой")
    values["data_dir"] = (source.parent / data_dir).resolve()
    return Config(**values)
