import csv


class WikipediaPropsFetcher:
    def __init__(self, path_to_csv_file, delimiter):
        with open(path_to_csv_file, encoding="utf8") as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            next(reader, None)

            self.dictionary = {row[0]: [row[1], row[2]] for row in reader}

    def get_identifier(self, wikidata_id):
        """
        Returns (entity) identifier of form WikipediaTitle_WikipediaPageId
        :param wikidata_id: wikidata_id without the Q at the beginning
        :return: Identifier to use in model for wikidata_id
        """
        wikipedia_page_id_title_tuple = self.dictionary.get("Q" + wikidata_id, None)
        if wikipedia_page_id_title_tuple is None:
            return None

        return wikipedia_page_id_title_tuple[1] + '_' + str(wikipedia_page_id_title_tuple[0])

    def get_title(self, wikidata_id):
        """
        Gets title to wikidata_id
        :param wikidata_id:
        :return:
        """
        wikipedia_page_id_title_tuple = self.dictionary.get("Q" + wikidata_id, None)
        if wikipedia_page_id_title_tuple is None:
            return None
        return wikipedia_page_id_title_tuple[1]


if __name__ == '__main__':
    a = WikipediaPropsFetcher('data/living_people_wikidata_id_wikipedia_page_id_title.csv', delimiter=';')
    print(len(a.dictionary))
    print(a.get_identifier('567'))


