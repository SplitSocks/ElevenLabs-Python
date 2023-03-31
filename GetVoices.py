    def get_API_voices(self):
        url = 'https://api.elevenlabs.io/v1/voices'
        headers = {
            'accept': 'application/json',
            'xi-api-key': self.get_api_key()
            }

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for voice in data['voices']:
                print(f"Name: {voice['name']}, Voice ID: {voice['voice_id']}")
        else:
            print(f"Error getting voices: {response.status_code}")