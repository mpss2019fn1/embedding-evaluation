import csv


class WikipediaPropsFetcher:
    def __init__(self, path_to_csv_file):
        with open(path_to_csv_file, encoding="utf8") as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            self.dictionary = {row[0]: row[2]+'_'+row[1] for row in reader}

    def get_identifier(self, wikidata_id):
        return self.dictionary.get('Q'+wikidata_id, None)


if __name__ == '__main__':
    a = WikipediaPropsFetcher('living_people_wikidata_id_wikipedia_page_id_title.csv')
    print(len(a.dictionary))
    print(a.get_identifier('Q567'))

