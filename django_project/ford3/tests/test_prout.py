from django.test import TestCase

class TestUtils(TestCase):

    def runTest(self):
        data = {
            'names': ['event_one', 'event_two'],
            'start_dates': ['date_one', 'date_two'],
            'end_dates': ['end_date_one', 'end_date_two'],
            'http_links': ['link1', 'link2']
        }
        result = my_function(data)
        print(result)
        self.assertEqual(len(result), 2)
        event_one = result[0]
        self.assertEqual(
            list(event_one.keys()), ['name', 'start_date', 'end_date', 'http_link'])
        self.assertEqual(event_one['name'], 'event_one')


        data = {
            'penguins': ['michel'],
            'seals': ['bernard']
        }

        result = my_function(data)
        print(result)
        self.assertEqual(result, [{'penguin': 'michel', 'seal': 'bernard'}])


def to_dict(data, zip_tuple):
    my_dict = {key[:-1]: None for key in data}
    
    for index, value in enumerate(zip_tuple):        
        key = list(my_dict.items())[index][0]
        my_dict[key] = value
    
    return my_dict

def zip_list_dict(data):
    values = list(zip(*[value for key, value in data.items()]))

    return [to_dict(data, zip_tuple) for zip_tuple in values]


def my_function(data):
    result = []
    names = data['names']
    start_dates = data['start_dates']
    end_dates = data['end_dates']
    http_links = data['http_links']
    event_count = len(names)
    for i in range(0, event_count):
        new_event = {}
        name = names[i]
        start_date = start_dates[i]
        end_date = end_dates[i]
        http_link = http_links[i]
        new_event['name'] = name
        new_event['start_date'] = start_date
        new_event['end_date'] = end_date
        new_event['http_link'] = http_link
        result.append(new_event)
    return result
# we have 4 lists of n elements
# we want one list of n dict
# a dict has 4 keys: name, start_date, end_date, http_link