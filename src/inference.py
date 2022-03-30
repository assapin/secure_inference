from io import BytesIO

import joblib
from pandas import DataFrame

import model
from config.settings import settings
from encryption.fernet_encryption import decrypt_file_inner
from key import fernet_key

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


def load_model(is_secure=None, model_file_name=None):
    secure = is_secure or settings.use_secure
    file_to_load = model_file_name or settings.get_model_file_name()

    with pkg_resources.path(model, file_to_load) as p:
        path = p
    if secure:
        path = BytesIO(decrypt_file_inner(key=fernet_key.key, source_path=path))
        path.seek(0)
    return joblib.load(path)


classifier = load_model(is_secure=None, model_file_name=None)


def predict(data: DataFrame, clf=classifier):
    return clf.predict(data)


if __name__ == '__main__':
    print(settings)
