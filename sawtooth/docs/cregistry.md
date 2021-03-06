<!--- -*- mode: markdown; fill-column: 80 -*- --->
<!---
Licensed under Creative Commons Attribution 4.0 International License
https://creativecommons.org/licenses/by/4.0/
--->

# PDO Contract Registry Transaction Family Specification  #

Version 0.1

## Overview ##

The PDO Contract Registry transaction family maintains a list of
PDO contracts and their mapping to the PDO contract enclaves that can
be used for the contract execution.

## State ##
This section describes what smart contract information is saved in the
Sawtooth Global State. The following defines the stored PDO smart contract info:

```cpp
message PdoContractInfo {
    // The "register" transaction id hash (256 bits, base64 encoded)
    string contract_id = 1;

    // Contract SHA256 hash used by the enclaves to verify the contract.
    // It is set during "register" transaction and cannot be changed later
    string contract_code_hash = 3;

    // PDO signature generated by the enclave service
    string pdo_contract_creator_pem_key = 4;

    // Provisioning service ids below are set during "register" transaction
    // and cannot be changed later
    repeated string provisioning_service_ids = 5;

    // Provisioned enclaves info
    repeated PdoContractEnclavesInfo enclaves_info = 6;
}
```
## Addressing ##

Addresses for the PDO contract registry transaction family are set by
adding sha512 hash of the PDO contract id to the contract registry namespace previx.

## Transaction Payload ##

PDO enclave registry transaction family payloads are defined by the
following protocol buffers code:

```cpp
message PdoContractTransaction {
    // The action that the transaction processor will take.
    // They are “register”, “revoke”, "add-enclaves", or "remove-enclaves"
    string verb = 1;

    // contract id
    string contract_id = 2;

    // Transaction details specific to the action. Refer below to
    // PdoContractRegister for "register" transaction
    // PdoContractAddEnclaves for "add-enclaves"
    // PdoContractRemoveEnclaves for "remove-enclaves"
    bytes transaction_details = 3;
}
```
Transaction details for the “register” transaction

```cpp
message PdoContractRegister {
    // Contract SHA256 hash used by the enclaves to verify the contract.
    // It is set during "register" transaction and cannot be changed later
    string contract_code_hash = 1;

    // public key of the contract creator
    string pdo_contract_creator_pem_key = 2;

    // PDO signature generated by the contract creator
    string pdo_signature = 3;

    // Provisioning service ids below are set during "register" transaction
    // and cannot be changed later
    repeated string provisioning_service_ids = 4;
}
```

Transaction details for the “add-enclaves” transaction

```cpp
message PdoContractAddEnclaves {
    // Signature generated by the contract creator
    string pdo_signature = 1;
    //
    repeated PdoContractEnclavesInfo enclaves_info = 2;
}
```
```cpp
message PdoContractEnclavesInfo {
    // It must match a corresponding verifying_key
    // in the contract enclave registry
    string contract_enclave_id = 1;

    // Encrypted key for the enclave to decrypt the contract state
    string encrypted_contract_state_encryption_key = 2;

    // Contract signature generated by the enclave
    string enclave_signature = 3;

    // PdoProvisioningKeyToStateSecretMap is defined below
    repeated PdoProvisioningKeyToStateSecretMap enclaves_map = 4;
}
```

Transaction details for the "remove-enclaves” transaction

```cpp
message PdoContractRemoveEnclaves {
    // Ids of enclaves to remove
    repeated string contract_enclave_ids = 1;
}
```

Below is PdoContractEnclaveProvisioningKeyToStateSecretMap definition
```cpp
message PdoContractRemoveEnclaves {
    // Ids of enclaves to remove
    repeated string contract_enclave_ids = 1;
}
```

## Transaction Header ##

One-time Sawtooth signing keys are generated for each PDO contract transaction.

## Inputs and Outputs ##

The inputs for validator registry family transactions must include:
*	The address of ``contract_id``
*	In case of “add-enclaves” actions, the addresses of all ``contract_enclave_id``'s
The outputs for validator registry family transactions must include:
*	The address of ``contract_id``

## Dependencies ##

None

## Family ##

*	family_name: “pdo_contract_instance_registry”
*	family_version: "1.0"

## Encoding ##

The encoding field must be set to “application/protobuf”.

## Execution ##

Untrusted transaction processor code will store, update,
or remove the PDO contract registry global state data.
Any client can add a new PDO contract.
A PDO signature is used to ensure that only the contract creator is able to add/remove
enclaves to a contract.

The generated signatures are computed as follows.
The PDO signature for contract ``“register”`` is computed over the serialization of the following fields:
* ``txn_signer`` public key of the transaction signer
* ``contract_code_hash``
* ``provisioning_service_ids`` a list of public keys of the provisionig services

The PDO signature for ``add-enclaves`` is computed over the serialization of the following fields:
* ``txn_signer`` public key of the transaction signer
* ``contract_id``
  * (the following block is repeated for all added enclaves)
  * ``provisioning_service_public_key_1``
  * ``provisioning_contract_state_secret_1``
  * ``provisioning_service_public_key_2``
  * ``provisioning_contract_state_secret_2``
  * ... for all provisioning services and respective provisioned secrets
  * ``encrypted_contract_state_encryption_key``
  * ``enclave_signature``

The enclave signature is computed over the serialization of the following fields:
* ``contract_id``
* ``pdo_contract_creator_pem_key`` the public key of the contract creator
  * (the following block is repeated for all added enclaves)
  * ``provisioning_service_public_key_1``
  * ``provisioning_contract_state_secret_1``
  * ``provisioning_service_public_key_2``
  * ``provisioning_contract_state_secret_2``
  * ... for all provisioning services and respective provisioned secrets
  * ``encrypted_contract_state_encryption_key``
