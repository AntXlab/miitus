def update_pypath():
    import sys, os
    from os.path import join, isdir, isfile, dirname, abspath

    libs_dir = dirname(abspath(__file__))
    for name in os.listdir(libs_dir):
        lib_path = join(libs_dir, name)
        if lib_path in sys.path:
            continue
        if isdir(lib_path) and isfile(join(join(lib_path, name), '__init__.py')):
            """ check if it's a package """
            sys.path.append(lib_path)

update_pypath()

