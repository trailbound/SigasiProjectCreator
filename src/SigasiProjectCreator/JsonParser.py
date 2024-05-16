# -*- coding: utf-8 -*-
"""
    :license: BSD, see LICENSE for more details.
"""
import json
import pathlib
from collections import defaultdict

from SigasiProjectCreator import abort_if_false, is_valid_name
from SigasiProjectCreator.ProjectFileParser import ProjectFileParser, project_file_parser, ProjectFileParserResult


@project_file_parser('json')
class JsonParser(ProjectFileParser):
    """JSON file parser"""
    def __init__(self):
        super().__init__()

    def parse_file(self, json_file, options=None):
        library_mapping = defaultdict(list)
        includes = set()
        defines = []
        with open(json_file, 'r') as f:
            compile_list = json.load(f)
            for library in compile_list:
                abort_if_false(is_valid_name(library), f'Invalid library name: {library}')
                for include_path in compile_list[library]['includes']:
                    includes.add(include_path)
                for file in compile_list[library]['files']:
                    library_mapping[file].append(library)
        return ProjectFileParserResult(library_mapping, verilog_defines=defines, verilog_includes=includes)

#            for row in reader:
#                if row:
#                    library = row[0].strip()
#                    if library == '#define':
#                        defines.append(row[1].strip())
#                    else:
#                        path = pathlib.Path(row[1].strip()).absolute().resolve()
#                        if library == '#include':
#                            includes.add(path)
#                        else:
#                            abort_if_false(is_valid_name(library), f'Invalid library name: {library}')
#                            library_mapping[path].append(library)
#        return ProjectFileParserResult(library_mapping, verilog_defines=defines, verilog_includes=includes)
