from typing import List


class GptOutputFormatter:

    @staticmethod
    def plan_today_format(schedule: List):
        json_list = []
        for x in schedule:
            description, hour = x
            element = {
                'hour': hour,
                'description': description
            }
            json_list.append(element)
        return json_list
