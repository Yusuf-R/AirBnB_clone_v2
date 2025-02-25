#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of either all models or models of `cls`

        Arguments:
            cls (type): class for which to return instances of

        Returns:
            dictionary of <object_name>.<object_id> as keys and object as value
        """

        if not cls:
            return FileStorage.__objects

        return {key: obj
                for key, obj in FileStorage.__objects.items()
                if type(obj) == cls}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f, indent=2)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel, 'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes `obj` from `objects` dictionary

        Arguments:
            obj (instance): instance of a class to delete
        """
        from models.base_model import BaseModel

        if not obj:
            return

        if not isinstance(obj, BaseModel):
            raise TypeError(f"{obj} must be an instance of BaseModel")

        try:
            key = f"{obj.__class__.__name__}.{obj.id}"
            del FileStorage.__objects[key]
            FileStorage.save(self)
        except KeyError:
            pass

    def close(self):
        """Calls reload() method"""
        self.reload()
