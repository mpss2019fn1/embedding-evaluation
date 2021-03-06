import csv
import os

from gensim_loader import VectorLoader
from metrics import mean_squared_pairwise_distance
from tasks import NeighborhoodTask


def build_groups(person_url_property_url_filepath, property_url_name_filepath, output_directory):
    # person_property_filepath laden
    with open(person_url_property_url_filepath, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        groups = {}
        for row in reader:
            values = groups.get(row[1])
            if values is None:
                values = []
                groups[row[1]] = values
            values.append(row[0])

    with open(property_url_name_filepath, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        property_url_name_dict = {row[0]: row[1] for row in reader}

    for property_url in groups:
        people_urls = groups[property_url]
        property_label = property_url_name_dict.get(property_url, "LabelNoFound")
        with open(os.path.join(output_directory, property_label + '.csv'), 'w+') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([property_label])
            csv_writer.writerows([row] for row in people_urls)


if __name__ == '__main__':
    LANG = 'de'
    ROOT_DIRECTORY = '/home/mapp/masterprojekt/Neighborhood Evaluations/'
    INPUT_DIRECTORY = f'{os.path.join(ROOT_DIRECTORY, LANG + "_occupations")}'

    loader = VectorLoader('doc2vec.binary.model')

    output = []

    for filename in os.listdir(INPUT_DIRECTORY):
        if filename.endswith('.csv'):
            with open(os.path.join(INPUT_DIRECTORY, filename), encoding='utf-8') as file:
                task = NeighborhoodTask(filename[:-4], file, mean_squared_pairwise_distance, loader, True)
                task()
                output.append(f'{filename[:-4]};'
                              f'{task.statistics.name_of_metric};'
                              f'{task.statistics.wikidata_entry_count};'
                              f'{task.statistics.embeddings_found};'
                              f'{task.statistics.score}')

    with open(os.path.join(ROOT_DIRECTORY, LANG + "_person_occupation_mean_distance.csv"), "w+") as file:
        file.write("dataset;name_of_metric;wikidata_entries;found_embeddings;score\n")
        {file.write(row + "\n") for row in output}

    loader.save_to_file(loader.identifier_not_found_set,
                        os.path.join(ROOT_DIRECTORY, LANG + '_not_found_identifiers.txt'))
    loader.save_to_file(loader.embedding_not_found_set,
                        os.path.join(ROOT_DIRECTORY, LANG + '_not_found_embeddings.txt'))

    # build_groups(os.path.join(ROOT_DIRECTORY, LANG + '_person_occupation.csv'),
    #              os.path.join(ROOT_DIRECTORY, LANG + '_occupation_name.csv'),
    #              INPUT_DIRECTORY)
