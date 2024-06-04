class Episode_meta:

    def __init__(self,
                 count: int,
                 start_time: list[float],
                 end_time: list[float],
                 episode_type: list[str]
                 ):
        self.__count = count
        self.__start_time = start_time  # In seconds
        self.__end_time = end_time  # In seconds
        self.__episode_type = episode_type

    # Getters
    @property
    def count(self) -> int:
        return self.__count

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def episode_type(self):
        return self.__episode_type

    def toDict(self) -> dict:
        return {
            'meta_episode_count': self.__count,
            'meta_episode_start_time': self.__start_time,
            'meta_episode_end_time': self.__end_time,
            'meta_episode_type': self.__episode_type
        }

    def __repr__(self):
        return (f"<Episode_meta: \n"
                f"count={self.__count}, \n"
                f"start_time={self.__start_time}, \n"
                f"end_time={self.__end_time}, \n"
                f"episode_type={self.__episode_type}\n"
                f">")
