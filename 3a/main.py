import argparse


class ClassHierarchyParser:
    def __init__(self):
        self.parent_child_mapping = {}
        self.ancestor_mapping = {}

    def add_class(self, parent_class, child_class):
        if child_class not in self.parent_child_mapping:
            self.parent_child_mapping[child_class] = {parent_class}
            self.ancestor_mapping[child_class] = {parent_class}
        else:
            self.parent_child_mapping[child_class].add(parent_class)

        if parent_class in self.ancestor_mapping:
            self.ancestor_mapping[child_class].update(
                self.ancestor_mapping[parent_class])

    def get_siblings(self, class_name):
        if class_name in self.parent_child_mapping:
            parent_class = self.parent_child_mapping[class_name]
            # print("parent_class", parent_class)
            return [
                child_class for child_class, parent in self.parent_child_mapping.items()
                if parent.intersection(parent_class) and child_class != class_name
            ]
        return []

    def get_parent_class(self, class_name):
        return list(self.parent_child_mapping.get(class_name, []))

    def get_ancestor_classes(self, class_name):
        return list(self.ancestor_mapping.get(class_name, []))

    def belong_to_same_ancestors(self, class_name1, class_name2):
        if class_name1 in self.ancestor_mapping and class_name2 in self.ancestor_mapping:
            ancestors1 = self.ancestor_mapping[class_name1]
            ancestors2 = self.ancestor_mapping[class_name2]
            return bool(ancestors1.intersection(ancestors2))
        return False


def parse_hierarchy_file(file_path):
    parser = ClassHierarchyParser()

    with open(file_path, 'r') as file:
        for line in file:
            parent_class, child_class = line.strip().split()
            parser.add_class(parent_class, child_class)

    return parser


def parse_id_to_name_file(file_path):
    id_to_name = {}

    with open(file_path, 'r') as file:
        for line in file:
            category_id, category_name = line.strip().split('\t')
            id_to_name[category_id] = category_name

    return id_to_name


def parse_name_to_id_file(file_path):
    name_to_id = {}

    with open(file_path, 'r') as file:
        for line in file:
            category_id, category_name = line.strip().split('\t')
            name_to_id[category_name] = category_id

    return name_to_id


def main():
    parser = argparse.ArgumentParser(description="Class Hierarchy Parser")
    parser.add_argument(
        "hierarchy_file", help="Path to the class hierarchy file")
    parser.add_argument("id_to_name_file",
                        help="Path to the ID to name mapping file")
    parser.add_argument("--siblings", metavar="CLASS",
                        help="Find siblings of a class")
    parser.add_argument("--parent", metavar="CLASS",
                        help="Find parent of a class")
    parser.add_argument("--ancestors", metavar="CLASS",
                        help="Find ancestors of a class")
    parser.add_argument("--same-ancestors", nargs=2, metavar=("CLASS1", "CLASS2"),
                        help="Check if two classes belong to the same ancestor(s)")

    args = parser.parse_args()

    hierarchy_file = args.hierarchy_file
    id_to_name_file = args.id_to_name_file

    # Parse the class hierarchy file
    class_parser = parse_hierarchy_file(hierarchy_file)

    # Parse the ID to name mapping file
    id_to_name = parse_id_to_name_file(id_to_name_file)

    # Parse the name to ID mapping file
    name_to_id = parse_name_to_id_file(id_to_name_file)
    # Perform the specified operations
    if args.siblings:
        id = name_to_id[args.siblings]
        siblings = class_parser.get_siblings(id)
        siblings = [id_to_name[sibling]
                    for sibling in siblings if sibling in id_to_name]
        print(f"Siblings of {args.siblings}: {siblings}")

    elif args.parent:
        id = name_to_id[args.parent]
        parents = class_parser.get_parent_class(id)
        parents = [id_to_name[parent]
                   for parent in parents if parent in id_to_name]
        print(f"Parent of {args.parent}: {parents}")
    elif args.ancestors:
        id = name_to_id[args.ancestors]
        ancestors = class_parser.get_ancestor_classes(id)
        print("ancestors", ancestors)
        ancestor_names = [id_to_name[ancestor]
                          for ancestor in ancestors if ancestor in id_to_name]
        print(f"Ancestors of {args.ancestors}: {ancestor_names}")
    elif args.same_ancestors:
        class1, class2 = args.same_ancestors
        belong_to_same_ancestors = class_parser.belong_to_same_ancestors(
            class1, class2)
        print(f"Belong to same ancestors: {belong_to_same_ancestors}")


if __name__ == "__main__":
    main()
