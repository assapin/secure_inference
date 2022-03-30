# Securing a Python inference package using PyArmor and Fernet keys

Distributing Python modules to untrusted environments requires securing the code.
In the case of an inference package, this includes obfuscating the code as well as any model files.

This repo demonstrates how to:
1. Secure code by obfuscating it with PyArmor
2. Securing the model file using a Fernet key
3. Writing the inference code such that it decrypts the model file in memory and uses it to perform predictions
## Structure
```encryption/fernet_encryption.py``` is a utility that can:
- Generate new Fernet keys
- Encrypt and decrypt files with specified keys

```train/train.py``` contains a simple training script that produces a joblib model

```model``` package contains the dumped joblib model

```inference.py``` simulates usage of the model during inference.
Loads the model from its encrypted path and decrypts it in memory using the key

```key/fernet_key.py``` a module containing the key used to encrypt/decrypt the pickled model file.
**Note: This file is *replaced* by the github action during step 2 of the worklfow (see below)**


```test/test_secure_inference.py``` validates that the encryption/decryption of the model file
doesn't change its behavior

```github-actions-secure.yaml``` contains the workflow for automatically 
securing the package on every push to main branch

## Workflow for securing the code
This workflow happens inside the github actions.
1. Pull a pre-generated Fernet key from the *github repository secret. 
   
2. Generate a local key/fernet_key.py file containing the key

3. Encrypt the model pickle file with the key

4. Test that the encryption didn't change the model by decrypting and validating
   
5. Obfuscate the entire codebase with PyArmor

6. Copy the encrypted model file and .env file into the obfuscated library

7. Test that the obfuscated inference.py file runs without exception

8. Tar.gz the obfuscated codebase and upload it into the workflow's artifacts

   


