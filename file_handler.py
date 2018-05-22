import csv


class CSVWriterContextManager:
    def __init__(self, filename, field_names):
        self.csv_file = filename
        self.field_names = field_names
        self.mode = 'w'
        self.new_line = ''
        self.writer = None

    def __enter__(self):
        self.out_file = open(self.csv_file, self.mode, newline=self.new_line)
        self.writer = csv.DictWriter(self.out_file, delimiter=',', fieldnames=self.field_names)
        self.writer.writeheader()
        self.writer.fieldnames = self.field_names
        return self.writer

    def __exit__(self, exc_type, exc_value, traceback):
        self.out_file.close()
