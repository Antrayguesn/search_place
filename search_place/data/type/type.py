class Type:
    PROPERTIES = []

    def __init__(self, **kwargs):
        for key in self.__class__.PROPERTIES:
            setattr(self, key, kwargs.get(key, None))

    def to_dict(self):
        return {key: getattr(self, key, None) for key in self.PROPERTIES}

    def merge(self, merging_type, force=False):
        """
        Met à jour les champs qui sont None avec les valeurs de l'autre instance.
        Si `force=True`, remplace même les valeurs existantes.
        """
        for key, value in merging_type.to_dict().items():
            attr = getattr(self, key, None)

            if force:
                if value is not None:
                    setattr(self, key, value)
            else:
                if attr is None and value is not None:
                    setattr(self, key, value)
        return self

    def __repr__(self):
        return repr(self.to_dict())

    def __str__(self):
        return repr(self.to_dict())
