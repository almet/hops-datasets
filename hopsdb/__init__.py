import argparse
from hopsdb.scrappers import SCRAPPERS
from hopsdb.writers import WRITERS


def generate_datafiles(scrappers_classes, writers_classes, output_dir, input_dir):
    # Iterate on the different scrappers to retrieve all the data.
    # This might take some time.
    buffer_data = {}
    for scrapper_class in scrappers_classes:
        scrapper = scrapper_class(input_dir)
        buffer_data.update(scrapper.scrap())

    # Then iterate on the different writers
    for writer_class in writers_classes:
        writer = writer_class(output_dir)
        writer.write(buffer_data)


def main():
    parser = argparse.ArgumentParser(
        description='A tool to scrap hops producers websites and produce '
                    'machine-readable data out of it.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument('-o', '--output-path', dest='output_path',
                        help='Path where the output files will be generated.',
                        default='output')

    parser.add_argument('-i', '--input-path', dest='input_path',
                        help='Path where to find the intput files, if any. ',
                        default='inputs')

    args = parser.parse_args()
    generate_datafiles([SCRAPPERS['yakimahops']], WRITERS.values(), 'output', args.input_path)
