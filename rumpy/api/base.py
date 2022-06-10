import base64
import datetime
import logging
import os
from typing import Any, Dict, List

import rumpy.utils as utils
from rumpy.client._requests import HttpRequest
from rumpy.exceptions import *

logger = logging.getLogger(__name__)


class BaseAPI:
    def __init__(self, http: HttpRequest = None):
        self._http = http

    def _get(self, endpoint: str, payload: Dict = {}):
        api_base = None
        if hasattr(self, "API_BASE"):
            api_base = self.API_BASE
        return self._http.get(endpoint, payload, api_base)

    def _post(self, endpoint: str, payload: Dict = {}):
        api_base = None
        if hasattr(self, "API_BASE"):
            api_base = self.API_BASE
        return self._http.post(endpoint, payload, api_base)

    def check_group_id_as_required(self, group_id=None):
        group_id = group_id or self._http.group_id
        if not group_id:
            raise ParamValueError("group_id is required, now it's None.")
        return group_id

    def check_group_joined_as_required(self, group_id=None):
        group_id = self.check_group_id_as_required(group_id)
        if group_id not in self._http.api.groups_id:
            raise RumChainException(f"You are not in this group: <{group_id}>.")
        return group_id

    def check_group_owner_as_required(self, group_id=None):
        group_id = self.check_group_joined_as_required(group_id)
        info = self._http.api.group_info(group_id)
        if info.user_pubkey != info.owner_pubkey:
            raise RumChainException(f"You are not the owner of this group: <{group_id}>.")
        return group_id

    def is_joined(self, group_id=None) -> bool:
        try:
            self.check_group_joined_as_required(group_id)
            return True
        except:
            return False

    def is_owner(self, group_id=None) -> bool:
        """return True if I create this group else False"""
        try:
            self.check_group_owner_as_required(group_id)
            return True
        except:
            return False

    def raise_error(self, resp, except_err=None):
        if err := resp.get("error"):
            if err != except_err:
                raise RumChainException(err)
        return resp

    def like(self, trx_id: str, group_id=None) -> Dict:
        return self._http.api._send(like_trx_id=trx_id, activity_type="Like", group_id=group_id)

    def dislike(self, trx_id: str, group_id=None) -> Dict:
        return self._http.api._send(like_trx_id=trx_id, activity_type="Dislike", group_id=group_id)

    def __send_note(self, group_id=None, **kwargs):
        return self._http.api._send(group_id=group_id, activity_type="Add", object_type="Note", **kwargs)

    def send_note(self, content: str = None, images: List = None, name=None, group_id=None):
        return self.__send_note(content=content, images=images, name=None, group_id=group_id)

    def del_note(self, trx_id, group_id=None):
        return self.__send_note(del_trx_id=trx_id, group_id=group_id)

    def edit_note(self, trx_id, content: str = None, images: List = None, group_id=None):
        return self.__send_note(
            edit_trx_id=trx_id,
            content=content,
            images=images,
            group_id=group_id,
        )

    def reply(self, trx_id: str, content: str = None, images=None, group_id=None):
        return self.__send_note(
            reply_trx_id=trx_id,
            content=content,
            images=images,
            group_id=group_id,
        )

    def trx_retweet_params(self, trx, group_id=None, nicknames={}):
        """trans from trx to an object of new trx to send to chain.
        Returns:
            obj: object of NewTrx,can be used as: self.send_note(obj=obj).
        """
        refer_tid = utils.get_refer_trxid(trx)
        refer_trx = None
        if refer_tid:
            refer_trx = self._http.api.trx(trx_id=refer_tid, group_id=group_id)
        params = utils.trx_retweet_params_init(trx=trx, refer_trx=refer_trx, nicknames=nicknames)
        return params

    def search_file_trxs(self, trx_id=None, group_id=None):
        trxs = self.get_group_all_contents(trx_id=trx_id, group_id=group_id)
        infos = []
        filetrxs = []
        for trx, _ in trxs:
            if trx["Content"].get("name") == "fileinfo":
                info = eval(base64.b64decode(trx["Content"]["file"]["content"]).decode("utf-8"))
                logger.debug(f"{info}")
                infos.append(info)
            if trx["Content"].get("type") == "File":
                filetrxs.append(trx)
        return infos, filetrxs

    def upload_file(self, file_path, group_id=None):
        if not os.path.isfile(file_path):
            logger.warning(f"{file_path} is not a file.")
            return
        for obj in utils.split_file_to_trx_objs(file_path):
            resp = self._http.api._send(obj=obj, activity_type="Add", group_id=group_id)

    def download_files(self, file_dir, group_id=None):
        infos, trxs = self.search_file_trxs(group_id)
        utils.merge_trxs_to_files(file_dir, infos, trxs)

    def get_group_all_contents(
        self,
        trx_id=None,
        group_id=None,
        senders=None,
        trx_types=None,
        reverse=False,
    ):
        """返回的是一个生成器，可以用 for ... in ... 来迭代访问。trx_types 的取值见 utils.trx_type() 的各种返回值"""
        trxs = self._http.api.get_group_content(group_id=group_id, trx_id=trx_id, num=20, reverse=reverse)
        checked_trxids = []
        trx_types = trx_types or []
        senders = senders or []
        while trxs:
            if trx_id in checked_trxids:
                break
            else:
                checked_trxids.append(trx_id)
            for trx in trxs:
                flag1 = (utils.trx_type(trx) in trx_types) or (not trx_types)
                flag2 = (trx.get("Publisher", "") in senders) or (not senders)
                if flag1 and flag2:
                    yield trx, trx.get("TrxId")
            trx_id = utils.last_trx_id(trx_id, trxs, reverse=reverse)
            trxs = self._http.api.get_group_content(group_id=group_id, trx_id=trx_id, num=20, reverse=reverse)

    def get_profiles(
        self,
        trx_id=None,
        types=("name", "image", "wallet"),
        group_id=None,
        pubkey=None,
        users=None,
    ):
        group_id = self.check_group_id_as_required(group_id)
        senders = [pubkey] if pubkey else None
        trxs = self.get_group_all_contents(
            trx_id=trx_id,
            group_id=group_id,
            trx_types=["person"],
            senders=senders,
            reverse=False,
        )
        users = users or {}
        progress_tid = None
        for trx, tid in trxs:

            progress_tid = tid
            if trx_content := trx.get("Content"):
                pubkey = trx["Publisher"]
                users[pubkey] = users.get(pubkey, {})
                for key in trx_content:
                    if key in types:
                        users[pubkey].update({key: trx_content[key]})
        return users, progress_tid

    def update_profiles_data(
        self,
        users_data: Dict = {},
        types=("name", "image", "wallet"),
        group_id=None,
        pubkey=None,
    ) -> Dict:
        """update users_data and returns it.
        {
            group_id:  "", # the group_id
            group_name: "", # the group_name
            trx_id: "", # the trx_id of groups progress
            trx_timestamp:"",
            update_at: "",
            data:{ pubkey:{
                name:"",
                image:{},
                wallet:[],
                }
            }
        }
        """
        # check group_id

        group_id = users_data.get("group_id") or self.check_group_id_as_required(group_id)

        # get new trxs from the trx_id
        trx_id = users_data.get("trx_id", None)
        users = users_data.get("data", {})
        users, progress_tid = self.get_profiles(
            users=users,
            trx_id=trx_id,
            types=types,
            group_id=group_id,
            pubkey=pubkey,
        )
        try:
            _ts = self._http.api.trx(group_id=group_id, trx_id=progress_tid)["TimeStamp"]
            _dt = utils.timestamp_to_datetime(_ts)
        except TypeError:
            _dt = None

        _now = datetime.datetime.now()
        users_data.update(
            {
                "group_id": group_id,
                "trx_id": progress_tid,
                "trx_timestamp": str(_dt or _now),
                "data": users,
                "update_at": str(_now),
            }
        )
        return users_data
