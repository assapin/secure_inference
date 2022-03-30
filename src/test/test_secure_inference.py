import os
from io import BytesIO

import joblib
import pytest
from cryptography.fernet import Fernet

import inference
import model
from config.settings import settings
from encryption import fernet_encryption
from test import resources

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import pandas as pd


def test_secure_inference_local():
    with pkg_resources.path(resources, 'x_test.csv') as p:
        test_inputs = pd.read_csv(p)

    with pkg_resources.path(model, settings.model_file_name) as p:
        with open(p, 'rb') as f:
            original_bytes = f.read()

    original_model = joblib.load(BytesIO(original_bytes))
    key = fernet_encryption.generate_key_inner()
    f = Fernet(key)
    encrypted = f.encrypt(original_bytes)
    decrypted = f.decrypt(encrypted)
    secure_model = joblib.load(BytesIO(decrypted))
    expected = inference.predict(test_inputs, original_model)
    secured = inference.predict(test_inputs, secure_model)
    assert (expected == secured).all()


@pytest.mark.skipif(not settings.use_secure, reason="runs only after encrypted model file created on file system")
def test_secure_inference_ci():
    with pkg_resources.path(resources, 'x_test.csv') as p:
        test_inputs = pd.read_csv(p)
    original_model = inference.load_model(is_secure=False)
    secure_model = inference.load_model(is_secure=True)
    expected = inference.predict(test_inputs, original_model)
    secured = inference.predict(test_inputs, secure_model)
    assert (expected == secured).all()
