import secrets

import algokit_utils
import pytest
from algokit_utils import Account, get_localnet_default_account
from algokit_utils.config import config
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient

from smart_contracts.artifacts.cert.client import (
    CertClient,
    DeleteArgs,
    Deploy,
    NewCertificateNftArgs,
    UpdateArgs,
)


@pytest.fixture(scope="session")
def cert_client(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    creator_account: Account,
) -> CertClient:
    config.configure(
        debug=True,
        # trace_all=True,
    )

    client = CertClient(
        algod_client,
        # creator=creator_account,
        app_id=679628442,
        signer=creator_account.signer,
        indexer_client=indexer_client,
    )

    # client.deploy(
    #     on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    #     on_update=algokit_utils.OnUpdate.AppendApp,
    #     update_args=Deploy[UpdateArgs](args=UpdateArgs()),
    #     delete_args=Deploy[DeleteArgs](args=DeleteArgs()),
    # )
    return client


def test_update(cert_client: CertClient) -> None:
    cert_client.update_update()


def test_create_certificate_nft(cert_client: CertClient) -> None:
    args = NewCertificateNftArgs(
        name="Veecert",
        image_url="https::",
        certificate_id=1,
        metadata_hash=secrets.token_hex(16),
        unit_name="VEC-1"
    )
    result = cert_client.create_certificate_nft(args=args)
    print(result.return_value)


def test_says_hello(cert_client: CertClient) -> None:
    result = cert_client.hello(name="World")

    assert result.return_value == "Hello, World"


def test_simulate_says_hello_with_correct_budget_consumed(
    cert_client: CertClient, algod_client: AlgodClient
) -> None:
    result = cert_client.compose().hello(name="World").hello(name="Jane").simulate()

    assert result.abi_results[0].return_value == "Hello, World"
    assert result.abi_results[1].return_value == "Hello, Jane"
    assert result.simulate_response["txn-groups"][0]["app-budget-consumed"] < 100
