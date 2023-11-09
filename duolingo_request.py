import requests
import json
import time

def make_request():
    while True:
        try:
            with open("response.json", 'r') as json_file:
                data = json.load(json_file)
            userid = data.get("user_id", "")
            authorization_token = data.get("token", "")

            url = "https://android-api-cf.duolingo.com/2017-06-30/batch?fields=responses%7Bbody%2Cstatus%2Cheaders%7D"
            headers = {
                "Cookie": "wuuid=b91f4ddf-d4f4-4ef8-b47c-04f5531e85db",
                "Authorization": rf"Bearer {authorization_token}",
                "User-Agent": "Duodroid/5.117.4 Dalvik/2.1.0 (Linux; U; Android 13; RMX3360 Build/TQ3C.230901.001.B1)",
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip, deflate",
            }
            request_data = {
                "requests": [
                    {
                        "body": '{"id":"xp_boost_stackable","isFree":true, "xpBoostMinutes":15, "xpBoostSource": "WIDGET_REWARD"}',
                        "bodyContentType": "application/json",
                        "method": "POST",
                        "url": rf"/2017-06-30/users/{userid}/shop-items?fields=id%2CpurchaseDate%2CpurchasePrice%2Cquantity%2CsubscriptionInfo%7Bcurrency%2CexpectedExpiration%2CisFreeTrialPeriod%2CperiodLength%2Cprice%2CproductId%2Crenewer%2Crenewing%2CvendorPurchaseId%7D%2CwagerDay%2CexpectedExpirationDate%2CpurchaseId%2CremainingEffectDurationInSeconds%2CexpirationEpochTime%2CfamilyPlanInfo%7BownerId%2CsecondaryMembers%2CinviteToken%2CpendingInvites%7BfromUserId%2CtoUserId%2Cstatus%7D%7D",
                    }
                ],
                "includeHeaders": False,
            }

            request_data_testingphase = {
                
                    "requests": [
                        {
                            "body": '{"id":"xp_boost_15","isFree":true}',
                            "bodyContentType": "application/json",
                            "method": "POST",
                            "url": rf"/2017-06-30/users/{userid}/shop-items?fields=id%2CpurchaseDate%2CpurchasePrice%2Cquantity%2CsubscriptionInfo%7Bcurrency%2CexpectedExpiration%2CisFreeTrialPeriod%2CperiodLength%2Cprice%2CproductId%2Crenewer%2Crenewing%2CvendorPurchaseId%7D%2CwagerDay%2CexpectedExpirationDate%2CpurchaseId%2CremainingEffectDurationInSeconds%2CexpirationEpochTime%2CfamilyPlanInfo%7BownerId%2CsecondaryMembers%2CinviteToken%2CpendingInvites%7BfromUserId%2CtoUserId%2Cstatus%7D%7D"
                        }
                    ],
                    "includeHeaders": False,
            }
            #request_data_json_new = json.dumps(request_data_testingphase)
            request_data_json = json.dumps(request_data)

            #response = requests.post(url, data=request_data_json_new, headers=headers)
            #response.raise_for_status()
            #with open("response_output.json", 'a') as output_file:
                # json.dump(response.json(), output_file, indent=2)

            response = requests.post(url, data=request_data_json, headers=headers)
            response.raise_for_status()


            #Debugger : 
            with open("response_output.json", 'a') as output_file:
                 json.dump(response.json(), output_file, indent=2)


            #print("Response written to response_output.json")

            #time.sleep(15 * 60) #Testing with 10sec 
            time.sleep(2)
            print("Response Successfull")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
