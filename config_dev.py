import os

################ Rum ################
# quorum_client_port
rum_port = 58356

################ token ################
rum_asset_id = "4f2ec12c-22f4-3a9e-b757-c84b6415ea8f"

################ xin ################

# git clone https://github.com/liujuanjuan1984/mixin-sdk-python

mixin_sdk_dirpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mixin-sdk-python")
mixin_bot_config_file = os.path.join(mixin_sdk_dirpath, "data", "bot-keystore.json")
