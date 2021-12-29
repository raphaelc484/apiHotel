from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from resources.filtros import (
    normalize_path_params,
    consulta_sem_cidade,
    consulta_com_cidade,
)
from flask_jwt_extended import jwt_required
import sqlite3


path_params = reqparse.RequestParser()
path_params.add_argument("cidade", type=str)
path_params.add_argument("stars_min", type=float)
path_params.add_argument("stars_max", type=float)
path_params.add_argument("diaria_min", type=float)
path_params.add_argument("diaria_max", type=float)
path_params.add_argument("limit", type=float)
path_params.add_argument("offset", type=float)


class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect("banco.db")
        cursor = connection.cursor()

        dados = path_params.parse_args()
        dados_validos = {
            chave: dados[chave] for chave in dados if dados[chave] is not None
        }
        parametros = normalize_path_params(**dados_validos)
        if not parametros.get("cidade"):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla)
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)
        hoteis = []
        for linha in resultado:
            hoteis.append(
                {
                    "id": linha[0],
                    "name": linha[1],
                    "stars": linha[2],
                    "diaria": linha[3],
                    "cidade": linha[4],
                }
            )

        return {"hoteis": hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument(
        "name",
        type=str,
        required=True,
        help="The field 'name' cannot be left blank.",
    )
    argumentos.add_argument(
        "stars",
        type=float,
        required=True,
        help="The field 'stars' cannot be left blank",
    )
    argumentos.add_argument("diaria")
    argumentos.add_argument("cidade")

    def get(self, id):
        hotel = HotelModel.find_hotel(id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel not found."}, 404

    @jwt_required()
    def post(self, id):
        if HotelModel.find_hotel(id):
            return {"message": "Hotel id '{}' already exists.".format(id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {
                "message": "An internal error ocurred tryng to save hotel."
            }, 500
        return hotel.json()

    @jwt_required()
    def put(self, id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {
                "message": "An internal error ocurred tryng to save hotel."
            }, 500
        return hotel.json(), 201

    @jwt_required()
    def delete(self, id):
        hotel = HotelModel.find_hotel(id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {
                    "message": "An internal error ocurred tryng to save hotel."
                }, 500
            return {"message": "Hotel deleted"}
        return {"message": "Hotel deleted."}, 404
