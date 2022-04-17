import sys
import threading
import json
import requests
import time

from oci.config import from_file
from oci.signer import Signer

from fetch import fetch_instance
from create import create_instance


def main(auth, region, tenancy, create_instance_option, webhook_url, mention_id):
    fetch_result = fetch_instance(auth, tenancy, region)
    if fetch_result == "[]":
        create_result = json.loads(create_instance(
            auth, region, create_instance_option
        ))
        failed = True
        if create_result["code"] == "InternalError":
            title = ":no_entry: 인스턴스 생성 실패"
            description = "사용량 초과."
            color = 16711680
        elif create_result["code"] == "TooManyRequests":
            title = ":no_entry: 인스턴스 생성 실패"
            description = "요청 횟수 초과.\n요청 주기를 변경하세요."
            color = 16711680
        else:
            title = ":white_check_mark: 인스턴스 생성 성공"
            description = "축하합니다! 인스턴스가 생성되었습니다."
            color = 32768
            failed = False

        content = ""
        if len(mention_id) != 0:
            for id in mention_id:
                content += f"<@{id}>"

        requests.post(
            webhook_url,
            json={
                "content": content,
                "embeds": [
                    {
                        "title": title,
                        "description": description,
                        "color": color,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                    }
                ]
            }
        )
        if not failed:
            sys.exit(0)
    else:
        sys.exit(0)

    if "-r" in sys.argv:
        try:
            repeat_interval = int(sys.argv[sys.argv.index("-r") + 1])
        except:
            repeat_interval = 300
        threading.Timer(
            repeat_interval,
            main,
            [auth, region, tenancy, create_instance_option, webhook_url, mention_id]
        ).start()


if __name__ == "__main__":
    print("Running...")
    with open("./config.json", "r") as file:
        config = json.load(file)
    oracle_cloud_config = from_file(config["oracle_cloud_config"], "DEFAULT")
    auth = Signer(
        tenancy=oracle_cloud_config["tenancy"],
        user=oracle_cloud_config["user"],
        fingerprint=oracle_cloud_config["fingerprint"],
        private_key_file_location=oracle_cloud_config["key_file"]
    )
    main(
        auth,
        oracle_cloud_config["region"],
        oracle_cloud_config["tenancy"],
        config["create_instance_option"],
        config["webhook_url"],
        config["mention_id"]
    )
