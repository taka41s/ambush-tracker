import csv
from linkedin_api import Linkedin

api = Linkedin('linkedin-bot@getambush.com', 'BHbNgEuJRePXx7C')

class Crawler:
    @staticmethod
    def run():
        with open('notambush.txt', 'w') as arquivo:
            arquivo.write("") 

        with open('url-list.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)
            lines = [(row[0].strip(), row[1].strip()) for row in reader]

        profile_ids = []

        for nome, url in lines:
            profile_id = Crawler.extract_linkedin_id(url)
            if profile_id:
                profile_ids.append(profile_id)

        for profile_id in profile_ids:
            print(profile_id)
            profile = api.get_profile(profile_id)
            ambush_experiences = [exp for exp in profile.get('experience', []) if exp.get('companyName') == 'Ambush']

            if not ambush_experiences:
                with open('notambush.txt', 'a') as file:
                    file.write('https://www.linkedin.com/in/' + profile_id + "\n")
                print("Nenhuma experiência encontrada com a empresa 'Ambush'. URL escrita em notambush.txt.")

    @staticmethod
    def extract_linkedin_id(url):
        if '/in/' in url:
            profile_id = url.split('/in/')[-1].strip('/')

            return profile_id
        else:
            return None