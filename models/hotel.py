from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = "hoteis"
    id = banco.Column(banco.String, primary_key=True)
    name = banco.Column(banco.String)
    stars = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String)

    def __init__(self, id, name, stars, diaria, cidade):
        self.id = id
        self.name = name
        self.stars = stars
        self.diaria = diaria
        self.cidade = cidade

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "stars": self.stars,
            "diaria": self.diaria,
            "cidade": self.cidade,
        }

    @classmethod
    def find_hotel(cls, id):
        hotel = cls.query.filter_by(id=id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, name, stars, diaria, cidade):
        self.name = name
        self.stars = stars
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
