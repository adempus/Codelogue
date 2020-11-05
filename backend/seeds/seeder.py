from abc import ABC, abstractmethod
from src.app.models import db, ProgrammingLanguage


class Seeder(ABC):
    def __init__(self, resPath):
        self._resourcePath = resPath
        self._db = db

    @staticmethod
    @abstractmethod
    def run(self):
        pass

    def iterateSeed(self):
        with open(self._resourcePath) as file:
            contents = file.read()
            for index, value in enumerate(contents.splitlines()):
                yield value


class ProgrammingLanguageSeeder(Seeder):
    def __init__(self, resPath='seeds/data/programming_languages.txt'):
        super().__init__(resPath)

    def run(self):
        for language in self.iterateSeed():
            print(f"seeding table ProgrammingLanguage with {language}")
            seed = ProgrammingLanguage(name=language)
            self._db.session.add(seed)
            self._db.session.commit()

        print(f"done seeding ProgrammingLanguage table. ")

