import requests
import time
from prettytable import PrettyTable


def check_and_claim(address):
    query_url = f"https://api.wukongfb.xyz/coins/wukong?address={address}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://www.wukongfb.xyz",
        "Referer": "https://www.wukongfb.xyz/"
    }

    claimed_amount = 0
    response = requests.get(query_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        available_amount = data['data']['available_amount']
        already_claim_amount = data['data']['already_claim_amount']

        if available_amount > 0:
            claim_url = "https://api.wukongfb.xyz/wukong-coin/claim"
            payload = {"address": address}

            claim_response = requests.post(claim_url, json=payload, headers=headers)
            if claim_response.status_code == 200 and claim_response.json()['code'] == 0:
                confirm_response = requests.get(query_url, headers=headers)
                if confirm_response.status_code == 200:
                    confirm_data = confirm_response.json()
                    claimed_amount = confirm_data['data']['already_claim_amount']
                    status = f"成功领取 {claimed_amount}"
                else:
                    status = "确认领取失败"
            else:
                status = "领取失败"
        else:
            if already_claim_amount > 0:
                status = f"已经领取 {already_claim_amount}"
                claimed_amount = already_claim_amount
            else:
                status = "没有资格领取"
    else:
        status = "查询失败"

    return status, claimed_amount


def main():
    file_path = input("这里输入txt文件路径：")
    total_claimed_amount = 0
    successful_claims = 0
    already_claimed = 0

    print("开始处理地址...\n")

    with open(file_path, 'r') as file:
        addresses = file.read().splitlines()

    # 创建表格
    table = PrettyTable()
    table.field_names = ["序号", "地址", "状态"]
    table.align["地址"] = "l"
    table.align["状态"] = "l"
    table.max_width["地址"] = 60  # 设置地址列的最大宽度，可以根据需要调整

    # 处理每个地址
    for index, address in enumerate(addresses, start=1):
        print(f"正在处理第 {index}/{len(addresses)} 个地址...")
        status, claimed = check_and_claim(address.strip())
        total_claimed_amount += claimed
        if '成功领取' in status:
            successful_claims += 1
        elif '已经领取' in status:
            already_claimed += 1

        # 添加到表格
        table.add_row([index, address, status])

        # 打印当前地址的结果
        print(f"地址: {address}")
        print(f"状态: {status}")
        print("-" * 50)

        time.sleep(1)  # 添加延迟以避免频繁请求

    # 打印完整结果表格
    print("\n处理完成！以下是完整结果：")
    print(table)

    # 打印总结
    print(f"\n总结：")
    print(f"- 总处理地址数：{len(addresses)}")
    print(f"- 本次成功领取地址数：{successful_claims}")
    print(f"- 之前已领取地址数：{already_claimed}")
    print(f"- 没有资格领取地址数：{len(addresses) - successful_claims - already_claimed}")
    print(f"- 总领取数量：{total_claimed_amount:.2f}")


if __name__ == "__main__":
    main()