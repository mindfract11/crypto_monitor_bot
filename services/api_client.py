import httpx

async def get_crypto_price(coin_id: str) -> float | None:
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

            if response.status_code == 200:
                data = response.json()
                if coin_id in data and "usd" in data[coin_id]:
                    price = float(data[coin_id]["usd"])
                    return price
                else:
                    print(f"[API ERROR] Money '{coin_id}' is not find in API.")
                    return None
            else:
                print(f"[API ERROR] Status code: {response.status_code}")
                return None

    except Exception as e:
        print(f"[API ERROR] Connection failed: {e}")
        return None