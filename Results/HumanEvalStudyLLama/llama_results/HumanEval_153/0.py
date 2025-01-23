def Strongest_Extension(class_name, extensions):
    def extension_strength(extension):
        return sum(1 for c in extension if c.isupper()) - sum(1 for c in extension if c.islower())

    strongest_extension = max(extensions, key=extension_strength)
    return class_name + '.' + strongest_extension