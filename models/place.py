#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql.schema import Table
from models.amenity import Amenity
from sqlalchemy.orm import relationship
from models import storage_type

if storage_type == "db":
    place_amenity = Table("place_amenity",
                          Base.metadata,
                          Column("place_id",
                                 String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id",
                                 String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = 'places'
    if storage_type == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity", backref="place_amenities",
                                 secondary=place_amenity, viewonly=False)
    else:
        city_id = user_id = name = description = ""
        number_rooms = number_bathrooms = max_guest = price_by_night = 0
        latitude = longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns list of `Review` instances with `place_id` == `Place.id`
            """
            from models.review import Review
            from models import storage

            all_reviews = storage.all(Review)

            return [rev_obj for rev_obj in all_reviews.values()
                    if rev_obj.place_id == self.id]

        @property
        def amenities(self):
            """Returns list of `Amenity` instances with `id` in `amenity_ids`
            """
            from models import storage

            amenities = storage.all(Amenity)

            return [amenity for amenity in amenities.values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Append amenity `id` to the list of amenity ids"""

            if type(obj) != Amenity:
                return

            if obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
