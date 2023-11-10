# duolingo_request.py
import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

def load_offsets_from_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data.get("offsets", [])

def make_request(user_id, token, offset_names):
    try:
        url = "https://android-api-cf.duolingo.com/2017-06-30/batch?fields=responses%7Bbody%2Cstatus%2Cheaders%7D"
        headers = {
            "Cookie": "wuuid=b91f4ddf-d4f4-4ef8-b47c-04f5531e85db",
            "Authorization": rf"Bearer {token}",
            "User-Agent": "Duodroid/5.117.4 Dalvik/2.1.0 (Linux; U; Android 13; RMX3360 Build/TQ3C.230901.001.B1)",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }
        if user_id == "909819677":  #Added Skip Option 
            offset_names = [offset for offset in offset_names if offset != "xp_boost_stackable"]

        for offset_name in offset_names:
            request_data = {
                "requests": [
                    {
                        "body": json.dumps({"id": offset_name, "isFree": True}),
                        "bodyContentType": "application/json",
                        "method": "POST",
                        "url": rf"/2017-06-30/users/{user_id}/shop-items?fields=id%2CpurchaseDate%2CpurchasePrice%2Cquantity%2CsubscriptionInfo%7Bcurrency%2CexpectedExpiration%2CisFreeTrialPeriod%2CperiodLength%2Cprice%2CproductId%2Crenewer%2Crenewing%2CvendorPurchaseId%7D%2CwagerDay%2CexpectedExpirationDate%2CpurchaseId%2CremainingEffectDurationInSeconds%2CexpirationEpochTime%2CfamilyPlanInfo%7BownerId%2CsecondaryMembers%2CinviteToken%2CpendingInvites%7BfromUserId%2CtoUserId%2Cstatus%7D%7D",
                    }
                ],
                "includeHeaders": False,
            }

            request_data_json = json.dumps(request_data)

            response = requests.post(url, data=request_data_json, headers=headers)
            response.raise_for_status()

            with open("response_output.json", 'a') as output_file:
                # Append data to the file
                json.dump(response.json(), output_file, indent=2)
                output_file.write("\n")

            print(f"Response written to response_output.json for User ID: {user_id} and id: {offset_name}")

    except requests.exceptions.RequestException as e:
        print(f"Request failed for User ID {user_id}: {e}")

def run_make_request():
    while True:
        user_ids = os.getenv("USER_IDS", "").split(",")
        
        for user_id in user_ids:
            token_var = user_id + "_TOKEN"
            token = os.getenv(token_var)

            # Load offset names from the JSON file
            offset_names = load_offsets_from_json("offsets.json")
            
            make_request(user_id, token, offset_names)

        # Sleep for 15 minutes before starting again
        print("Cooling down for 15 minutes...")
        time.sleep(15 * 60)

if __name__ == '__main__':
    run_make_request()
