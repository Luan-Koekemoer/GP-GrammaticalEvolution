from os import path


class Bnf:
    def __init__(self, bnf_file, function_map):
        self.bnf_dict = self.__create_bnf(bnf_file)
        self.function_map = function_map

    def __create_bnf(self, pybnf_file):
        if not path.exists(pybnf_file):
            raise FileNotFoundError

        bnf = {}
        with open(pybnf_file) as filestream:
            for line in filestream.readlines():
                if line == "\n":
                    continue
                else:
                    ge_line = line.split("::=")
                    ge_line[0] = ge_line[0].strip()
                    ge_line[1] = ge_line[1].strip().replace("\n", "")

                    ge_line_options = ge_line[1].split("|")
                    if len(ge_line_options) == 1:
                        ge_line_options = ge_line_options[0].split(" ")
                    ge_line_options = list(map(lambda x: x.strip(), ge_line_options))
                    bnf[ge_line[0]] = ge_line_options

        return bnf

    def convert_bnf_to_py(self, bnf, chromosome, filepath_out):
        pass
