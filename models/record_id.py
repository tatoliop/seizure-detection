from pathlib import Path


class Record_id:

    def __init__(self,
                 subject: str,
                 record: str,
                 filename: str,
                 dataset: str,
                 has_episode: bool,
                 description: str = ''):
        self.__subject = subject
        self.__record = record
        self.__filename = filename
        self.__dataset = dataset
        self.__has_episode = has_episode
        self.__description = description

    # Getters
    @property
    def subject(self):
        return self.__subject

    @property
    def record(self):
        return self.__record

    @property
    def filename(self):
        return self.__filename

    @property
    def dataset(self):
        return self.__dataset

    @property
    def has_episode(self):
        return self.__has_episode

    @property
    def description(self):
        return self.__description

    def toDict(self) -> dict:
        return {
            'subject': self.__subject,
            'record': self.__record,
            'filename': self.__filename,
            'dataset': self.__dataset,
            'has_episode': self.__has_episode,
            'description': self.__description
        }

    def __repr__(self):
        return (f"<Record_id: \n"
                f"subject={self.__subject}, \n"
                f"record={self.__record}, \n"
                f"filename={self.__filename}, \n"
                f"dataset={self.__dataset}, \n"
                f"has_episode={self.__has_episode}, \n"
                f"description={self.__description}"
                f">")

    def __hash__(self):
        return hash((self.subject, self.record))

    def __eq__(self, __value):
        return (self.subject, self.record) == (__value.subject, __value.record)

    def __ne__(self, __value):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == __value)
