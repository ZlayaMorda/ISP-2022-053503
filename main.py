import argparse
import ser_package.factory_serializer as fs
import ser_package.serializers as sp

if __name__ == '__main__':
    types = {"json": sp.JsonSerializer(), "toml": sp.TomlSerializer(), "yaml": sp.YamlSerializer()}

    parser = argparse.ArgumentParser(description='utility for converting between toml, yaml, json, code')
    parser.add_argument("ser_or_deser", help="serialization(ser) or deserialization(deser)")
    parser.add_argument("from_type", help="convert from this type")
    parser.add_argument("first_path", help="path of first file")
    parser.add_argument("to_type", help="convert to this type")
    parser.add_argument("second_path", help="path of second file")

    args = parser.parse_args()
    if args.ser_or_deser == "serialization" or args.ser_or_deser == "ser":
        if (args.from_type != args.to_type) and (args.first_path != args.second_path) \
                and args.from_type in types.keys() and args.to_type in types.keys():
            with open(args.first_path, "r") as file:
                string = ""
                for i in file.readlines():
                    string += i
                fs.dump(types[args.from_type], string, args.second_path, args.from_type, args.to_type)
        else:
            print("input correct types")

    elif args.ser_or_deser == "deserialization" or args.ser_or_deser == "deser":
        if args.from_type in types and args.to_type == "code":
            code = str(fs.load(types[args.from_type], args.first_path))
            with open(args.second_path, "w") as file:
                file.write(code)
        else:
            print("input correct types")
