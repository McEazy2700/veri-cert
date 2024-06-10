from algopy import (
    ARC4Contract,
    Global,
    arc4,
    itxn,
    op,
)


class NewCertificateNftArgs(arc4.Struct, kw_only=True):
    name: arc4.String
    image_url: arc4.String
    certificate_id: arc4.UInt64
    metadata_hash: arc4.String
    unit_name: arc4.String


class Cert(ARC4Contract):
    @arc4.abimethod()
    def hello(self, name: arc4.String) -> arc4.String:
        return "Hello, " + name

    @arc4.abimethod()
    def create_certificate_nft(
        self,
        args: NewCertificateNftArgs,
    ) -> arc4.UInt64:
        txn = itxn.AssetConfig(
            asset_name=args.name.native,
            fee=1000,
            unit_name=args.unit_name.native,
            url=args.image_url.native,
            manager=Global.current_application_address,
            freeze=Global.current_application_address,
            clawback=Global.current_application_address,
            reserve=Global.current_application_address,
            metadata_hash=args.metadata_hash.native.bytes,
        )
        txn.submit()
        asset = op.ITxn.created_asset_id()

        return arc4.UInt64(asset.id)

    @arc4.abimethod(allow_actions=["UpdateApplication"])
    def update(self) -> bool:
        return True

    @arc4.abimethod(allow_actions=["DeleteApplication"])
    def delete(self) -> bool:
        return True
