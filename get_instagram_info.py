# (File intentionally left blank. All Instagram info/publishing code removed.)
import os
from dotenv import load_dotenv

def get_account_info():
    """
    Utility to get Instagram Business Account ID and verify access token.
    """
    load_dotenv()
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    
    if not access_token:
        print("ERROR: Access token not found in .env file")
        return
    
    # 1. First verify the access token
    verify_url = f"https://graph.facebook.com/debug_token"
    params = {
        'input_token': access_token,
        'access_token': access_token
    }
    
    try:
        print("\nVerifying access token...")
        response = requests.get(verify_url, params=params)
        token_info = response.json()
        
        print("\nToken Information:")
        print("-" * 50)
        if 'data' in token_info:
            print(f"Valid: {token_info['data'].get('is_valid', False)}")
            print(f"App ID: {token_info['data'].get('app_id')}")
            print(f"Expires: {token_info['data'].get('expires_at') or 'Never'}")
            print("\nPermissions:", token_info['data'].get('scopes', []))
        else:
            print("Error getting token info:", token_info.get('error', {}).get('message'))
            return
        
        # 2. Get Instagram Business Account ID
        print("\nFetching Instagram Business Account info...")
        me_url = "https://graph.facebook.com/v18.0/me"
        params = {
            'access_token': access_token,
            'fields': 'instagram_business_account'
        }
        
        response = requests.get(me_url, params=params)
        account_info = response.json()
        
        print("\nAccount Information:")
        print("-" * 50)
        if 'instagram_business_account' in account_info:
            ig_account_id = account_info['instagram_business_account']['id']
            print(f"Instagram Business Account ID: {ig_account_id}")
            
            # 3. Get account details
            account_url = f"https://graph.facebook.com/v18.0/{ig_account_id}"
            params = {
                'access_token': access_token,
                'fields': 'username,name,profile_picture_url'
            }
            
            response = requests.get(account_url, params=params)
            details = response.json()
            
            print(f"Username: {details.get('username')}")
            print(f"Name: {details.get('name')}")
            print("\nThis is your correct Instagram Business Account ID:", ig_account_id)
            print("\nUpdate your .env file with this ID")
            
        else:
            print("Error:", account_info.get('error', {}).get('message'))
            if 'error' in account_info:
                error = account_info['error']
                if error.get('code') == 190:
                    print("\nYour access token appears to be invalid or expired.")
                    print("Please get a new access token from the Meta Developer Dashboard.")
                elif error.get('code') == 24:
                    print("\nYour access token doesn't have the required permissions.")
                    print("Required permissions: instagram_basic, instagram_content_publish")
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    get_account_info()
